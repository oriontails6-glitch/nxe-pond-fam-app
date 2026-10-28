"""
Submission Portal for NXE Pond Fam Halloween App.
Features:
- Costume and avatar submission with live preview
- In-game name and backstory length validation
- Automatic progression guidance to Costume Gallery
- Kid-friendly spooky Halloween microcopy
"""
import html
import streamlit as st
import config
from db import (
    get_entry_by_governor,
    get_quiz_attempts,
    upsert_entry
)
from images import process_and_upload_avatar
from phases import CompetitionPhase


def sanitize_text(text: str) -> str:
    """Strips dangerous control characters and trims text."""
    if not text:
        return ""
    clean = "".join(ch for ch in text if ch == "\n" or ch == "\r" or ch == "\t" or (ord(ch) >= 32 and ord(ch) != 127))
    return clean.strip()


def render_submit(user_gid: str, current_phase: CompetitionPhase):
    st.markdown("## 🎨 Costume & Avatar Submission Portal 🎃")

    # Check existing entry
    existing_entry = get_entry_by_governor(user_gid)
    is_editing = existing_entry is not None

    # Check quiz score and qualification (everyone qualifies on equal ground!)
    attempts = get_quiz_attempts(user_gid)
    best_score = max([a["score"] for a in attempts], default=0) if attempts else 0
    is_qualified = True

    # Phase check: submissions allowed only in Phase 1
    if current_phase != CompetitionPhase.SUBMISSIONS:
        st.warning(f"🔒 Costume submissions are currently sleeping. Current stage: **{current_phase.label}**.")
        if existing_entry:
            st.info("Your costume is safely locked inside the mist-shrouded pond vault:")
            if existing_entry.get("thumb_path"):
                st.image(existing_entry["thumb_path"], caption="Your Spooky Avatar", width=300)
            st.markdown(f"**In-Game Name:** {html.escape(existing_entry['ingame_name'])}")
            st.markdown(f"**Backstory:** {html.escape(existing_entry['backstory'])}")

            st.markdown("""
            <div class="next-step-box">
                <h3 style="color: var(--candy); margin: 0 0 0.4rem 0;">👻 Costume Locked & Ready!</h3>
                <p style="color: #F8FAFC; margin-bottom: 0.8rem;">Ready to inspect everyone's spooky costumes in the gallery?</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("👻 Explore the Spooky Costume Gallery ➡️", key="sub_locked_to_gal"):
                st.session_state.active_screen = "gallery"
                st.rerun()
        return

    # Everyone competes on equal ground
    if not attempts:
        st.info("💡 **Psst!** You haven't tried the Spooky Fantasy Lore Quiz yet! Feel free to submit your costume now and take the fun quiz anytime.")
    else:
        st.success(f"✨ **All Contestants Stand on Equal Ground!** Your trivia flex score is {best_score}/5. Every costume is 100% eligible for community voting and all tournament prizes!")

    if is_editing:
        st.markdown('<div class="pond-card pumpkin-accent-card"><strong>✨ Existing Costume Found!</strong> You can update your photo, name, or backstory anytime before the deadline.</div>', unsafe_allow_html=True)

    default_name = existing_entry["ingame_name"] if is_editing else ""
    default_backstory = existing_entry["backstory"] if is_editing else ""

    with st.form("costume_submission_form"):
        ign_input = st.text_input(
            "In-Game Name (your King Shot name, max 30 chars)",
            value=default_name,
            max_chars=config.INGAME_NAME_MAX_CHARS,
            placeholder="e.g. SpookyDuckling99"
        )

        st.markdown("#### 📸 Avatar Image")
        st.caption("Upload a PNG or JPG photo (max 5 MB). The app will automatically convert it to WebP and remove EXIF data.")
        avatar_file = st.file_uploader(
            "Select costume photo",
            type=["png", "jpg", "jpeg", "webp"],
            label_visibility="collapsed"
        )

        if is_editing and existing_entry.get("thumb_path") and not avatar_file:
            st.caption("Currently saved costume:")
            st.image(existing_entry["thumb_path"], width=180)

        backstory_input = st.text_area(
            "Character Backstory (max 500 chars)",
            value=default_backstory,
            max_chars=config.BACKSTORY_MAX_CHARS,
            height=130,
            placeholder="Describe your character's eerie origin, comedic pond escapades, or spooky goblin title..."
        )

        chars_len = len(backstory_input.strip())
        st.caption(f"Length: {chars_len}/{config.BACKSTORY_MAX_CHARS} characters")

        submit_btn = st.form_submit_button(
            "🎃 Update My Costume" if is_editing else "🎃 Seal My Costume in the Pond Vault!"
        )

        if submit_btn:
            clean_name = sanitize_text(ign_input)
            clean_backstory = sanitize_text(backstory_input)

            if not clean_name:
                st.error("Please enter your In-Game Name so the alliance knows who you are!")
                return

            if not clean_backstory:
                st.error("Please write a spooky or silly character backstory!")
                return

            # Handle image
            image_url = existing_entry["image_path"] if is_editing else None
            thumb_url = existing_entry["thumb_path"] if is_editing else None

            if avatar_file:
                bytes_data = avatar_file.getvalue()
                old_img = existing_entry.get("image_path") if is_editing else None
                old_thumb = existing_entry.get("thumb_path") if is_editing else None

                ok_img, msg_img, main_url, t_url = process_and_upload_avatar(
                    bytes_data, avatar_file.name, old_img, old_thumb
                )

                if not ok_img:
                    st.error(msg_img)
                    return

                image_url = main_url
                thumb_url = t_url

            elif not is_editing:
                st.error("Please choose a costume photo to upload!")
                return

            # Upsert into database
            try:
                upsert_entry(
                    governor_id=user_gid,
                    ingame_name=clean_name,
                    backstory=clean_backstory,
                    image_path=image_url,
                    thumb_path=thumb_url,
                    quiz_score=best_score,
                    qualified=is_qualified
                )

                st.balloons()
                st.success("🎃 **BOO! Your costume has been sealed in the vault!**")
                st.session_state.active_screen = "gallery"
                st.rerun()

            except Exception:
                st.error("A spooky swamp hiccup occurred! Could not save right now. Please try again.")

    # Navigation Bar
    st.markdown("---")
    col_sn1, col_sn2 = st.columns(2)
    with col_sn1:
        if st.button("⬅️ Back to Quiz", key="sub_back_to_quiz"):
            st.session_state.active_screen = "quiz"
            st.rerun()
    with col_sn2:
        if st.button("👻 Continue to Gallery ➡️", key="sub_proceed_to_gallery"):
            st.session_state.active_screen = "gallery"
            st.rerun()
