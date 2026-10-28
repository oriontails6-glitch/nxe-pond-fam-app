"""
Trivia Quiz screen for NXE Pond Fam Halloween App.
Features:
- 5 random active questions per attempt from Supabase pool
- Shuffled option order
- Max 3 attempts per Governor ID
- 30-second cooldown between attempts
- Automatic progression guidance to Costume Submission
- Server-side grading
- Hilarious spooky kid-friendly jokes
"""
import random
import time
import streamlit as st
from datetime import datetime, timezone
import config
from db import (
    get_active_questions,
    get_quiz_attempts,
    record_quiz_attempt,
    get_entry_by_governor,
    update_entry_quiz_status
)
from phases import CompetitionPhase


def render_quiz(user_gid: str, current_phase: CompetitionPhase):
    st.markdown("## 🧠 The Spooky Fantasy Lore Initiation 🎃")
    st.markdown("""
    *Answer 5 fun questions from the whimsical pond archives! Trivia scores are purely for bragging rights — all contestants stand on 100% equal ground to win!*
    """)

    # Phase check: Trivia allowed ONLY in Phase 1
    if current_phase != CompetitionPhase.SUBMISSIONS:
        st.warning(f"🔒 The Trivia Gate is sleeping during **{current_phase.label}**. No new quiz attempts can be made.")
        attempts = get_quiz_attempts(user_gid)
        if attempts:
            best = max(a["score"] for a in attempts)
            st.info(f"Your final recorded trivia score is **{best}/5** (👑 Official Contestant on Equal Ground!).")
        
        # Guide button to next step
        if st.button("🎨 Go to Costume Submission ➡️", key="quiz_closed_next_btn"):
            st.session_state.active_screen = "submit"
            st.rerun()
        return

    # Check previous attempts
    attempts = get_quiz_attempts(user_gid)
    attempts_used = len(attempts)
    best_score = max([a["score"] for a in attempts], default=0) if attempts else 0

    st.markdown(f'<div class="pond-card" style="display: flex; justify-content: space-around; text-align: center;"><div><div style="font-size: 0.85rem; color: var(--text-secondary);">ATTEMPTS USED</div><div style="font-family: \'Fredoka\', sans-serif; font-size: 1.5rem; color: var(--sky);">{attempts_used}/{config.QUIZ_MAX_ATTEMPTS}</div></div><div><div style="font-size: 0.85rem; color: var(--text-secondary);">LORE FLEX SCORE</div><div style="font-family: \'Fredoka\', sans-serif; font-size: 1.5rem; color: var(--candy);">{best_score}/5</div></div><div><div style="font-size: 0.85rem; color: var(--text-secondary);">STATUS</div><div style="font-family: \'Fredoka\', sans-serif; font-size: 1.2rem; color: #34D399;">{"👑 Ready to Compete!" if attempts_used > 0 else "📚 In Progress"}</div></div></div>', unsafe_allow_html=True)

    # Check 30-second cooldown from newest attempt
    if attempts:
        newest = datetime.fromisoformat(attempts[0]["created_at"].replace("Z", "+00:00"))
        elapsed = (datetime.now(timezone.utc) - newest).total_seconds()
        if elapsed < config.QUIZ_COOLDOWN_SECONDS:
            remaining_cd = int(config.QUIZ_COOLDOWN_SECONDS - elapsed)
            st.warning(f"⏳ The ghosts are reviewing your scroll! Please wait **{remaining_cd} seconds** before attempting again.")
            return

    # If already took an attempt, guide forward while allowing more tries if available
    if attempts_used > 0:
        st.success(f"🎉 **Initiation Complete!** Your best trivia score is **{best_score}/5**! (All contestants stand on 100% equal ground to win the tournament prizes!)")
        st.markdown("""
        <div class="next-step-box">
            <h3 style="color: var(--candy); margin: 0 0 0.4rem 0;">🎃 Step 1 Complete!</h3>
            <p style="color: #F8FAFC; margin-bottom: 0.8rem;">Your costume stands on equal ground! Ready to upload your photo & backstory?</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎨 Continue to Costume Submission ➡️", key="quiz_pass_proceed_btn"):
            st.session_state.active_screen = "submit"
            st.rerun()

        if attempts_used >= config.QUIZ_MAX_ATTEMPTS:
            st.markdown("---")
            return
        st.caption("Want to flex your lore knowledge with another attempt? You can try again below (scores are for fun):")

    # Quiz initialization in session_state
    if "current_quiz_questions" not in st.session_state or st.session_state.get("quiz_attempt_num") != attempts_used:
        all_pool = get_active_questions()
        if len(all_pool) < config.QUIZ_QUESTIONS_PER_ATTEMPT:
            st.error("The Goblin Librarian hasn't seeded questions yet! Please run `python seed_questions.py`.")
            return

        sampled = random.sample(all_pool, config.QUIZ_QUESTIONS_PER_ATTEMPT)
        prepared = []
        for q in sampled:
            opts = list(enumerate(q["options"]))
            random.shuffle(opts)
            shuffled_texts = [o[1] for o in opts]
            new_correct_idx = [i for i, o in enumerate(opts) if o[0] == q["correct_index"]][0]

            prepared.append({
                "id": q["id"],
                "text": q["text"],
                "options": shuffled_texts,
                "_correct_index": new_correct_idx
            })

        st.session_state.current_quiz_questions = prepared
        st.session_state.quiz_attempt_num = attempts_used

    # Render Active Quiz Form
    st.markdown(f"### Attempt #{attempts_used + 1} of {config.QUIZ_MAX_ATTEMPTS}")
    st.caption("Pick the best answer for each question. Score 3+ to qualify!")

    questions = st.session_state.current_quiz_questions
    user_choices = {}

    with st.form(f"quiz_form_{attempts_used}"):
        for idx, q in enumerate(questions, start=1):
            st.markdown(f"**{idx}. {q['text']}**")
            choice = st.radio(
                label=f"q_{q['id']}",
                options=q["options"],
                key=f"q_choice_{q['id']}",
                label_visibility="collapsed"
            )
            user_choices[q["id"]] = q["options"].index(choice)
            st.markdown("")

        submit_quiz_btn = st.form_submit_button("📜 Grade My Answers & Cast the Spell!")

        if submit_quiz_btn:
            score = 0
            q_ids = []
            for q in questions:
                q_ids.append(q["id"])
                if user_choices.get(q["id"]) == q["_correct_index"]:
                    score += 1

            # Record attempt in database
            record_quiz_attempt(user_gid, score, q_ids)

            # Update entry if exists and score improved
            new_best = max(best_score, score)
            existing_entry = get_entry_by_governor(user_gid)
            if existing_entry:
                update_entry_quiz_status(user_gid, new_best, True)

            # Clear session questions
            if "current_quiz_questions" in st.session_state:
                del st.session_state.current_quiz_questions

            # Celebrate completion (everyone qualifies on equal ground!)
            st.balloons()
            st.session_state.active_screen = "submit"
            st.rerun()
