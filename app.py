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
from styles import get_css, get_floating_ghosts_html
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

# Check if admin route requested
is_admin_route = (q_params.get("page") == "admin")

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
    render_admin(test_mode=test_mode)
    st.stop()


# ==========================================
# SPOOKY HALLOWEEN HERO HEADER
# ==========================================
st.markdown("""<div class="vector-halloween-hero">
<div class="hero-full-moon"></div>
<div class="hero-title-box">
<h1 class="hero-halloween-title">🎃 NXE POND FAM 🎃</h1>
<div style="font-family: 'Fredoka', sans-serif; font-size: 1.15rem; font-weight: 700; color: #FFE082; text-shadow: 0 2px 4px rgba(0,0,0,0.5); margin: 0.35rem 0;">
Spooky Halloween Avatar & Costume Championship
</div>
<div class="hero-sub-badge">👑 King Shot Alliance NXE</div>
</div>
</div>
<div class="creature-strip">
<div style="text-align: center;"><span style="font-size: 1.8rem;">🦆</span><div style="font-size: 0.75rem; font-weight: 700; color: #FFD000;">Witchy Duck</div></div>
<div style="text-align: center;"><span style="font-size: 1.8rem;">🐉</span><div style="font-size: 0.75rem; font-weight: 700; color: #C77DFF;">Baby Dragon</div></div>
<div style="text-align: center;"><span style="font-size: 1.8rem;">🐟</span><div style="font-size: 0.75rem; font-weight: 700; color: #FF9E00;">Pond Fish</div></div>
<div style="text-align: center;"><span style="font-size: 1.8rem;">🎃</span><div style="font-size: 0.75rem; font-weight: 700; color: #FF7A00;">Jack-o'-Lantern</div></div>
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

    # 2. Clean 4-Step Minimal Navigation Stepper
    if st.session_state.active_screen in ("home", "login"):
        attempts = get_quiz_attempts(user_gid)
        entry = get_entry_by_governor(user_gid)
        if not attempts:
            st.session_state.active_screen = "quiz"
        elif not entry:
            st.session_state.active_screen = "submit"
        else:
            st.session_state.active_screen = "gallery"

    steps = [
        ("quiz", "🧠 Quiz"),
        ("submit", "🎨 Costume"),
        ("gallery", "👻 Gallery"),
        ("leaderboard", "🏆 Podium")
    ]

    step_cols = st.columns(4)
    for i, (s_key, s_label) in enumerate(steps):
        with step_cols[i]:
            is_active = (st.session_state.active_screen == s_key)
            lbl = f"⭐ {s_label}" if is_active else s_label
            if st.button(lbl, key=f"step_btn_{s_key}"):
                st.session_state.active_screen = s_key
                st.rerun()

    st.markdown("---")

    # 3. Active Screen View
    curr = st.session_state.active_screen

    if curr == "quiz":
        render_quiz(user_gid, current_phase)
    elif curr == "submit":
        render_submit(user_gid, current_phase)
    elif curr == "gallery":
        render_gallery(user_gid, current_phase)
    elif curr == "leaderboard":
        render_leaderboard(current_phase, phase_info.get("voting_end"))
    else:
        render_quiz(user_gid, current_phase)

    # 4. Spooky Dad Joke at bottom of view
    render_dad_joke_card()


# ==========================================
# SPOOKY HALLOWEEN FOOTER
# ==========================================
st.markdown("---")
st.markdown('<div style="text-align: center; color: var(--text-secondary); font-size: 0.9rem; padding: 1rem 0;">🎃 <strong>NXE Pond Fam Halloween</strong> • May Your Pumpkins Glow & Your Ducks Quack Forever! 🦆👻🦇</div>', unsafe_allow_html=True)
