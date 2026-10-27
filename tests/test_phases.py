"""Unit tests for phases.py: UTC evaluations, formatting, and TEST_MODE overrides."""
from datetime import datetime, timezone, timedelta
from phases import evaluate_phase, CompetitionPhase, format_utc_display, format_countdown, parse_iso_utc


def test_phase_timeline():
    now_utc = datetime(2026, 10, 28, 12, 0, 0, tzinfo=timezone.utc)
    settings = {
        "submission_deadline_utc": "2026-10-29T14:00:00Z",
        "voting_start_utc": "2026-10-30T14:00:00Z",
        "voting_end_utc": "2026-10-31T14:00:00Z",
        "phase_override": ""
    }

    # Phase 1: Submissions
    p1, info1 = evaluate_phase(settings, test_mode=False, current_time_utc=now_utc)
    assert p1 == CompetitionPhase.SUBMISSIONS
    assert info1["target_label"] == "Submissions Close"

    # Phase 2: Judging
    p2, info2 = evaluate_phase(settings, test_mode=False, current_time_utc=datetime(2026, 10, 29, 15, 0, 0, tzinfo=timezone.utc))
    assert p2 == CompetitionPhase.JUDGING
    assert info2["target_label"] == "Voting Opens"

    # Phase 3: Voting
    p3, info3 = evaluate_phase(settings, test_mode=False, current_time_utc=datetime(2026, 10, 30, 16, 0, 0, tzinfo=timezone.utc))
    assert p3 == CompetitionPhase.VOTING
    assert info3["target_label"] == "Voting Closes"

    # Phase 4: Results
    p4, info4 = evaluate_phase(settings, test_mode=False, current_time_utc=datetime(2026, 11, 1, 10, 0, 0, tzinfo=timezone.utc))
    assert p4 == CompetitionPhase.RESULTS
    assert info4["target_time"] is None


def test_test_mode_phase_override():
    settings = {
        "submission_deadline_utc": "2026-10-29T14:00:00Z",
        "voting_start_utc": "2026-10-30T14:00:00Z",
        "voting_end_utc": "2026-10-31T14:00:00Z",
        "phase_override": "voting"
    }

    # When test_mode is False, override is ignored
    p_real, _ = evaluate_phase(settings, test_mode=False, current_time_utc=datetime(2026, 10, 28, 12, 0, 0, tzinfo=timezone.utc))
    assert p_real == CompetitionPhase.SUBMISSIONS

    # When test_mode is True, override is forced to VOTING
    p_over, info_over = evaluate_phase(settings, test_mode=True, current_time_utc=datetime(2026, 10, 28, 12, 0, 0, tzinfo=timezone.utc))
    assert p_over == CompetitionPhase.VOTING
    assert info_over["is_override"] is True
