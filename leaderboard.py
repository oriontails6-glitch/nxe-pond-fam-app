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
    st.markdown("## 🏆 Grand Halloween Leaderboard 🎃")

    # Phase check: locked until Phase 4 (Results)
    if current_phase != CompetitionPhase.RESULTS:
        st.markdown(f'<div class="pond-card" style="text-align: center; padding: 2.5rem 1rem;"><div style="font-size: 3rem; margin-bottom: 0.5rem;">👑 🎃 👑</div><h3 style="color: var(--pumpkin);">Results Locked Until Voting Concludes!</h3><p style="color: var(--text-secondary); max-width: 480px; margin: 0 auto 1.2rem auto;">The Goblin Council and Pond Ghosts are keeping vote tallies 100% confidential to prevent bandwagon voting!</p><div style="font-size: 1.1rem; color: var(--candy); font-weight: 700;">⏳ Grand Reveal scheduled for: {format_utc_display(voting_end_utc)}</div></div>', unsafe_allow_html=True)

        col_l1, col_l2 = st.columns(2)
        with col_l1:
            if st.button("⬅️ Explore the Costume Gallery", key="lb_back_gal_btn"):
                st.session_state.active_screen = "gallery"
                st.rerun()
        with col_l2:
            if st.button("🏰 Return to Home Hub", key="lb_back_home_btn"):
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

    st.markdown(f'<div class="pond-card" style="border: 2px solid #FFD700; background: linear-gradient(180deg, #2D1438 0%, #160D24 100%); text-align: center; padding: 2rem 1rem;"><div style="font-size: 3rem; margin-bottom: 0.2rem;">👑 🎃 👑</div><div style="font-size: 0.95rem; font-weight: 800; color: #FFD700; text-transform: uppercase; letter-spacing: 1.5px;">NXE Halloween Champion</div><h1 style="color: var(--pumpkin); margin: 0.4rem 0 0.8rem 0; font-size: 2.3rem;">{escaped_name}</h1><div style="display: inline-block; background: rgba(255, 209, 102, 0.2); border: 2px solid #FFD166; border-radius: 9999px; padding: 8px 20px; font-weight: 700; color: #FFD166; font-size: 1.15rem; margin-bottom: 1rem;">🗳️ {winner["votes"]} Total Community Votes</div></div>', unsafe_allow_html=True)

    if winner.get("image_path"):
        st.markdown(f"""<div class="gallery-img-container" style="max-height: 320px; height: 300px; margin: 0.5rem auto 1rem auto;">
<img src="{html.escape(winner['image_path'])}" alt="Champion Costume" class="gallery-fit-image" />
</div>""", unsafe_allow_html=True)

    st.markdown(f"**Winning Backstory:**\n\n> *{escaped_story}*")
    st.markdown("---")

    # Full Kingdom Standings
    st.markdown("### 🎖️ Full Kingdom Standings")

    for entry in leaderboard_data:
        rank = entry["rank"]
        name = html.escape(entry["ingame_name"])
        story = html.escape(entry["backstory"])
        votes = entry["votes"]

        rank_badge = "👑 #1" if rank == 1 else (f"🥈 #{rank}" if rank == 2 else (f"🥉 #{rank}" if rank == 3 else f"#{rank}"))

        with st.expander(f"{rank_badge} — {name} ({votes} votes)", expanded=(rank <= 3)):
            col1, col2 = st.columns([1, 2])
            with col1:
                thumb = entry.get("thumb_path") or entry.get("image_path")
                if thumb:
                    st.image(thumb, use_column_width=True)
            with col2:
                st.markdown(f"**In-Game Name:** `{name}`")
                st.markdown(f"**Final Votes:** `{votes}`")
                st.markdown(f"**Backstory:** {story}")

    st.markdown("---")
    if st.button("⬅️ Back to Costume Gallery", key="lb_end_gal_btn"):
        st.session_state.active_screen = "gallery"
        st.rerun()
