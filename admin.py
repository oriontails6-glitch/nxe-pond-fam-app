"""
Admin Sanctum for NXE Pond Fam Halloween App.
Reached strictly via ?page=admin.
Features:
- Constant-time password check across 4 admin credentials
- Full submissions view (including hidden and non-qualified entries)
- Hide & restore entries with mandatory reason
- Roster Manager (paste, CSV upload, add single, remove, deduplicate)
- Vote Audit (live vote tallies and void vote capability)
- Phase Settings Editor
- CSV Export of entries and votes
- TEST_MODE phase override selector (hidden when TEST_MODE=False)
"""
import io
import csv
import hmac
import html
import streamlit as st
from datetime import datetime, timezone, timedelta
import config
from db import (
    get_all_entries_admin,
    set_entry_hidden_admin,
    get_all_votes_admin,
    void_vote_admin,
    update_setting_admin,
    get_settings,
    get_admin_logs,
    add_roster_ids,
    remove_roster_id,
    get_roster_overview,
    get_entry_by_governor,
    get_voter_cast_votes
)


def verify_admin_credentials(username: str, password: str) -> bool:
    """Verifies credentials using constant-time comparison."""
    if not username or not password:
        return False
    try:
        admins = st.secrets.get("ADMIN_USERS", {})
        if username in admins:
            expected_pass = str(admins[username])
            return hmac.compare_digest(expected_pass.encode("utf-8"), password.encode("utf-8"))
    except Exception:
        pass
    return False


