"""
Leaderboard and Winner Reveal Screen for NXE Pond Fam Halloween App.
Features:
- Locked with countdown until Phase 4 (Results)
- Ranks only qualified, non-hidden entries
- Top 3 podium with confetti and crown animations
- Shared ranks for ties
- Unveils winner's In-Game Name and avatar
- Back navigation buttons
"""
import html
import streamlit as st
from db import get_leaderboard
from phases import CompetitionPhase, format_utc_display


def render_leaderboard(current_phase: CompetitionPhase, voting_end_utc):
    st.markdown("## Tournament Leaderboard")

    # Phase check: locked until Phase 4 (Results)
    if current_phase != CompetitionPhase.RESULTS:
        st.markdown(f'<div class="pond-card" style="text-align: center; padding: 2.5rem 1rem;"><div style="font-size: 2rem; margin-bottom: 0.5rem;">🏆</div><h3 style="color: var(--pumpkin);">Results Locked Until Voting Concludes</h3><p style="color: var(--text-secondary); max-width: 480px; margin: 0 auto 1.2rem auto;">Vote tallies remain confidential until voting officially concludes to ensure fair results.</p><div style="font-size: 1.05rem; color: var(--candy); font-weight: 700;">Grand Reveal scheduled for: {format_utc_display(voting_end_utc)}</div></div>', unsafe_allow_html=True)

        col_l1, col_l2 = st.columns(2)
        with col_l1:
            if st.button("← Explore Costume Gallery", key="lb_back_gal_btn"):
                st.session_state.active_screen = "gallery"
                st.rerun()
        with col_l2:
            if st.button("Return to Home", key="lb_back_home_btn"):
                st.session_state.active_screen = "home"
                st.rerun()
        return

    # Phase 4 Active: Display winners!
    leaderboard_data = get_leaderboard()

    if not leaderboard_data:
        st.info("No qualified contestants entered the arena.")
        return

    st.balloons()

    # Grand Winner Spotlight
    winner = leaderboard_data[0]
    escaped_name = html.escape(winner["ingame_name"])
    escaped_story = html.escape(winner["backstory"])

    st.markdown(f"""<div class="pond-card" style="border: 1px solid rgba(251, 191, 36, 0.45); background: linear-gradient(135deg, rgba(58, 28, 92, 0.85) 0%, rgba(28, 14, 48, 0.9) 100%); text-align: center; padding: 2rem 1.2rem; box-shadow: 0 14px 40px rgba(251, 191, 36, 0.25);">
<div style="font-size: 0.9rem; font-weight: 800; color: #FBBF24; text-transform: uppercase; letter-spacing: 2px; font-family: 'Fredoka', sans-serif;">NXE Tournament Champion</div>
<h1 style="color: #FFFDF5; margin: 0.4rem 0 0.6rem 0; font-size: 2.3rem; text-shadow: 0 2px 12px rgba(251, 191, 36, 0.4);">{escaped_name}</h1>
<div style="display: inline-block; background: rgba(251, 191, 36, 0.18); border: 1px solid #FBBF24; border-radius: 9999px; padding: 6px 20px; font-weight: 700; color: #FDE68A; font-size: 1.05rem; margin-bottom: 0.75rem;">
{winner["votes"]} Community Votes
</div>
<div style="display: block; background: rgba(124, 58, 237, 0.25); border: 1px solid rgba(196, 181, 253, 0.3); border-radius: 14px; padding: 8px 14px; color: #FDE047; font-weight: 700; font-size: 0.95rem; max-width: 380px; margin: 0 auto;">
Grand Prize: 1 Month Card (Sponsored by Papa Mo)
</div>
</div>""", unsafe_allow_html=True)

    if winner.get("image_path"):
        st.markdown(f"""<div class="gallery-img-container" style="max-height: 320px; height: 300px; margin: 0.5rem auto 1rem auto;">
<img src="{html.escape(winner['image_path'])}" alt="Champion Costume" class="gallery-fit-image" />
</div>""", unsafe_allow_html=True)

    st.markdown(f"**Winning Backstory:**\n\n> *{escaped_story}*")
    st.markdown("---")

    # Full Kingdom Standings
    st.markdown("### Final Standings")

    for entry in leaderboard_data:
        rank = entry["rank"]
        name = html.escape(entry["ingame_name"])
        story = html.escape(entry["backstory"])
        votes = entry["votes"]

        rank_badge = "1st Place (#1)" if rank == 1 else (f"2nd Place (#{rank})" if rank == 2 else (f"3rd Place (#{rank})" if rank == 3 else f"#{rank}"))

        with st.expander(f"{rank_badge} — {name} ({votes} votes)", expanded=(rank <= 3)):
            col1, col2 = st.columns([1, 2])
            with col1:
                thumb = entry.get("thumb_path") or entry.get("image_path")
                if thumb:
                    st.image(thumb, use_column_width=True)
            with col2:
                st.markdown(f"**In-Game Name:** `{name}`")
                st.markdown(f"**Final Votes:** `{votes}`")
                if rank == 1:
                    st.markdown("**Prize:** `1 Month Card` *(Sponsored by Papa Mo)*")
                elif rank == 2:
                    st.markdown("**Prize:** `Everyone Obeys You for 24 Hours!`")
                elif rank == 3:
                    st.markdown("**Prize:** `150M RSS Dinner at Orion's Pax`")
                st.markdown(f"**Backstory:** {story}")

    st.markdown("---")
    if st.button("← Back to Costume Gallery", key="lb_end_gal_btn"):
        st.session_state.active_screen = "gallery"
        st.rerun()
