"""
Anonymous Costume Gallery & Voting Screen for NXE Pond Fam Halloween App.
Features:
- 100% anonymous (no names or Governor IDs displayed)
- Mobile-first layout with pagination (8 cards at a time)
- Sticky 'Votes left: X/3' chip during Phase 3
- Atomic transaction-safe voting via Supabase RPC
- Non-qualified entries showcase with funny deterministic badges
- Long backstories collapsible with 'Read more'
- Seamless navigation buttons to other steps
"""
import html
import random
import streamlit as st
import config
from db import (
    get_public_gallery_entries,
    get_voter_cast_votes,
    cast_vote,
    remove_vote,
    get_entry_by_governor
)
from phases import CompetitionPhase


def render_gallery(user_gid: str, current_phase: CompetitionPhase):
    st.markdown("## 👻 Anonymous Costume Gallery 🪷")

    # Phase 1: Gallery is sealed until Phase 2
    if current_phase == CompetitionPhase.SUBMISSIONS:
        st.markdown("""<div class="pond-card" style="text-align: center; padding: 2.2rem 1.2rem;">
<div style="font-size: 2.6rem; margin-bottom: 0.35rem;">🗝️ 🪷 🔒</div>
<h3 style="color: #FDE047; font-family: 'Fredoka', sans-serif; font-size: 1.5rem; margin: 0.2rem 0 0.6rem 0;">The Misty Pond Vault is Sealed!</h3>
<p style="color: #DDD6FE; font-size: 0.94rem; line-height: 1.55; max-width: 460px; margin: 0 auto 1.2rem auto;">
All contestant costumes are safely resting under the moonlit lily pads to keep every disguise a grand surprise. The gallery unseals when deliberations begin!
</p>
<div style="display: inline-block; background: rgba(251, 191, 36, 0.15); border: 1px solid rgba(251, 191, 36, 0.35); border-radius: 9999px; padding: 6px 16px; font-size: 0.9rem; color: #FDE68A; font-weight: 700;">
⏳ Submissions are open now • Make sure your costume is sealed!
</div>
</div>""", unsafe_allow_html=True)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            if st.button("⬅️ Back to Lore Quiz", key="gal_to_quiz_btn"):
                st.session_state.active_screen = "quiz"
                st.rerun()
        with col_g2:
            if st.button("🎨 Go to Costume Submission ➡️", key="gal_to_sub_btn"):
                st.session_state.active_screen = "submit"
                st.rerun()
        return

    # Fetch gallery entries
    if "gallery_order" not in st.session_state:
        raw_entries = get_public_gallery_entries()
        random.shuffle(raw_entries)
        st.session_state.gallery_order = raw_entries
    else:
        raw_entries = st.session_state.gallery_order

    if not raw_entries:
        st.info("No costumes are floating in the pond yet. Check back soon!")
        return

    # User's own entry ID
    user_entry = get_entry_by_governor(user_gid)
    user_entry_id = user_entry["id"] if user_entry else None

    # Fetch user's current votes
    user_votes = get_voter_cast_votes(user_gid)
    votes_used = len(user_votes)
    votes_left = max(0, config.VOTES_PER_VOTER - votes_used)

    # Phase 3 Sticky Votes Chip
    if current_phase == CompetitionPhase.VOTING:
        st.markdown(f'<div class="sticky-votes-chip">🗳️ Votes Remaining: {votes_left} / {config.VOTES_PER_VOTER}</div>', unsafe_allow_html=True)
        st.caption("Tap 'Vote' on 3 different favorites. You can remove a vote and re-spend it anytime before voting ends!")
    elif current_phase == CompetitionPhase.JUDGING:
        st.markdown('<div class="pond-card pumpkin-accent-card"><strong>👻 Phase 2 Deliberation:</strong> Browse and admire the spooky costumes! Community voting unlocks in Phase 3.</div>', unsafe_allow_html=True)
    else:
        st.info("Voting has concluded! Check the **Leaderboard** for the crowned winner.")

    # Pagination: 8 entries per page
    if "gallery_page_size" not in st.session_state:
        st.session_state.gallery_page_size = 8

    visible_entries = raw_entries[:st.session_state.gallery_page_size]

    for idx, entry in enumerate(visible_entries, start=1):
        eid = entry["id"]
        is_own = (eid == user_entry_id)
        is_voted = (eid in user_votes)
        is_qualified = entry.get("qualified", False)

        with st.container():
            img_url = entry.get("thumb_path") or entry.get("image_path") or ""
            escaped_img = html.escape(img_url)
            raw_backstory = entry.get("backstory", "").strip()
            escaped_backstory = html.escape(raw_backstory)

            card_html = f"""<div class="gallery-item">
<details class="gallery-card-details">
<summary>
<div class="gallery-img-container">
<img src="{escaped_img}" alt="Halloween Costume" class="gallery-fit-image" loading="lazy" />
</div>
<div style="text-align: center;">
<span class="tap-reveal-pill">👆 Tap photo to read backstory 📖</span>
</div>
</summary>
<div class="story-revealed-panel">
<div class="story-header">📜 Spooky Backstory:</div>
<p class="story-body">{escaped_backstory}</p>
</div>
</details>"""
            st.markdown(card_html, unsafe_allow_html=True)

            st.markdown('<div style="color: #34D399; font-size: 0.9rem; font-weight: 700; margin: 4px 0 10px 0;">🎃 Official Contestant</div>', unsafe_allow_html=True)

            # Voting Controls (Active in Phase 3)
            if current_phase == CompetitionPhase.VOTING:
                if is_own:
                    st.info("🌟 This is your own costume! (Self-voting is forbidden)")
                elif is_voted:
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.success("✅ Voted for this costume!")
                    with c2:
                        if st.button("❌ Remove Vote", key=f"unvote_{eid}"):
                            res = remove_vote(user_gid, eid)
                            if res.get("success"):
                                st.rerun()
                            else:
                                st.error(res.get("message", "Error removing vote."))
                elif votes_left > 0:
                    if st.button(f"🗳️ Vote for Costume #{idx}", key=f"vote_{eid}"):
                        res = cast_vote(user_gid, eid)
                        if res.get("success"):
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(res.get("message", "Error casting vote."))
                else:
                    st.caption("🔒 All 3 votes used! (Remove a vote above to switch)")

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("")

    # Load More Button
    if st.session_state.gallery_page_size < len(raw_entries):
        if st.button("🔽 Load 8 More Costumes", key="load_more_btn"):
            st.session_state.gallery_page_size += 8
            st.rerun()

    # Navigation Bar
    st.markdown("---")
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Back to Costume", key="gal_back_sub_btn"):
            st.session_state.active_screen = "submit"
            st.rerun()
    with col_nav2:
        if st.button("🏆 View Podium ➡️", key="gal_to_leaderboard_btn"):
            st.session_state.active_screen = "leaderboard"
            st.rerun()
