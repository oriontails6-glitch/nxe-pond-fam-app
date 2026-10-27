"""
Configuration and constants for NXE Pond Fam Halloween App.
"""

# Theme switch: "moonlit pond" (default) or "sky" (fallback light palette)
THEME = "moonlit pond"

# Alliance name
ALLIANCE_NAME = "NXE"
APP_TITLE = "NXE Pond Fam: Spooky Halloween Costume Arena"

# Default test Governor ID
TEST_GOVERNOR_ID = "296378532"

# Voting rules
VOTES_PER_VOTER = 3

# Quiz rules
QUIZ_QUESTIONS_PER_ATTEMPT = 5
QUIZ_MAX_ATTEMPTS = 3
QUIZ_COOLDOWN_SECONDS = 30
QUIZ_QUALIFYING_SCORE = 3

# Submission rules
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB
IMAGE_LONG_SIDE_MAX = 1080
THUMB_WIDTH = 480
WEBP_QUALITY = 80
BACKSTORY_MAX_CHARS = 500
INGAME_NAME_MAX_CHARS = 30

# Rate limits
LOGIN_MAX_FAILED_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 10

# Session token expiration
SESSION_TOKEN_EXPIRY_HOURS = 24
ADMIN_SESSION_EXPIRY_HOURS = 2

# Deterministic funny tags for non-qualified entries (18 total)
NON_QUALIFIED_TAGS = [
    "📚 I did not read the books, vibes only",
    "🐸 Failed the lore, passed the cuteness",
    "🦆 Quack-uated with zero lore marks",
    "👻 Boo-ks? Never heard of them",
    "🪷 Just here for the costume",
    "🎃 Lore score: pumpkin spice",
    "🧙 Wizard school dropout, outfit still legendary",
    "🐊 Skipped the reading, ate the snacks",
    "🍂 Blew off the exam, mastered the swagger",
    "✨ Pure aura, zero percent textbook",
    "🦇 The bats told me the wrong answers",
    "🛶 Lost my study guide in the reeds",
    "🍄 Educated by mushrooms, dressed by royalty",
    "📜 Signed my test scroll in invisible kelp ink",
    "☕ Overdosed on espresso pellets before the exam",
    "🕸️ Tangled in cobwebs, skipped the revision",
    "👑 Crown is on, brain is off",
    "🍕 In an alliance with Don Pengucci's tacos instead"
]


def get_non_qualified_tag(entry_id_str: str) -> str:
    """Deterministically selects a fun tag based on entry UUID."""
    val = sum(ord(c) for c in str(entry_id_str))
    return NON_QUALIFIED_TAGS[val % len(NON_QUALIFIED_TAGS)]