def render_admin(test_mode: bool):
    st.markdown("## 🏛️ NXE Council Admin Sanctum")

    # Session authentication check
    if "admin_logged_user" not in st.session_state:
        st.session_state.admin_logged_user = None

    admin_user = st.session_state.admin_logged_user

    if not admin_user:
        st.markdown("#### 🔒 Council Officer Verification")
        with st.form("admin_login_form"):
            u_in = st.text_input("Officer Username")
            p_in = st.text_input("Passkey", type="password")
            login_btn = st.form_submit_button("Unlock Sanctum")

            if login_btn:
                if verify_admin_credentials(u_in.strip(), p_in.strip()):
                    st.session_state.admin_logged_user = u_in.strip()
                    st.session_state.admin_login_time = datetime.now(timezone.utc)
                    st.success("Access granted to the Council Sanctum.")
                    st.rerun()
                else:
                    st.error("Invalid officer credentials.")
        return

    # Logged-in Header
    col_adm1, col_adm2 = st.columns([3, 1])
    with col_adm1:
        st.success(f"🛡️ Logged in as: **{admin_user}**")
    with col_adm2:
        if st.button("🚪 Lock Sanctum", key="admin_logout_btn"):
            st.session_state.admin_logged_user = None
            st.rerun()

    # Admin Tabs
    t_entries, t_roster, t_votes, t_settings, t_logs = st.tabs([
        "📋 Submissions",
        "📜 Roster Manager",
        "🗳️ Vote Audit",
        "🕒 Phase Settings",
        "📜 Audit Logs & Export"
    ])

    # ==========================================
    # 1. SUBMISSIONS TAB
    # ==========================================
    with t_entries:
        st.subheader("All Costumes (Qualified, Non-Qualified & Hidden)")
        entries = get_all_entries_admin()

        if not entries:
            st.info("No costume entries submitted yet.")
        else:
            for e in entries:
                eid = e["id"]
                ign = html.escape(e["ingame_name"])
                gid = e["governor_id"]
                score = e["quiz_score"]
                qual = e["qualified"]
                is_hidden = e["hidden"]

                status_tag = "🔴 HIDDEN" if is_hidden else "👑 Qualified"

                with st.expander(f"{ign} (Gov: {gid}) — {status_tag} | Lore Score: {score}/5"):
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        if e.get("thumb_path") or e.get("image_path"):
                            st.image(e.get("thumb_path") or e["image_path"], use_column_width=True)
                    with c2:
                        st.markdown(f"**In-Game Name:** `{ign}`")
                        st.markdown(f"**Governor ID:** `{gid}`")
                        st.markdown(f"**Quiz Score:** `{score}/5` *(All contestants stand on 100% equal ground)*")
                        st.markdown(f"**Submitted UTC:** `{e.get('created_at')}`")
                        st.markdown(f"**Backstory:**\n{html.escape(e['backstory'])}")

                        st.markdown("---")
                        st.markdown("#### Moderation Action")
                        reason = st.text_input("Mandatory reason for action:", key=f"reason_{eid}")
                        if is_hidden:
                            if st.button("🟢 Restore to Public Gallery", key=f"rest_{eid}"):
                                if not reason.strip():
                                    st.error("Please enter a reason for audit logging.")
                                else:
                                    set_entry_hidden_admin(eid, False, admin_user, reason.strip())
                                    st.success("Entry restored.")
                                    st.rerun()
                        else:
                            if st.button("🔴 Hide from Public Gallery", key=f"hide_{eid}"):
                                if not reason.strip():
                                    st.error("Please enter a reason for audit logging.")
                                else:
                                    set_entry_hidden_admin(eid, True, admin_user, reason.strip())
                                    st.success("Entry hidden.")
                                    st.rerun()

    # ==========================================
    # 2. ROSTER MANAGER TAB
    # ==========================================
    with t_roster:
        st.subheader("Alliance Roster Allowlist")
        roster_list = get_roster_overview()
        st.metric("Total Approved Governors", len(roster_list))

        st.markdown("#### Batch Add Governor IDs")
        st.caption("Paste IDs separated by newlines, commas, or spaces (e.g. from kingdom bot or discord export):")
        pasted_text = st.text_area("Governor IDs to Allow", height=100, key="roster_paste")

        uploaded_roster = st.file_uploader("Or Upload CSV with Governor IDs", type=["csv"], key="roster_csv")

        if st.button("➕ Process & Add to Roster"):
            raw_ids = []
            if pasted_text:
                # Split by commas, spaces, newlines
                cleaned = pasted_text.replace(",", " ").replace(";", " ")
                raw_ids.extend(cleaned.split())

            if uploaded_roster:
                try:
                    content = uploaded_roster.getvalue().decode("utf-8")
                    reader = csv.reader(io.StringIO(content))
                    for row in reader:
                        raw_ids.extend(row)
                except Exception:
                    st.error("Error reading CSV file.")

            if not raw_ids:
                st.warning("Please paste IDs or upload a CSV first.")
            else:
                added, dupes, inv = add_roster_ids(raw_ids)
                st.success(f"✅ Roster updated: Added **{added}**, skipped **{dupes}** duplicates, ignored **{inv}** invalid entries.")
                st.rerun()

        st.markdown("---")
        st.markdown("#### Remove a Governor ID")
        remove_id = st.text_input("Governor ID to remove")
        if st.button("Remove ID from Roster"):
            if not remove_id.strip():
                st.warning("Enter an ID.")
            else:
                target = remove_id.strip()
                # Warn if player has an entry or votes
                existing_e = get_entry_by_governor(target)
                existing_v = get_voter_cast_votes(target)
                warn_msg = []
                if existing_e:
                    warn_msg.append(f"This governor has submitted entry '{existing_e['ingame_name']}'!")
                if existing_v:
                    warn_msg.append(f"This governor has already cast {len(existing_v)} vote(s)!")

                if warn_msg:
                    st.warning(" ⚠️ " + " ".join(warn_msg))

                remove_roster_id(target)
                st.success(f"Governor ID {target} removed from roster.")
                st.rerun()

    # ==========================================
    # 3. VOTE AUDIT TAB
    # ==========================================
    with t_votes:
        st.subheader("Live Vote Audit & Tallies")
        votes = get_all_votes_admin()
        entries = get_all_entries_admin()
        entry_map = {e["id"]: e for e in entries}

        st.metric("Total Community Votes Cast", len(votes))

        # Live vote count per entry
        counts = {}
        for v in votes:
            eid = v["entry_id"]
            counts[eid] = counts.get(eid, 0) + 1

        ranked_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        st.markdown("#### Live Vote Tallies (Admin Confidential)")
        for eid, tally in ranked_counts:
            entry_info = entry_map.get(eid)
            ign = entry_info["ingame_name"] if entry_info else "Unknown"
            gid = entry_info["governor_id"] if entry_info else "Unknown"
            st.write(f"🗳️ **{tally} votes** — {ign} (Gov ID: `{gid}`)")

        st.markdown("---")
        st.markdown("#### Individual Vote Logs")
        for v in votes[:50]:
            vid = v["id"]
            voter = v["voter_id"]
            target_entry = entry_map.get(v["entry_id"])
            t_ign = target_entry["ingame_name"] if target_entry else v["entry_id"]
            col_v1, col_v2 = st.columns([3, 1])
            with col_v1:
                st.caption(f"Vote #{vid}: Voter `{voter}` voted for **{t_ign}** at `{v['created_at']}`")
            with col_v2:
                void_reason = st.text_input("Void reason", key=f"vr_{vid}", placeholder="Reason to void")
                if st.button("Void", key=f"void_{vid}"):
                    if not void_reason.strip():
                        st.error("Reason required.")
                    else:
                        void_vote_admin(vid, admin_user, void_reason.strip())
                        st.success("Vote voided.")
                        st.rerun()

    # ==========================================
    # 4. PHASE SETTINGS TAB
    # ==========================================
    with t_settings:
        st.subheader("Competition Phase Schedule (UTC)")
        settings = get_settings()

        st.markdown("Current scheduled times in UTC (ISO format: `YYYY-MM-DDTHH:MM:SSZ`):")

        sub_val = st.text_input("Submission Deadline (UTC)", value=settings.get("submission_deadline_utc", ""))
        v_start_val = st.text_input("Voting Start (UTC)", value=settings.get("voting_start_utc", ""))
        v_end_val = st.text_input("Voting End (UTC)", value=settings.get("voting_end_utc", ""))

        if st.button("Save Phase Times"):
            update_setting_admin("submission_deadline_utc", sub_val.strip(), admin_user)
            update_setting_admin("voting_start_utc", v_start_val.strip(), admin_user)
            update_setting_admin("voting_end_utc", v_end_val.strip(), admin_user)
            st.success("Phase times updated successfully!")
            st.rerun()

        # TEST_MODE tools (visible ONLY when TEST_MODE is True)
        if test_mode:
            st.markdown("---")
            st.markdown("### 🧪 TEST_MODE Phase Override")
            st.caption("Since TEST_MODE is enabled in secrets, you can force any competition phase for testing:")
            curr_override = settings.get("phase_override", "").strip().lower()
            options = ["", "submissions", "judging", "voting", "results"]
            choice = st.selectbox(
                "Select Forced Phase Override",
                options=options,
                index=options.index(curr_override) if curr_override in options else 0
            )

            if st.button("Apply Phase Override"):
                update_setting_admin("phase_override", choice, admin_user)
                st.success(f"Phase override set to '{choice or 'Real Clock'}'.")
                st.rerun()

    # ==========================================
    # 5. AUDIT LOGS & EXPORT
    # ==========================================
    with t_logs:
        st.subheader("Append-Only Admin Audit Log")
        logs = get_admin_logs()
        st.dataframe(logs, use_container_width=True)

        st.markdown("---")
        st.subheader("Data Export (CSV)")

        # Export entries
        entries = get_all_entries_admin()
        out_e = io.StringIO()
        w_e = csv.writer(out_e)
        w_e.writerow(["id", "governor_id", "ingame_name", "backstory", "quiz_score", "qualified", "hidden", "created_at"])
        for e in entries:
            w_e.writerow([e["id"], e["governor_id"], e["ingame_name"], e["backstory"], e["quiz_score"], e["qualified"], e["hidden"], e["created_at"]])

        st.download_button(
            label="📥 Download Submissions CSV",
            data=out_e.getvalue(),
            file_name="nxe_submissions.csv",
            mime="text/csv"
        )

        # Export votes
        votes = get_all_votes_admin()
        out_v = io.StringIO()
        w_v = csv.writer(out_v)
        w_v.writerow(["id", "voter_id", "entry_id", "created_at"])
        for v in votes:
            w_v.writerow([v["id"], v["voter_id"], v["entry_id"], v["created_at"]])

        st.download_button(
            label="📥 Download Votes CSV",
            data=out_v.getvalue(),
            file_name="nxe_votes.csv",
            mime="text/csv"
        )
