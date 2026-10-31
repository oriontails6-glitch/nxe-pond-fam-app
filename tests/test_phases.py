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


def test_overlapping_schedule():
    """Tests overlapping schedule: voting starts at 15:00 UTC, submissions close at 19:00 UTC, voting closes at 19:00 UTC 31 Oct."""
    settings = {
        "submission_deadline_utc": "2026-10-29T19:00:00Z",
        "voting_start_utc": "2026-10-29T15:00:00Z",
        "voting_end_utc": "2026-10-31T19:00:00Z",
        "phase_override": ""
    }

    # 14:30 UTC: Submissions open, Voting not yet open
    t1 = datetime(2026, 10, 29, 14, 30, 0, tzinfo=timezone.utc)
    p1, info1 = evaluate_phase(settings, current_time_utc=t1)
    assert p1 == CompetitionPhase.SUBMISSIONS
    assert info1["can_submit"] is True
    assert info1["can_vote"] is False
    assert info1["target_label"] == "Voting Opens"

    # 16:00 UTC: Overlap period! Voting IS OPEN and Submissions ARE ALSO OPEN
    t2 = datetime(2026, 10, 29, 16, 0, 0, tzinfo=timezone.utc)
    p2, info2 = evaluate_phase(settings, current_time_utc=t2)
    assert p2 == CompetitionPhase.VOTING
    assert info2["can_submit"] is True
    assert info2["can_vote"] is True
    assert info2["target_label"] == "Submissions Close"

    # 20:00 UTC: Submissions closed, Voting remains open
    t3 = datetime(2026, 10, 29, 20, 0, 0, tzinfo=timezone.utc)
    p3, info3 = evaluate_phase(settings, current_time_utc=t3)
    assert p3 == CompetitionPhase.VOTING
    assert info3["can_submit"] is False
    assert info3["can_vote"] is True
    assert info3["target_label"] == "Voting Closes"

    # Post voting: Results
    t4 = datetime(2026, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
    p4, info4 = evaluate_phase(settings, current_time_utc=t4)
    assert p4 == CompetitionPhase.RESULTS
    assert info4["can_submit"] is False
    assert info4["can_vote"] is False
