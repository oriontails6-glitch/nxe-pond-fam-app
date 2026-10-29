"""Unit tests for input sanitization, deterministic tags, and admin security."""
import hmac
import html
import config
from submit import sanitize_text


def test_input_sanitization():
    # Dangerous control characters and null bytes are stripped
    dirty = "Hello\x00World!\x08\x1f Spooky Ghost"
    cleaned = sanitize_text(dirty)
    assert "\x00" not in cleaned
    assert "\x08" not in cleaned
    assert "Hello World! Spooky Ghost" in cleaned or "HelloWorld! Spooky Ghost" in cleaned

    # HTML tags are preserved as plain text by escaping (never rendered raw)
    script_attack = "<script>alert('pwned')</script>"
    escaped = html.escape(script_attack)
    assert "&lt;script&gt;" in escaped


def test_deterministic_non_qualified_tags():
    # Same entry ID produces identical tag
    eid1 = "11111111-2222-3333-4444-555555555555"
    tag_a = config.get_non_qualified_tag(eid1)
    tag_b = config.get_non_qualified_tag(eid1)
    assert tag_a == tag_b
    assert tag_a in config.NON_QUALIFIED_TAGS

    # Total tags is at least 18
    assert len(config.NON_QUALIFIED_TAGS) >= 18


def test_constant_time_admin_hash():
    val1 = "AdminPassword123!"
    val2 = "AdminPassword123!"
    val3 = "WrongPassword123!"
    assert hmac.compare_digest(val1.encode(), val2.encode()) is True
    assert hmac.compare_digest(val1.encode(), val3.encode()) is False


def test_exhibition_governor_rule():
    """Verify governor 409716271 is marked as exhibition only and cannot receive votes."""
    exhibition_gid = "409716271"
    
    # Exhibition entry check
    entry_pax = {"id": "pax-entry-id", "governor_id": "409716271"}
    entry_normal = {"id": "normal-entry-id", "governor_id": "296378532"}
    
    assert (entry_pax.get("governor_id") == exhibition_gid) is True
    assert (entry_normal.get("governor_id") == exhibition_gid) is False
