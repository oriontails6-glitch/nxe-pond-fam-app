"""
Supabase client and database queries for NXE Pond Fam Halloween App.
All operations execute server-side using the SUPABASE_SERVICE_KEY, bypassing RLS.
Includes login rate-limiting, transaction-safe RPC voting, and admin audit logging.
"""
import os
import streamlit as st
from datetime import datetime, timezone, timedelta
from supabase import create_client, Client
import config

_supabase_client = None


def get_supabase_client() -> Client:
    """Returns singleton Supabase client using secrets."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    url = None
    key = None

    try:
        if "SUPABASE_URL" in st.secrets:
            url = st.secrets["SUPABASE_URL"]
        if "SUPABASE_SERVICE_KEY" in st.secrets:
            key = st.secrets["SUPABASE_SERVICE_KEY"]
    except Exception:
        pass

    if not url or not key:
        # Fallback to local .streamlit/secrets.toml if not running directly inside streamlit context
        try:
            import toml
            p = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
            if not os.path.exists(p):
                p = os.path.join(".streamlit", "secrets.toml")
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    sec = toml.load(f)
                    url = sec.get("SUPABASE_URL")
                    key = sec.get("SUPABASE_SERVICE_KEY")
        except Exception:
            pass

    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be provided in secrets!")

    _supabase_client = create_client(url, key)
    return _supabase_client


# ==========================================
# SETTINGS
# ==========================================

def get_settings() -> dict:
    """Fetches all key/value pairs from settings table."""
    try:
        client = get_supabase_client()
        res = client.table("settings").select("*").execute()
        return {r["key"]: r["value"] for r in (res.data or [])}
    except Exception as e:
        return {
            "submission_deadline_utc": "2026-10-29T14:00:00Z",
            "voting_start_utc": "2026-10-30T14:00:00Z",
            "voting_end_utc": "2026-10-31T14:00:00Z",
            "phase_override": ""
        }


# ==========================================
# ROSTER & LOGIN RATE LIMITING
# ==========================================

def is_governor_in_roster(governor_id: str) -> bool:
    """Checks if governor ID exists in the approved roster."""
    client = get_supabase_client()
    res = client.table("roster").select("governor_id").eq("governor_id", governor_id.strip()).execute()
    return len(res.data or []) > 0


def check_login_rate_limit(governor_id: str) -> tuple[bool, int]:
    """
    Checks if governor ID has exceeded 5 failed attempts in the last 10 minutes.
    Returns (allowed, cooldown_seconds_left).
    """
    client = get_supabase_client()
    ten_mins_ago = (datetime.now(timezone.utc) - timedelta(minutes=config.LOGIN_LOCKOUT_MINUTES)).isoformat()
    res = (
        client.table("login_attempts")
        .select("created_at")
        .eq("governor_id", governor_id)
        .eq("success", False)
        .gte("created_at", ten_mins_ago)
        .order("created_at", desc=True)
        .execute()
    )

    failures = res.data or []
    if len(failures) >= config.LOGIN_MAX_FAILED_ATTEMPTS:
        # Calculate remaining cooldown
        newest_fail = datetime.fromisoformat(failures[0]["created_at"].replace("Z", "+00:00"))
        unlock_time = newest_fail + timedelta(minutes=config.LOGIN_LOCKOUT_MINUTES)
        now_utc = datetime.now(timezone.utc)
        remaining = int((unlock_time - now_utc).total_seconds())
        return False, max(0, remaining)

    return True, 0


def record_login_attempt(governor_id: str, success: bool):
    """Records a login attempt for audit and rate-limiting."""
    try:
        client = get_supabase_client()
        client.table("login_attempts").insert({
            "governor_id": governor_id,
            "success": success
        }).execute()
    except Exception:
        pass


def add_roster_ids(id_list: list[str]) -> tuple[int, int, int]:
    """
    Adds multiple governor IDs to the roster.
    Returns (added_count, duplicate_count, invalid_count).
    """
    client = get_supabase_client()
    existing_res = client.table("roster").select("governor_id").execute()
    existing_ids = {r["governor_id"] for r in (existing_res.data or [])}

    added = 0
    duplicates = 0
    invalid = 0

    to_insert = []
    seen_in_batch = set()

    for raw in id_list:
        clean = raw.strip()
        if not clean:
            continue
        if not clean.isdigit() or len(clean) > 20:
            invalid += 1
            continue
        if clean in existing_ids or clean in seen_in_batch:
            duplicates += 1
            continue

        seen_in_batch.add(clean)
        to_insert.append({"governor_id": clean})

    if to_insert:
        client.table("roster").insert(to_insert).execute()
        added = len(to_insert)

    return added, duplicates, invalid


def remove_roster_id(governor_id: str) -> bool:
    """Removes a governor ID from the roster."""
    client = get_supabase_client()
    client.table("roster").delete().eq("governor_id", governor_id).execute()
    return True


def get_roster_overview() -> list[dict]:
    """Returns all roster IDs with added timestamps."""
    client = get_supabase_client()
    res = client.table("roster").select("*").order("added_at", desc=True).execute()
    return res.data or []


# ==========================================
# TRIVIA QUIZ
# ==========================================

def get_active_questions() -> list[dict]:
    """Retrieves all active trivia questions from the database."""
    client = get_supabase_client()
    res = client.table("questions").select("id, text, options, correct_index").eq("active", True).execute()
    return res.data or []


def get_quiz_attempts(governor_id: str) -> list[dict]:
    """Retrieves quiz attempts for a governor ID ordered by newest first."""
    client = get_supabase_client()
    res = (
        client.table("quiz_attempts")
        .select("*")
        .eq("governor_id", governor_id)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []


def record_quiz_attempt(governor_id: str, score: int, question_ids: list[int]):
    """Records a completed quiz attempt."""
    client = get_supabase_client()
    client.table("quiz_attempts").insert({
        "governor_id": governor_id,
        "score": score,
        "question_ids": question_ids
    }).execute()


# ==========================================
# SUBMISSIONS & ENTRIES
# ==========================================

def get_entry_by_governor(governor_id: str) -> dict | None:
    """Fetches an entry by governor ID."""
    client = get_supabase_client()
    res = client.table("entries").select("*").eq("governor_id", governor_id).execute()
    if res.data:
        return res.data[0]
    return None


def upsert_entry(
    governor_id: str,
    ingame_name: str,
    backstory: str,
    image_path: str,
    thumb_path: str,
    quiz_score: int,
    qualified: bool
) -> dict:
    """Creates or updates a costume entry for the governor."""
    client = get_supabase_client()
    existing = get_entry_by_governor(governor_id)

    payload = {
        "governor_id": governor_id,
        "ingame_name": ingame_name,
        "backstory": backstory,
        "image_path": image_path,
        "thumb_path": thumb_path,
        "quiz_score": quiz_score,
        "qualified": qualified,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    if existing:
        res = client.table("entries").update(payload).eq("id", existing["id"]).execute()
        return res.data[0]
    else:
        payload["created_at"] = datetime.now(timezone.utc).isoformat()
        res = client.table("entries").insert(payload).execute()
        return res.data[0]


def update_entry_quiz_status(governor_id: str, best_score: int, qualified: bool):
    """Updates the quiz score and qualified flag on an existing entry."""
    client = get_supabase_client()
    client.table("entries").update({
        "quiz_score": best_score,
        "qualified": qualified,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }).eq("governor_id", governor_id).execute()


# ==========================================
# GALLERY & VOTING (ANONYMOUS & TRANSACTION-SAFE)
# ==========================================

def get_public_gallery_entries() -> list[dict]:
    """
    Fetches all non-hidden entries for the anonymous gallery.
    Includes governor_id internally for server-side exhibition/voting rules.
    """
    client = get_supabase_client()
    res = (
        client.table("entries")
        .select("id, governor_id, image_path, thumb_path, backstory, qualified, created_at")
        .eq("hidden", False)
        .order("created_at", desc=False)
        .execute()
    )
    return res.data or []


def get_voter_cast_votes(voter_id: str) -> list[str]:
    """Returns list of entry IDs the voter has voted for."""
    client = get_supabase_client()
    res = client.table("votes").select("entry_id").eq("voter_id", voter_id).execute()
    return [r["entry_id"] for r in (res.data or [])]


def cast_vote(voter_id: str, entry_id: str) -> dict:
    """Calls the PostgreSQL RPC function cast_vote for atomic concurrency-safe voting."""
    client = get_supabase_client()

    # Rule: Specific governor 409716271 is an exhibition-only entry that cannot receive votes
    chk = client.table("entries").select("governor_id").eq("id", entry_id).execute()
    if chk.data and chk.data[0].get("governor_id") == "409716271":
        return {"success": False, "message": "This costume is an exhibition entry and is not eligible for community voting."}

    res = client.rpc("cast_vote", {"p_voter_id": voter_id, "p_entry_id": entry_id}).execute()
    return res.data


def remove_vote(voter_id: str, entry_id: str) -> dict:
    """Calls the PostgreSQL RPC function remove_vote to reclaim a vote."""
    client = get_supabase_client()
    res = client.rpc("remove_vote", {"p_voter_id": voter_id, "p_entry_id": entry_id}).execute()
    return res.data


# ==========================================
# LEADERBOARD (PHASE 4 ONLY)
# ==========================================

def get_leaderboard() -> list[dict]:
    """
    Computes leaderboard ranking from votes table for qualified, non-hidden entries.
    Reveals winner's in-game name and avatar image!
    Handles ties by assigning shared ranks.
    Exhibition entry (409716271) is excluded from competitive podium prize rankings.
    """
    client = get_supabase_client()
    entries_res = (
        client.table("entries")
        .select("id, governor_id, ingame_name, image_path, thumb_path, backstory, created_at")
        .eq("hidden", False)
        .execute()
    )
    raw_entries = entries_res.data or []
    entries = [e for e in raw_entries if e.get("governor_id") != "409716271"]

    # Get vote counts
    votes_res = client.table("votes").select("entry_id").execute()
    vote_counts = {}
    for v in (votes_res.data or []):
        eid = v["entry_id"]
        vote_counts[eid] = vote_counts.get(eid, 0) + 1

    for e in entries:
        e["votes"] = vote_counts.get(e["id"], 0)

    # Sort primarily by votes (descending), then by created_at (ascending)
    entries.sort(key=lambda x: (-x["votes"], x["created_at"]))

    # Assign shared ranks for ties
    current_rank = 1
    for i, entry in enumerate(entries):
        if i > 0 and entry["votes"] == entries[i - 1]["votes"]:
            entry["rank"] = entries[i - 1]["rank"]
        else:
            entry["rank"] = current_rank
        current_rank += 1

    return entries


# ==========================================
# ADMIN & AUDIT
# ==========================================

def get_all_entries_admin() -> list[dict]:
    """Retrieves all entries (including hidden and non-qualified) with full identities for admin audit."""
    client = get_supabase_client()
    res = client.table("entries").select("*").order("created_at", desc=True).execute()
    return res.data or []


def set_entry_hidden_admin(entry_id: str, hidden: bool, admin: str, reason: str):
    """Hides or restores an entry and logs the action."""
    client = get_supabase_client()
    client.table("entries").update({
        "hidden": hidden,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", entry_id).execute()

    action = "HIDE_ENTRY" if hidden else "RESTORE_ENTRY"
    log_admin_action(admin, action, f"entry:{entry_id}", {"reason": reason})


def log_admin_action(admin: str, action: str, target: str, detail: dict):
    """Appends an event to the admin_log table."""
    try:
        client = get_supabase_client()
        client.table("admin_log").insert({
            "admin": admin,
            "action": action,
            "target": target,
            "detail": detail
        }).execute()
    except Exception:
        pass


def get_all_votes_admin() -> list[dict]:
    """Fetches all votes with timestamps for audit."""
    client = get_supabase_client()
    res = client.table("votes").select("id, voter_id, entry_id, created_at").order("created_at", desc=True).execute()
    return res.data or []


def void_vote_admin(vote_id: int, admin: str, reason: str):
    """Voids a suspicious vote and logs the action."""
    client = get_supabase_client()
    client.table("votes").delete().eq("id", vote_id).execute()
    log_admin_action(admin, "VOID_VOTE", f"vote:{vote_id}", {"reason": reason})


def update_setting_admin(key: str, value: str, admin: str):
    """Updates a settings row and logs the action."""
    client = get_supabase_client()
    client.table("settings").upsert({"key": key, "value": value}).execute()
    log_admin_action(admin, "UPDATE_SETTING", f"setting:{key}", {"new_value": value})


def get_admin_logs() -> list[dict]:
    """Fetches audit logs."""
    client = get_supabase_client()
    res = client.table("admin_log").select("*").order("created_at", desc=True).limit(100).execute()
    return res.data or []
