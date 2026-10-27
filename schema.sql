-- ==================================================================
-- NXE POND FAM: SPOOKY HALLOWEEN AVATAR & COSTUME COMPETITION
-- Complete Supabase Postgres Database Schema & RPC Functions
-- ==================================================================

-- 1. Enable pgcrypto for UUID generation if not already enabled
create extension if not exists "pgcrypto";

-- 2. Drop existing tables if re-running (clean slate)
drop function if exists cast_vote(text, uuid);
drop function if exists remove_vote(text, uuid);
drop table if exists votes cascade;
drop table if exists entries cascade;
drop table if exists quiz_attempts cascade;
drop table if exists questions cascade;
drop table if exists login_attempts cascade;
drop table if exists admin_log cascade;
drop table if exists settings cascade;
drop table if exists roster cascade;

-- 3. Table: roster
create table roster (
    governor_id text primary key,
    added_at timestamptz not null default now()
);

-- 4. Table: entries
create table entries (
    id uuid primary key default gen_random_uuid(),
    governor_id text unique not null references roster(governor_id) on delete cascade,
    ingame_name text not null,
    image_path text,
    thumb_path text,
    backstory text not null,
    quiz_score int not null default 0,
    qualified boolean not null default false,
    hidden boolean not null default false,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- 5. Table: questions (fantasy lore pool)
create table questions (
    id serial primary key,
    text text not null,
    options jsonb not null,
    correct_index int not null,
    active boolean not null default true
);

-- 6. Table: quiz_attempts
create table quiz_attempts (
    id serial primary key,
    governor_id text not null references roster(governor_id) on delete cascade,
    score int not null,
    question_ids jsonb not null,
    created_at timestamptz not null default now()
);

-- 7. Table: votes
create table votes (
    id serial primary key,
    voter_id text not null references roster(governor_id) on delete cascade,
    entry_id uuid not null references entries(id) on delete cascade,
    created_at timestamptz not null default now(),
    unique(voter_id, entry_id)
);

-- 8. Table: login_attempts (for rate-limiting)
create table login_attempts (
    id serial primary key,
    governor_id text not null,
    success boolean not null,
    created_at timestamptz not null default now()
);

-- 9. Table: admin_log
create table admin_log (
    id serial primary key,
    admin text not null,
    action text not null,
    target text not null,
    detail jsonb,
    created_at timestamptz not null default now()
);

-- 10. Table: settings
create table settings (
    key text primary key,
    value text not null
);

-- 11. Performance Indexes
create index idx_votes_entry_id on votes(entry_id);
create index idx_votes_voter_id on votes(voter_id);
create index idx_entries_qualified_hidden on entries(qualified, hidden);
create index idx_quiz_attempts_governor on quiz_attempts(governor_id, created_at desc);
create index idx_login_attempts_rate_limit on login_attempts(governor_id, created_at desc);

-- 12. Enable Row Level Security (RLS) on all tables
-- All app operations run server-side using service_role key, bypassing RLS.
-- No public policies means direct public API access is 100% blocked.
alter table roster enable row level security;
alter table entries enable row level security;
alter table questions enable row level security;
alter table quiz_attempts enable row level security;
alter table votes enable row level security;
alter table login_attempts enable row level security;
alter table admin_log enable row level security;
alter table settings enable row level security;

-- 13. Seed Settings
insert into settings (key, value) values
    ('submission_deadline_utc', '2026-10-29T14:00:00Z'),
    ('voting_start_utc', '2026-10-30T14:00:00Z'),
    ('voting_end_utc', '2026-10-31T14:00:00Z'),
    ('phase_override', '')
on conflict (key) do update set value = excluded.value;

-- 14. Seed Test Governor ID in Roster
insert into roster (governor_id) values ('296378532')
on conflict (governor_id) do nothing;

-- 15. Transaction-safe Voting RPC: cast_vote
create or replace function cast_vote(p_voter_id text, p_entry_id uuid)
returns json
language plpgsql
security definer
as $$
declare
    v_override text;
    v_voting_start text;
    v_voting_end text;
    v_now timestamptz := now();
    v_start_tz timestamptz;
    v_end_tz timestamptz;
    v_is_voting boolean := false;
    v_entry record;
    v_vote_count int;
begin
    -- 1. Phase Check (supports TEST_MODE phase_override)
    select value into v_override from settings where key = 'phase_override';
    if v_override is not null and v_override != '' then
        if lower(v_override) = 'voting' then
            v_is_voting := true;
        end if;
    else
        select value into v_voting_start from settings where key = 'voting_start_utc';
        select value into v_voting_end from settings where key = 'voting_end_utc';
        v_start_tz := v_voting_start::timestamptz;
        v_end_tz := v_voting_end::timestamptz;
        if v_now >= v_start_tz and v_now < v_end_tz then
            v_is_voting := true;
        end if;
    end if;

    if not v_is_voting then
        return json_build_object(
            'success', false,
            'code', 'PHASE_CLOSED',
            'message', 'Voting is not open right now. The ghosts are napping.'
        );
    end if;

    -- 2. Verify voter is in roster
    if not exists (select 1 from roster where governor_id = p_voter_id) then
        return json_build_object(
            'success', false,
            'code', 'NOT_IN_ROSTER',
            'message', 'The pond does not know you.'
        );
    end if;

    -- 3. Concurrency Protection: Acquire advisory transaction lock on voter ID
    -- Prevents race conditions from simultaneous double-taps
    perform pg_advisory_xact_lock(hashtext(p_voter_id));

    -- 4. Check entry existence and eligibility
    select id, governor_id, qualified, hidden into v_entry from entries where id = p_entry_id;
    if not found then
        return json_build_object(
            'success', false,
            'code', 'ENTRY_NOT_FOUND',
            'message', 'That costume vanished like a ghost.'
        );
    end if;

    if v_entry.hidden then
        return json_build_object(
            'success', false,
            'code', 'ENTRY_NOT_FOUND',
            'message', 'That costume vanished like a ghost.'
        );
    end if;

    if not v_entry.qualified then
        return json_build_object(
            'success', false,
            'code', 'NOT_QUALIFIED',
            'message', 'This one is just here for the vibes. No votes allowed.'
        );
    end if;

    -- 5. Anti-Self-Voting Rule
    if v_entry.governor_id = p_voter_id then
        return json_build_object(
            'success', false,
            'code', 'SELF_VOTE',
            'message', 'Voting for yourself? Nice try, little frog.'
        );
    end if;

    -- 6. Check duplicate vote for this entry
    if exists (select 1 from votes where voter_id = p_voter_id and entry_id = p_entry_id) then
        return json_build_object(
            'success', false,
            'code', 'ALREADY_VOTED',
            'message', 'You already voted for this one. Spread the love!'
        );
    end if;

    -- 7. Check 3-vote limit
    select count(*) into v_vote_count from votes where voter_id = p_voter_id;
    if v_vote_count >= 3 then
        return json_build_object(
            'success', false,
            'code', 'LIMIT_REACHED',
            'message', 'All 3 votes used! Remove one to switch.'
        );
    end if;

    -- 8. Insert vote
    insert into votes (voter_id, entry_id) values (p_voter_id, p_entry_id);

    return json_build_object(
        'success', true,
        'code', 'OK',
        'message', 'Vote cast! The ghosts nod approvingly.',
        'votes_remaining', 3 - (v_vote_count + 1)
    );
end;
$$;

-- 16. Transaction-safe Vote Removal RPC: remove_vote
create or replace function remove_vote(p_voter_id text, p_entry_id uuid)
returns json
language plpgsql
security definer
as $$
declare
    v_override text;
    v_voting_start text;
    v_voting_end text;
    v_now timestamptz := now();
    v_start_tz timestamptz;
    v_end_tz timestamptz;
    v_is_voting boolean := false;
    v_deleted int;
begin
    -- 1. Phase Check
    select value into v_override from settings where key = 'phase_override';
    if v_override is not null and v_override != '' then
        if lower(v_override) = 'voting' then
            v_is_voting := true;
        end if;
    else
        select value into v_voting_start from settings where key = 'voting_start_utc';
        select value into v_voting_end from settings where key = 'voting_end_utc';
        v_start_tz := v_voting_start::timestamptz;
        v_end_tz := v_voting_end::timestamptz;
        if v_now >= v_start_tz and v_now < v_end_tz then
            v_is_voting := true;
        end if;
    end if;

    if not v_is_voting then
        return json_build_object(
            'success', false,
            'code', 'PHASE_CLOSED',
            'message', 'Voting is not open right now. The ghosts are napping.'
        );
    end if;

    -- 2. Concurrency lock on voter
    perform pg_advisory_xact_lock(hashtext(p_voter_id));

    -- 3. Delete vote
    delete from votes where voter_id = p_voter_id and entry_id = p_entry_id;
    get diagnostics v_deleted = row_count;

    if v_deleted > 0 then
        return json_build_object(
            'success', true,
            'code', 'OK',
            'message', 'Vote removed! You have reclaimed a vote to spend.'
        );
    else
        return json_build_object(
            'success', false,
            'code', 'VOTE_NOT_FOUND',
            'message', 'You had not voted for this costume.'
        );
    end if;
end;
$$;
