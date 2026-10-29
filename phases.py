"""
Server-side phase logic driven by UTC timestamps stored in Supabase settings table.
Phases:
1. SUBMISSIONS: now until submission_deadline_utc
2. JUDGING: submission_deadline_utc until voting_start_utc
3. VOTING: voting_start_utc until voting_end_utc
4. RESULTS: after voting_end_utc
"""
from enum import Enum
from datetime import datetime, timezone


class CompetitionPhase(Enum):
    SUBMISSIONS = 1
    JUDGING = 2
    VOTING = 3
    RESULTS = 4

    @property
    def label(self) -> str:
        if self == CompetitionPhase.SUBMISSIONS:
            return "Phase 1: Submissions Open"
        elif self == CompetitionPhase.JUDGING:
            return "Phase 2: Ghostly Deliberation (Judging)"
        elif self == CompetitionPhase.VOTING:
            return "Phase 3: Community Voting"
        else:
            return "Phase 4: Grand Winner Revealed"

    @property
    def badge_color(self) -> str:
        if self == CompetitionPhase.SUBMISSIONS:
            return "#FF9A3C"  # Pumpkin Orange
        elif self == CompetitionPhase.JUDGING:
            return "#7CC8FF"  # Sky Blue
        elif self == CompetitionPhase.VOTING:
            return "#7CF2D0"  # Mint Green
        else:
            return "#FFD700"  # Gold


def parse_iso_utc(date_str: str) -> datetime | None:
    """Safely parses an ISO date string into a UTC timezone-aware datetime."""
    if not date_str:
        return None
    try:
        clean = date_str.strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def format_utc_display(dt: datetime | None) -> str:
    """Formats datetime clearly in UTC (e.g. '29 Oct 2026, 14:00 UTC')."""
    if not dt:
        return "N/A"
    return dt.strftime("%d %b %Y, %H:%M UTC")


def format_countdown(td) -> str:
    """Formats a timedelta into a clean mobile-friendly countdown string."""
    if not td or td.total_seconds() <= 0:
        return "00h 00m 00s"
    total_seconds = int(td.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"


def evaluate_phase(settings: dict, test_mode: bool = False, current_time_utc: datetime | None = None) -> tuple[CompetitionPhase, dict]:
    """
    Evaluates current phase strictly on the server clock in UTC.
    Honors phase_override ONLY if test_mode is True.
    """
    if current_time_utc is None:
        current_time_utc = datetime.now(timezone.utc)
    elif current_time_utc.tzinfo is None:
        current_time_utc = current_time_utc.replace(tzinfo=timezone.utc)

    # Check phase override when TEST_MODE is active
    override_val = settings.get("phase_override", "").strip().lower()
    if test_mode and override_val:
        override_map = {
            "submissions": CompetitionPhase.SUBMISSIONS,
            "judging": CompetitionPhase.JUDGING,
            "voting": CompetitionPhase.VOTING,
            "results": CompetitionPhase.RESULTS
        }
        if override_val in override_map:
            forced_phase = override_map[override_val]
            sub_d = parse_iso_utc(settings.get("submission_deadline_utc", "2026-10-29T14:00:00Z"))
            vot_s = parse_iso_utc(settings.get("voting_start_utc", "2026-10-30T14:00:00Z"))
            vot_e = parse_iso_utc(settings.get("voting_end_utc", "2026-10-31T14:00:00Z"))

            if forced_phase == CompetitionPhase.SUBMISSIONS:
                t_time = sub_d
                t_lbl = "Submissions Close (Preview)"
            elif forced_phase == CompetitionPhase.JUDGING:
                t_time = vot_s
                t_lbl = "Voting Opens (Preview)"
            elif forced_phase == CompetitionPhase.VOTING:
                t_time = vot_e
                t_lbl = "Voting Closes (Preview)"
            else:
                t_time = None
                t_lbl = "Competition Concluded (Preview)"

            rem = (t_time - current_time_utc) if (t_time and t_time > current_time_utc) else None

            can_sub = (forced_phase == CompetitionPhase.SUBMISSIONS)
            can_vot = (forced_phase == CompetitionPhase.VOTING)

            return forced_phase, {
                "phase": forced_phase,
                "current_time_utc": current_time_utc,
                "server_utc_str": current_time_utc.strftime("%d %b %Y, %H:%M UTC"),
                "target_time": t_time,
                "target_label": t_lbl,
                "countdown_str": format_countdown(rem) if rem else "PREVIEW ACTIVE",
                "is_override": True,
                "submission_deadline": sub_d,
                "voting_start": vot_s,
                "voting_end": vot_e,
                "can_submit": can_sub,
                "can_vote": can_vot,
            }

    sub_deadline = parse_iso_utc(settings.get("submission_deadline_utc", "2026-10-29T19:00:00Z"))
    voting_start = parse_iso_utc(settings.get("voting_start_utc", "2026-10-29T15:00:00Z"))
    voting_end = parse_iso_utc(settings.get("voting_end_utc", "2026-10-31T14:00:00Z"))

    can_submit = bool(sub_deadline and current_time_utc < sub_deadline)
    can_vote = bool(voting_start and voting_end and voting_start <= current_time_utc < voting_end)

    if voting_start and sub_deadline and voting_start <= sub_deadline:
        # Overlapping schedule: voting starts while submissions are still open
        if current_time_utc < voting_start:
            phase = CompetitionPhase.SUBMISSIONS
            target_time = voting_start
            target_label = "Voting Opens"
        elif current_time_utc < sub_deadline:
            phase = CompetitionPhase.VOTING
            target_time = sub_deadline
            target_label = "Submissions Close"
        elif voting_end and current_time_utc < voting_end:
            phase = CompetitionPhase.VOTING
            target_time = voting_end
            target_label = "Voting Closes"
        else:
            phase = CompetitionPhase.RESULTS
            target_time = None
            target_label = "Competition Concluded"
    else:
        # Sequential schedule: Submissions -> Judging -> Voting -> Results
        if sub_deadline and current_time_utc < sub_deadline:
            phase = CompetitionPhase.SUBMISSIONS
            target_time = sub_deadline
            target_label = "Submissions Close"
        elif voting_start and current_time_utc < voting_start:
            phase = CompetitionPhase.JUDGING
            target_time = voting_start
            target_label = "Voting Opens"
        elif voting_end and current_time_utc < voting_end:
            phase = CompetitionPhase.VOTING
            target_time = voting_end
            target_label = "Voting Closes"
        else:
            phase = CompetitionPhase.RESULTS
            target_time = None
            target_label = "Competition Concluded"

    remaining = (target_time - current_time_utc) if target_time else None

    return phase, {
        "phase": phase,
        "current_time_utc": current_time_utc,
        "server_utc_str": current_time_utc.strftime("%d %b %Y, %H:%M UTC"),
        "submission_deadline": sub_deadline,
        "voting_start": voting_start,
        "voting_end": voting_end,
        "target_time": target_time,
        "target_label": target_label,
        "countdown_str": format_countdown(remaining) if remaining else "00:00:00",
        "is_override": False,
        "can_submit": can_submit,
        "can_vote": can_vote,
    }
