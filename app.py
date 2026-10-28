"""
NXE Pond Fam: Spooky Halloween Avatar & Costume Competition App
Main Application Entrypoint, Navigation, and Seamless Automatic Progression.
Built for King Shot Alliance NXE.
"""
import os
import hmac
import hashlib
import random
import streamlit as st
from datetime import datetime, timezone, timedelta

# 1. Page Configuration (Centered mobile-first layout)
st.set_page_config(
    page_title="NXE Pond Fam Spooky Halloween",
    page_icon="🎃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Core imports
import config
from styles import get_css, get_floating_ghosts_html, get_storybook_header_svg
from sponsor_config import (
    SPONSOR_NAME, SPONSOR_TITLE, SPONSOR_SUBTITLE, SPONSOR_IMAGE, SPONSOR_IMAGE_FALLBACK,
    ORGANIZERS_NAME, ORGANIZERS_TITLE, ORGANIZERS_SUBTITLE, ORGANIZERS_IMAGE, ORGANIZERS_IMAGE_FALLBACK,
    TOURNAMENT_PRIZES, PAPA_MO_QUOTES, TWINNS_QUOTES, get_image_base64_data_uri
)
from phases import CompetitionPhase, evaluate_phase, format_utc_display
from db import (
    get_settings,
    is_governor_in_roster,
    check_login_rate_limit,
    record_login_attempt,
    get_entry_by_governor,
    get_quiz_attempts
)
from quiz import render_quiz
from submit import render_submit
from gallery import render_gallery
from leaderboard import render_leaderboard
from admin import render_admin

# 2. Inject Responsive Styles & Floating Pumpkins/Ghosts
st.markdown(get_css(config.THEME), unsafe_allow_html=True)
st.markdown(get_floating_ghosts_html(), unsafe_allow_html=True)


# ==========================================
# SESSION TOKEN HANDLING (HMAC SIGNED FOR MOBILE RELOAD)
# ==========================================

def get_session_secret() -> str:
    try:
        if "SESSION_SECRET" in st.secrets:
            return str(st.secrets["SESSION_SECRET"]).strip()
    except Exception:
        pass
    return "nxe-pond-secret-fallback-token-signing-key"


def generate_session_token(governor_id: str) -> str:
    """Generates an HMAC-SHA256 signed session token with 24-hour expiry."""
    expiry = int((datetime.now(timezone.utc) + timedelta(hours=config.SESSION_TOKEN_EXPIRY_HOURS)).timestamp())
    payload = f"{governor_id}:{expiry}"
    sig = hmac.new(get_session_secret().encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def verify_session_token(token: str) -> str | None:
    """Verifies HMAC signature and expiry. Returns governor_id if valid."""
    if not token or ":" not in token:
        return None
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return None
        gid, exp_str, sig = parts
        expiry = int(exp_str)
        now_ts = int(datetime.now(timezone.utc).timestamp())
        if now_ts > expiry:
            return None
        payload = f"{gid}:{exp_str}"
        expected_sig = hmac.new(get_session_secret().encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected_sig, sig):
            return gid
    except Exception:
        pass
    return None


# 3. Session State & Navigation Initialization
if "user_gid" not in st.session_state:
    st.session_state.user_gid = None

if "active_screen" not in st.session_state:
    st.session_state.active_screen = "login"

if "joke_idx" not in st.session_state:
    st.session_state.joke_idx = random.randint(0, 15)

# Check query params for persistent mobile login token
q_params = st.query_params
token_in_url = q_params.get("session")

if token_in_url and not st.session_state.user_gid:
    verified_gid = verify_session_token(token_in_url)
    if verified_gid and is_governor_in_roster(verified_gid):
        st.session_state.user_gid = verified_gid

# Check if admin route requested or active screen is admin_sanctum
is_admin_route = (q_params.get("page") == "admin") or (st.session_state.active_screen == "admin_sanctum")

# 4. Phase Evaluation
settings = get_settings()
test_mode = False
try:
    test_mode = bool(st.secrets.get("TEST_MODE", False))
except Exception:
    pass

current_phase, phase_info = evaluate_phase(settings, test_mode=test_mode)

# Sidebar Test Mode Phase Switcher (Visible ONLY when TEST_MODE=true)
if test_mode:
    with st.sidebar:
        st.markdown("### 🧪 Test Mode Phase Switcher")
        st.caption("Change phase instantly to preview Gallery and Podium:")
        curr_override = settings.get("phase_override", "").strip().lower()
        st.info(f"Active Mode: **{curr_override.upper() or 'REAL SCHEDULE'}**")

        if st.button("👻 Preview Phase 3: Voting (Gallery)", key="tb_vote_btn"):
            from db import update_setting_admin
            update_setting_admin("phase_override", "voting", "test_controller")
            st.session_state.active_screen = "gallery"
            st.rerun()

        if st.button("🏆 Preview Phase 4: Results (Podium)", key="tb_res_btn"):
            from db import update_setting_admin
            update_setting_admin("phase_override", "results", "test_controller")
            st.session_state.active_screen = "leaderboard"
            st.rerun()

        if st.button("⏱️ Reset to Real Clock (Phase 1 Submissions)", key="tb_reset_btn"):
            from db import update_setting_admin
            update_setting_admin("phase_override", "", "test_controller")
            st.session_state.active_screen = "home"
            st.rerun()


# ==========================================
# ADMIN ROUTE (HIDDEN FROM CONTESTANTS)
# ==========================================
if is_admin_route:
    col_ab1, col_ab2 = st.columns([3, 1])
    with col_ab2:
        if st.button("⬅️ Return to App", key="admin_back_btn"):
            if "page" in st.query_params:
                del st.query_params["page"]
            st.session_state.active_screen = "login" if not st.session_state.user_gid else "quiz"
            st.rerun()
    render_admin(test_mode=test_mode)
    st.stop()


# ==========================================
# COZY STORYBOOK HERO HEADER (Pinterest Inspo 4 & 5)
# ==========================================
st.markdown(f"""<div class="storybook-hero-card">
{get_storybook_header_svg()}
<div class="storybook-title">NXE POND FAM</div>
<div class="storybook-subtitle">Spooky Halloween Avatar & Costume Championship</div>
<div class="storybook-badge">👑 King Shot Alliance NXE</div>
</div>""", unsafe_allow_html=True)

# Phase Banner with Live UTC Countdown
banner_color = current_phase.badge_color
phase_tag = f'<span class="phase-badge" style="background-color: {banner_color}; color: #070C18;">{current_phase.label}</span>'
server_clock_str = phase_info.get("server_utc_str", "UTC")

if phase_info["target_time"]:
    target_str = format_utc_display(phase_info["target_time"])
    countdown_display = f'<div style="margin-top: 6px;"><div style="color: var(--text-secondary); font-size: 0.88rem;">🕒 Server Clock: <strong style="color: #FFFFFF;">{server_clock_str}</strong></div><div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-top: 4px;"><span style="color: var(--text-secondary); font-size: 0.9rem;">{phase_info["target_label"]}: <strong style="color: #FFFFFF;">{target_str}</strong></span><span style="font-family: \'Fredoka\', sans-serif; font-size: 1.15rem; color: #FBBF24; font-weight: 700;">⏳ {phase_info["countdown_str"]}</span></div></div>'
else:
    countdown_display = f'<div style="margin-top: 6px;"><div style="color: var(--text-secondary); font-size: 0.88rem;">🕒 Server Clock: <strong style="color: #FFFFFF;">{server_clock_str}</strong></div><div style="color: #34D399; font-weight: 700; margin-top: 4px;">🏆 Competition Concluded! Check the Champion Podium!</div></div>'

banner_html = f'<div class="phase-banner"><div>{phase_tag}</div>{countdown_display}</div>'
st.markdown(banner_html, unsafe_allow_html=True)


# ==========================================
# SPOOKY DAD JOKES REPOSITORY
# ==========================================
DAD_JOKES = [
    ("Why don't skeletons fight each other in the pond?", "They don't have the guts! 💀🤣"),
    ("What is a duck's favorite Halloween candy?", "Quacker Jacks! 🦆🍿"),
    ("Why did the scarecrow win a Nobel Prize?", "Because he was outstanding in his field! 🌾🎃"),
    ("What kind of music do pond fish listen to on Halloween?", "Something with a good bass line! 🐟🎸"),
    ("What did the baby dragon say when he coughed?", "'Oops, excuse my spark!' 🐉🔥"),
    ("Why do mummies have trouble making friends?", "Because they are too wrapped up in themselves! 🧟‍♂️"),
    ("What do you call a duck that does magic tricks?", "A Flying Sorcerer! 🦆✨"),
    ("How do vampires get around the haunted pond?", "In blood vessels! 🧛🛶"),
    ("What is a ghost's favorite dessert?", "I-scream with extra booberries! 👻🍦"),
    ("Why did the vampire visit the pond doctor?", "Because he was coffin too much! 🧛‍♂️🤧"),
    ("What is a witch's favorite subject in school?", "Spelling! 🧙‍♀️📖"),
    ("Why don't dragons eat clowns?", "Because they taste funny! 🐉🤡"),
    ("What happens when a ghost gets lost in the pond fog?", "He is truly mist! 🌫️👻"),
    ("Why do ducks have feathers?", "To cover their butt-quacks! 🦆😂"),
    ("Where do ghosts go shopping for groceries?", "At the ghost-ery store! 🥛👻"),
    ("What is a goblin's favorite cheese?", "Monster-ella! 🧀👺")
]


def render_dad_joke_card():
    idx = st.session_state.get("joke_idx", 0) % len(DAD_JOKES)
    q, a = DAD_JOKES[idx]
    st.markdown("---")
    st.markdown(f"""<div class="pond-card" style="text-align: center; border: 1px solid #7C3AED; background: linear-gradient(180deg, #240E3E 0%, #170929 100%); padding: 1.1rem;">
<div style="font-size: 1.4rem; margin-bottom: 0.3rem;">🦆 🎃 🐉</div>
<div style="font-size: 0.82rem; font-weight: 700; color: #A78BFA; text-transform: uppercase; letter-spacing: 1px;">Spooky Pond Dad Joke</div>
<div style="font-family: 'Fredoka', sans-serif; font-size: 1.1rem; color: #FDE047; margin: 0.5rem 0 0.2rem 0;">"{q}"</div>
<div style="font-size: 1rem; color: #FFFFFF; font-weight: 600;">👉 {a}</div>
</div>""", unsafe_allow_html=True)
    col_j1, col_j2, col_j3 = st.columns([1, 2, 1])
    with col_j2:
        if st.button("🎲 Tell Me Another Joke!", key="roll_dad_joke_btn"):
            st.session_state.joke_idx = (idx + 1) % len(DAD_JOKES)
            st.rerun()


def render_home_showcase_carousel():
    """Renders the consolidated 4-tab interactive carousel containing Prizes, Sponsor, Organizers, and Guidelines."""
    st.markdown('<div style="text-align: center; margin: 1.4rem 0 0.6rem 0;"><span style="font-family: \'Fredoka\', sans-serif; font-size: 1.15rem; color: #FBBF24; font-weight: 700;">✨ Tournament Lore, Prizes & Benefactors ✨</span></div>', unsafe_allow_html=True)

    t_prizes, t_sponsor, t_organizers, t_guide = st.tabs([
        "🏆 Rewards",
        "👑 Papa Mo (Sponsor)",
        "👻 Ghost Twinns",
        "📜 Guidelines"
    ])

    with t_prizes:
        prizes_html = "".join([
            f"""<div class="prize-item" style="border-left: 4px solid {p['color']};">
                <span style="background: rgba(255,255,255,0.1); color: {p['color']}; font-family: 'Fredoka', sans-serif; font-size: 0.78rem; font-weight: 700; padding: 2px 10px; border-radius: 9999px;">{p['rank']}</span>
                <div class="prize-title" style="color: {p['color']};">{p['title']}</div>
                <p class="prize-desc">{p['desc']}</p>
            </div>""" for p in TOURNAMENT_PRIZES
        ])
        st.markdown(f"""<div class="pond-card" style="padding-bottom: 0.5rem;">
<div style="font-family: 'Fredoka', sans-serif; font-size: 1.25rem; color: #FBBF24; margin-bottom: 0.6rem; text-align: center;">🏆 Official Tournament Rewards</div>
<div style="text-align: center; color: #DDD6FE; font-size: 0.88rem; margin-bottom: 1rem;">Funded directly from the royal treasury of <strong>Papa Mo</strong>!</div>
{prizes_html}
</div>""", unsafe_allow_html=True)

    with t_sponsor:
        if "papamo_idx" not in st.session_state:
            st.session_state.papamo_idx = random.randint(0, len(PAPA_MO_QUOTES) - 1)
        idx_p = st.session_state.papamo_idx % len(PAPA_MO_QUOTES)
        p_quote = PAPA_MO_QUOTES[idx_p]

        sponsor_uri = get_image_base64_data_uri(SPONSOR_IMAGE) or get_image_base64_data_uri(SPONSOR_IMAGE_FALLBACK)
        img_sponsor_html = f'<img src="{sponsor_uri}" class="brand-banner-img" alt="Papa Mo Sponsor" />' if sponsor_uri else '<div style="font-size: 2.3rem; margin: 0.15rem 0;">👑 🦆 👑</div>'

        st.markdown(f"""<div class="papamo-sponsor-card">
<div class="papamo-badge">👑 OFFICIAL TOURNAMENT SPONSOR 👑</div>
{img_sponsor_html}
<div class="papamo-title">PAPA MO'S ROYAL POND PATRONAGE</div>
<div style="font-size: 0.9rem; color: #FDE68A; font-weight: 600; margin-bottom: 0.2rem;">{SPONSOR_TITLE}</div>
<div style="font-size: 0.82rem; color: #DDD6FE; margin-bottom: 0.7rem;">{SPONSOR_SUBTITLE}</div>
<div class="papamo-quote-box">
"{p_quote}"
</div>
</div>""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🎲 Papa Mo's Wisdom", key="papamo_carousel_refresh"):
                st.session_state.papamo_idx = (idx_p + 1) % len(PAPA_MO_QUOTES)
                st.rerun()

    with t_organizers:
        if "twinns_idx" not in st.session_state:
            st.session_state.twinns_idx = random.randint(0, len(TWINNS_QUOTES) - 1)
        idx_t = st.session_state.twinns_idx % len(TWINNS_QUOTES)
        t_quote = TWINNS_QUOTES[idx_t]

        org_uri = get_image_base64_data_uri(ORGANIZERS_IMAGE) or get_image_base64_data_uri(ORGANIZERS_IMAGE_FALLBACK)
        img_org_html = f'<img src="{org_uri}" class="brand-banner-img" alt="The Ghost Twinns: Orion & Nobu" />' if org_uri else '<div style="font-size: 2.3rem; margin: 0.15rem 0;">👻 👻 🪷</div>'

        st.markdown(f"""<div class="organizers-card">
<div class="organizers-badge">👻 TOURNAMENT ORGANIZERS 👻</div>
{img_org_html}
<div style="font-family: 'Fredoka', sans-serif; font-size: 1.35rem; font-weight: 700; color: #E9D5FF; margin: 0.2rem 0;">{ORGANIZERS_NAME}</div>
<div style="font-size: 0.9rem; color: #DDD6FE; font-weight: 600; margin-bottom: 0.2rem;">{ORGANIZERS_TITLE}</div>
<div style="font-size: 0.82rem; color: #C084FC; margin-bottom: 0.6rem;">{ORGANIZERS_SUBTITLE}</div>
<div class="papamo-quote-box" style="border-left-color: #C084FC;">
"{t_quote}"
</div>
</div>""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🎲 Twinns Ghost Wisdom", key="twinns_carousel_refresh"):
                st.session_state.twinns_idx = (idx_t + 1) % len(TWINNS_QUOTES)
                st.rerun()

    with t_guide:
        st.markdown("""<div class="pond-card" style="text-align: left;">
<div style="font-family: 'Fredoka', sans-serif; font-size: 1.25rem; color: #FBBF24; margin-bottom: 0.8rem; text-align: center;">📜 Tournament Guidelines & How to Win</div>
<div style="margin-bottom: 0.85rem;">
    <strong style="color: #FDE047; font-size: 0.96rem;">1. 🧠 Step 1: Pass the 5-Question Lore Quiz</strong>
    <p style="color: #DDD6FE; font-size: 0.88rem; margin: 3px 0 0 0; line-height: 1.45;">Score 4+ out of 5 to earn the 👑 Qualified Contestant status. (Scored below 4? You still compete in the fun Honorary Vibes tier!).</p>
</div>
<div style="margin-bottom: 0.85rem;">
    <strong style="color: #FDE047; font-size: 0.96rem;">2. 🎨 Step 2: Upload Avatar & Spooky Backstory</strong>
    <p style="color: #DDD6FE; font-size: 0.88rem; margin: 3px 0 0 0; line-height: 1.45;">Upload your in-game Halloween avatar screenshot and write the story or joke behind your costume. Mobile-optimized for landscape & portrait screenshots.</p>
</div>
<div style="margin-bottom: 0.85rem;">
    <strong style="color: #FDE047; font-size: 0.96rem;">3. 🗳️ Step 3: Vote for Your 3 Favorites</strong>
    <p style="color: #DDD6FE; font-size: 0.88rem; margin: 3px 0 0 0; line-height: 1.45;">During the live voting round, every verified governor gets exactly 3 votes. Tap any costume card in the gallery to expand its story and cast your votes!</p>
</div>
<div>
    <strong style="color: #FDE047; font-size: 0.96rem;">4. 🏆 Step 4: Claim Podium Glory & Riches</strong>
    <p style="color: #DDD6FE; font-size: 0.88rem; margin: 3px 0 0 0; line-height: 1.45;">When voting concludes, the automated podium crowns the champions! 1st takes the Month Card, 2nd commands the alliance for 24h (except Papa Mo!), and 3rd feasts on 150M RSS at Orion's Pax.</p>
</div>
</div>""", unsafe_allow_html=True)


def render_quick_officer_portal():
    """In-app Officer & Co-Admin Quick Portal for 1-tap Governor ID additions right on mobile."""
    with st.expander("🛡️ Alliance Officer & Co-Admin Portal (Add IDs On Mobile)", expanded=bool(st.session_state.get("admin_logged_user"))):
        admin_user = st.session_state.get("admin_logged_user")

        if not admin_user:
            st.caption("Are you an NXE alliance officer? Log in here to approve Governor IDs directly on your phone — no PC, terminal, or git required!")
            with st.form("quick_officer_login_form"):
                c_u, c_p = st.columns(2)
                with c_u:
                    u_in = st.text_input("Officer Username", placeholder="e.g. admin1")
                with c_p:
                    p_in = st.text_input("Officer Passkey", type="password")
                adm_btn = st.form_submit_button("🔓 Unlock Officer Tools")

                if adm_btn:
                    from admin import verify_admin_credentials
                    if verify_admin_credentials(u_in.strip(), p_in.strip()):
                        st.session_state.admin_logged_user = u_in.strip()
                        st.success(f"Welcome Officer {u_in.strip()}! Roster tools unlocked.")
                        st.rerun()
                    else:
                        st.error("Invalid officer credentials.")
        else:
            c_top1, c_top2 = st.columns([3, 1])
            with c_top1:
                st.success(f"🛡️ Officer Active: **`{admin_user}`**")
            with c_top2:
                if st.button("🚪 Logout Officer", key="quick_adm_logout"):
                    st.session_state.admin_logged_user = None
                    st.rerun()

            st.markdown("#### ⚡ 1-Tap Add Governor ID")
            st.caption("Quickly approve an alliance member so they can log in right now:")
            c_gid, c_btn = st.columns([2, 1])
            with c_gid:
                new_gid = st.text_input("Governor ID (digits only)", placeholder="e.g. 296378532", key="quick_add_gid_input")
            with c_btn:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                add_now = st.button("➕ Approve ID", key="quick_add_gid_btn")

            if add_now:
                clean_id = (new_gid or "").strip()
                if not clean_id.isdigit():
                    st.error("Governor ID must be numeric digits only.")
                else:
                    from db import add_roster_ids
                    added, dupes, inv = add_roster_ids([clean_id])
                    if added > 0:
                        st.success(f"🎉 Governor ID `{clean_id}` is now approved! They can log in immediately.")
                    elif dupes > 0:
                        st.info(f"ℹ️ Governor ID `{clean_id}` is ALREADY approved in the roster.")
                    else:
                        st.warning("Could not add ID. Please check format.")

            st.markdown("---")
            col_full1, col_full2 = st.columns(2)
            with col_full1:
                if st.button("🏛️ Open Full Council Admin Sanctum", key="open_full_sanctum_btn"):
                    st.session_state.active_screen = "admin_sanctum"
                    st.rerun()
            with col_full2:
                st.caption("Manage submissions, audit community votes, edit phase schedule, and export CSV.")


# ==========================================
# FLOW CONTROL: LOGGED IN VS LOGGED OUT
# ==========================================
user_gid = st.session_state.user_gid

if not user_gid:
    # GUEST & LOGIN VIEW (NO CLUTTERED TABS)
    st.subheader("🔑 Contestant Login")
    st.caption("Enter your King Shot Governor ID and secret alliance join code to compete:")

    with st.form("login_form"):
        gov_in = st.text_input("Governor ID (digits only)", max_chars=20, placeholder="e.g. 296378532")
        join_in = st.text_input("Alliance Secret Quack (Join Code)", type="password", placeholder="From alliance chat")
        login_btn = st.form_submit_button("🎃 Enter the Haunted Pond!")

        if login_btn:
            clean_gid = (gov_in or "").strip()
            clean_join = (join_in or "").strip()

            if not clean_gid.isdigit():
                st.error("Please enter your numeric Governor ID (digits only).")
            else:
                allowed, cooldown_secs = check_login_rate_limit(clean_gid)
                if not allowed:
                    st.error(f"🦇 Too many wrong attempts! Try again in {cooldown_secs} seconds.")
                else:
                    expected_join = st.secrets.get("JOIN_CODE", "NXEHALLOWEEN2026").strip().lower()
                    if clean_join.lower() != expected_join:
                        record_login_attempt(clean_gid, False)
                        st.error("That is not the secret quack! Ask an NXE officer in alliance chat.")
                    elif not is_governor_in_roster(clean_gid):
                        record_login_attempt(clean_gid, False)
                        st.error("Governor ID not found in the alliance roster! Ask an officer to add you.")
                    else:
                        record_login_attempt(clean_gid, True)
                        st.session_state.user_gid = clean_gid
                        token = generate_session_token(clean_gid)
                        st.query_params["session"] = token

                        # Route to exact required step
                        attempts = get_quiz_attempts(clean_gid)
                        entry = get_entry_by_governor(clean_gid)
                        if not attempts:
                            st.session_state.active_screen = "quiz"
                        elif not entry:
                            st.session_state.active_screen = "submit"
                        else:
                            st.session_state.active_screen = "gallery"
                        st.balloons()
                        st.rerun()

    # Guest link if voting or results open
    if current_phase in (CompetitionPhase.VOTING, CompetitionPhase.RESULTS):
        st.markdown("")
        if st.button("👀 Just browsing? View Costume Gallery as Guest ➡️", key="guest_gal_btn"):
            st.session_state.active_screen = "gallery"
            st.session_state.user_gid = "guest"
            st.rerun()

    # Officer & Co-Admin Quick Portal (1-Tap Governor ID Add right on mobile)
    render_quick_officer_portal()

    # Unified Home Carousel: Prizes, Papa Mo, Ghost Twinns, Guidelines
    render_home_showcase_carousel()

    # Spooky dad joke
    render_dad_joke_card()

else:
    # LOGGED IN VIEW: STREAMLINED STEP PROGRESSION
    # 1. Compact User Bar
    col_u1, col_u2 = st.columns([3, 1])
    with col_u1:
        st.markdown(f"🧙 Contestant: **Governor `{user_gid}`**")
    with col_u2:
        if st.button("🚪 Logout", key="user_logout_btn"):
            st.session_state.user_gid = None
            st.session_state.active_screen = "login"
            if "session" in st.query_params:
                del st.query_params["session"]
            st.rerun()

    # 2. Clean 5-Step Minimal Navigation Stepper
    if st.session_state.active_screen in ("login",):
        attempts = get_quiz_attempts(user_gid)
        entry = get_entry_by_governor(user_gid)
        if not attempts:
            st.session_state.active_screen = "quiz"
        elif not entry:
            st.session_state.active_screen = "submit"
        else:
            st.session_state.active_screen = "gallery"

    steps = [
        ("home", "📜 Prizes"),
        ("quiz", "🧠 Quiz"),
        ("submit", "🎨 Costume"),
        ("gallery", "👻 Gallery"),
        ("leaderboard", "🏆 Podium")
    ]

    step_cols = st.columns(5)
    for i, (s_key, s_label) in enumerate(steps):
        with step_cols[i]:
            is_active = (st.session_state.active_screen == s_key)
            lbl = f"⭐ {s_label}" if is_active else s_label
            if st.button(lbl, key=f"step_btn_{s_key}"):
                st.session_state.active_screen = s_key
                st.rerun()

    st.markdown("---")

    # 3. Active Screen View (Focused, Clean & Uncluttered)
    curr = st.session_state.active_screen

    if curr == "home":
        render_home_showcase_carousel()
    elif curr == "quiz":
        render_quiz(user_gid, current_phase)
    elif curr == "submit":
        render_submit(user_gid, current_phase)
    elif curr == "gallery":
        render_gallery(user_gid, current_phase)
    elif curr == "leaderboard":
        render_leaderboard(current_phase, phase_info.get("voting_end"))
    else:
        render_quiz(user_gid, current_phase)

    # 4. Spooky Dad Joke at bottom
    render_dad_joke_card()


# ==========================================
# SPOOKY HALLOWEEN FOOTER
# ==========================================
st.markdown("---")
st.markdown('<div style="text-align: center; color: var(--text-secondary); font-size: 0.9rem; padding: 1rem 0;">🎃 <strong>NXE Pond Fam Halloween</strong> • May Your Pumpkins Glow & Your Ducks Quack Forever! 🦆👻🦇</div>', unsafe_allow_html=True)
