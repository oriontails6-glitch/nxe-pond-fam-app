"""
Cozy Storybook Halloween Theme for NXE Pond Fam.
Inspired by hand-drawn storybook Halloween illustrations:
- Soft twilight plum & warm harvest amber palette
- Custom vector storybook hero scene: Goggle Sheet-Ghost, Witchy Duck, and Chibi Baby Dragon with flower
- Frosted glassmorphism cards (no harsh neon borders)
- Tactile royal amethyst pill buttons & unified mobile segmented stepper
- Full mobile responsiveness with zero horizontal overflow
"""

def get_css(theme_name: str = "moonlit pond") -> str:
    css = """<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --bg-midnight: #0E071A;
    --card-surface: rgba(28, 15, 48, 0.78);
    --card-border: rgba(216, 180, 254, 0.14);
    --gold: #FBBF24;
    --gold-light: #FEF08A;
    --pumpkin: #F97316;
    --pumpkin-warm: #FB923C;
    --candy: #FBBF24;
    --slime: #34D399;
    --sky: #93C5FD;
    --text-primary: #FAF5EF;
    --text-secondary: #DDD6FE;
    --text-muted: #A78BFA;
    --amethyst-1: #7C3AED;
    --amethyst-2: #5B21B6;
    --amethyst-glow: rgba(124, 58, 237, 0.35);
}

/* Base Streamlit App Background */
.stApp {
    background: #0E071A !important;
    background-image: 
        radial-gradient(circle at 50% 0%, #29124A 0%, transparent 65%),
        radial-gradient(circle at 10% 40%, #1E0938 0%, transparent 45%),
        radial-gradient(circle at 90% 80%, #220B3E 0%, transparent 50%) !important;
    color: var(--text-primary);
    font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Prevent horizontal overflow on all devices */
html, body, [data-testid="stAppViewContainer"] {
    overflow-x: hidden !important;
    max-width: 100vw !important;
}

/* Hide default Streamlit chrome */
#MainMenu, header, footer, .stDeployButton {
    visibility: hidden !important;
    display: none !important;
}

/* Typography with Fredoka headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Fredoka', 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: #FAF5EF !important;
    letter-spacing: -0.2px;
}

.block-container {
    max-width: 660px !important;
    padding-top: 0.5rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 0.9rem !important;
    padding-right: 0.9rem !important;
}

/* ==============================================
   COZY STORYBOOK HERO BANNER
   ============================================== */
.storybook-hero-card {
    background: rgba(24, 12, 42, 0.85);
    border: 1px solid rgba(216, 180, 254, 0.18);
    border-radius: 26px;
    padding: 1rem 1rem 1.4rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.1rem;
    box-shadow: 0 14px 38px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.12);
}

.storybook-hero-scene {
    width: 100%;
    height: auto;
    border-radius: 20px;
    display: block;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    margin-bottom: 1rem;
}

.storybook-title {
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 2.15rem;
    font-weight: 800;
    color: #FFFDF5;
    text-shadow: 0 2px 10px rgba(251, 191, 36, 0.35);
    margin: 0.2rem 0 0.1rem 0;
    line-height: 1.15;
    letter-spacing: 0.5px;
}

.storybook-subtitle {
    font-family: 'Nunito', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #DDD6FE;
    margin-bottom: 0.6rem;
}

.storybook-badge {
    display: inline-block;
    background: rgba(245, 158, 11, 0.16);
    border: 1px solid #FBBF24;
    color: #FEF08A;
    font-family: 'Fredoka', sans-serif;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 3px 14px;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.25);
}

/* ==============================================
   PAPA MO SPONSOR CARD
   ============================================== */
.papamo-sponsor-card {
    background: linear-gradient(135deg, rgba(45, 18, 76, 0.82) 0%, rgba(26, 11, 46, 0.88) 100%) !important;
    border: 1px solid rgba(251, 191, 36, 0.32) !important;
    border-radius: 22px !important;
    padding: 1.15rem 1.35rem !important;
    margin-bottom: 1.2rem !important;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(251, 191, 36, 0.2) !important;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.papamo-badge {
    display: inline-block;
    background: rgba(251, 191, 36, 0.18);
    border: 1px solid #FBBF24;
    color: #FDE68A;
    font-family: 'Fredoka', sans-serif;
    font-weight: 700;
    font-size: 0.78rem;
    padding: 3px 12px;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.45rem;
}

.papamo-title {
    font-family: 'Fredoka', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #FDE047;
    margin: 0.1rem 0 0.25rem 0;
    text-shadow: 0 2px 8px rgba(253, 224, 71, 0.3);
}

.papamo-quote-box {
    background: rgba(18, 7, 33, 0.65);
    border-left: 3px solid #FBBF24;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin: 0.75rem 0 0.5rem 0;
    font-style: italic;
    color: #FAF5EF;
    font-size: 0.92rem;
    line-height: 1.45;
}

/* ==============================================
   COZY FROSTED GLASS CARDS
   ============================================== */
.pond-card {
    background: var(--card-surface) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 22px !important;
    padding: 1.3rem 1.25rem !important;
    margin-bottom: 1.15rem !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    position: relative;
    z-index: 2;
}

/* Phase Schedule Banner */
.phase-banner {
    background: rgba(28, 14, 48, 0.85);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(251, 191, 36, 0.3);
    border-radius: 18px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    position: relative;
    z-index: 2;
}

.phase-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ==============================================
   TACTILE ROYAL AMETHYST PILL BUTTONS
   ============================================== */
div.stButton > button:first-child {
    font-family: 'Fredoka', sans-serif !important;
    font-size: 1.04rem !important;
    font-weight: 600 !important;
    min-height: 48px !important;
    padding: 10px 22px !important;
    border-radius: 9999px !important;
    background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(216, 180, 254, 0.35) !important;
    box-shadow: 0 4px 16px rgba(124, 58, 237, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    transition: all 0.18s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35) !important;
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 6px 22px rgba(139, 92, 246, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
}

div.stButton > button:first-child:active {
    transform: translateY(1px) scale(0.98) !important;
}

/* Form Inputs (16px to prevent iOS auto-zoom) */
input, textarea, select {
    font-size: 16px !important;
    border-radius: 14px !important;
    background-color: rgba(18, 9, 32, 0.85) !important;
    color: #FAF5EF !important;
    border: 1px solid rgba(167, 139, 250, 0.25) !important;
    padding: 12px 14px !important;
    box-sizing: border-box !important;
}

input:focus, textarea:focus {
    border-color: #FBBF24 !important;
    box-shadow: 0 0 12px rgba(251, 191, 36, 0.35) !important;
}

/* ==============================================
   RESPONSIVE GALLERY CARDS & NO-OVERFLOW IMAGES
   ============================================== */
.gallery-item {
    background: rgba(28, 14, 48, 0.78);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.14);
    border-radius: 22px;
    padding: 1rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 8px 26px rgba(0, 0, 0, 0.35);
}

.gallery-card-details {
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
}

.gallery-card-details summary {
    list-style: none;
    cursor: pointer;
    outline: none;
}

.gallery-card-details summary::-webkit-details-marker {
    display: none;
}

.gallery-img-container {
    width: 100%;
    max-width: 100%;
    height: 250px;
    max-height: 250px;
    background: #0B0414;
    border-radius: 16px;
    border: 1px solid rgba(167, 139, 250, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.gallery-card-details:hover .gallery-img-container {
    border-color: #C084FC;
    transform: scale(1.008);
}

.gallery-fit-image {
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 12px;
    display: block;
}

.tap-reveal-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    background: rgba(124, 58, 237, 0.2);
    border: 1px solid rgba(167, 139, 250, 0.35);
    border-radius: 9999px;
    color: #DDD6FE;
    font-size: 0.82rem;
    font-weight: 600;
    padding: 5px 14px;
    margin: 8px auto 4px auto;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.gallery-card-details[open] .tap-reveal-pill {
    background: rgba(52, 211, 153, 0.2);
    border-color: #34D399;
    color: #6EE7B7;
}

.story-revealed-panel {
    background: rgba(16, 8, 28, 0.85);
    border: 1px solid rgba(167, 139, 250, 0.2);
    border-radius: 14px;
    padding: 0.85rem 1rem;
    margin-top: 8px;
    margin-bottom: 8px;
    animation: fadeInStory 0.22s ease-out;
}

@keyframes fadeInStory {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
}

.story-header {
    font-family: 'Fredoka', sans-serif;
    color: #FDE047;
    font-size: 0.92rem;
    font-weight: 700;
    margin-bottom: 3px;
}

.story-body {
    color: #FAF5EF;
    font-size: 0.9rem;
    line-height: 1.45;
    margin: 0;
}

.sticky-votes-chip {
    position: sticky;
    top: 0.5rem;
    z-index: 99;
    background: rgba(28, 14, 48, 0.94);
    backdrop-filter: blur(12px);
    border: 1px solid #FBBF24;
    border-radius: 9999px;
    padding: 8px 20px;
    text-align: center;
    font-family: 'Fredoka', sans-serif;
    font-size: 1.08rem;
    font-weight: 700;
    color: #FDE68A;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
    margin-bottom: 1.1rem;
}

.non-qualified-badge {
    background: rgba(59, 23, 94, 0.7);
    border: 1px solid rgba(192, 132, 252, 0.35);
    color: #E9D5FF;
    font-size: 0.82rem;
    font-weight: 700;
    border-radius: 10px;
    padding: 5px 12px;
    display: inline-block;
    margin-top: 6px;
}

/* ==============================================
   MOBILE RESPONSIVENESS (< 600px)
   ============================================== */
@media (max-width: 600px) {
    .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-top: 0.3rem !important;
        padding-bottom: 2.5rem !important;
    }
    .storybook-hero-card {
        padding: 0.85rem 0.65rem 1.1rem 0.65rem !important;
        border-radius: 20px !important;
        margin-bottom: 0.85rem !important;
    }
    .storybook-title {
        font-size: 1.65rem !important;
    }
    .storybook-subtitle {
        font-size: 0.88rem !important;
    }
    .papamo-sponsor-card {
        padding: 0.95rem 1rem !important;
        border-radius: 18px !important;
        margin-bottom: 0.9rem !important;
    }
    .papamo-title {
        font-size: 1.18rem !important;
    }
    .pond-card {
        padding: 0.95rem !important;
        border-radius: 18px !important;
        margin-bottom: 0.85rem !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0.25rem !important;
    }
    div[data-testid="column"] {
        min-width: 0 !important;
        padding: 0 !important;
    }
    div.stButton > button:first-child {
        font-size: 0.86rem !important;
        padding: 8px 6px !important;
        min-height: 42px !important;
        white-space: nowrap !important;
        border-radius: 12px !important;
    }
    .phase-banner {
        padding: 0.65rem 0.8rem !important;
        border-radius: 14px !important;
        font-size: 0.86rem !important;
        margin-bottom: 0.85rem !important;
    }
    .gallery-img-container {
        height: 215px !important;
        max-height: 215px !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    div.stButton > button:first-child {
        animation: none !important;
        transition: none !important;
        transform: none !important;
    }
}
</style>"""
    return css.strip()


def get_floating_ghosts_html() -> str:
    """Soft ambient background stars and floating mist (GPU friendly)."""
    return """<div style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;overflow:hidden;" aria-hidden="true"></div>"""


def get_storybook_header_svg() -> str:

    """
    Returns the custom storybook vector scene inspired by Pinterest Inspo 4 & 5:
    - Glowing Harvest Moon in a star-dusted night sky
    - 1. The Goggle Sheet-Ghost with sweet smile (Inspo 4)
    - 2. The Witchy Yellow Duckling with purple hat & stars
    - 3. The Chibi Baby Dragon with flower (Inspo 5)
    - 4. Smiling carved Jack-o'-Lanterns in the meadow (Inspo 5)
    """
    svg = """<svg viewBox="0 0 600 240" fill="none" xmlns="http://www.w3.org/2000/svg" class="storybook-hero-scene">
  <defs>
    <linearGradient id="skyGrad" x1="300" y1="0" x2="300" y2="240" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1B0C33"/>
      <stop offset="60%" stop-color="#2D144F"/>
      <stop offset="100%" stop-color="#140826"/>
    </linearGradient>
    <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFDF0"/>
      <stop offset="45%" stop-color="#FEF08A"/>
      <stop offset="80%" stop-color="#FBBF24" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#FBBF24" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="duckGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FDE047"/>
      <stop offset="100%" stop-color="#EAB308"/>
    </linearGradient>
    <linearGradient id="ghostGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F1ECFA"/>
    </linearGradient>
    <linearGradient id="dragonGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#C084FC"/>
      <stop offset="100%" stop-color="#9333EA"/>
    </linearGradient>
    <linearGradient id="pumpGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FB923C"/>
      <stop offset="100%" stop-color="#EA580C"/>
    </linearGradient>
  </defs>

  <!-- Sky Canvas -->
  <rect width="600" height="240" rx="20" fill="url(#skyGrad)"/>

  <!-- Soft Ambient Clouds / Mist -->
  <path d="M0 90 Q 90 70 200 85 T 400 75 T 600 85 L 600 240 L 0 240 Z" fill="#240F3E" opacity="0.45"/>
  <path d="M0 130 Q 140 115 310 130 T 600 125 L 600 240 L 0 240 Z" fill="#1C0A33" opacity="0.7"/>

  <!-- Glowing Harvest Moon -->
  <circle cx="300" cy="72" r="58" fill="url(#moonGlow)"/>
  <circle cx="300" cy="72" r="38" fill="#FFFDF5"/>
  <circle cx="300" cy="72" r="38" fill="#FEF08A" opacity="0.5"/>
  <circle cx="312" cy="62" r="7" fill="#FDE047" opacity="0.35"/>
  <circle cx="292" cy="80" r="9" fill="#FDE047" opacity="0.3"/>
  <circle cx="304" cy="86" r="4" fill="#FDE047" opacity="0.25"/>

  <!-- Storybook 4-Point Stars -->
  <path d="M80 40 Q80 48 72 48 Q80 48 80 56 Q80 48 88 48 Q80 48 80 40 Z" fill="#FEF08A"/>
  <path d="M140 28 Q140 34 134 34 Q140 34 140 40 Q140 34 146 34 Q140 34 140 28 Z" fill="#FEF08A" opacity="0.8"/>
  <path d="M480 35 Q480 43 472 43 Q480 43 480 51 Q480 43 488 43 Q480 43 480 35 Z" fill="#FEF08A"/>
  <path d="M530 52 Q530 57 525 57 Q530 57 530 62 Q530 57 535 57 Q530 57 530 52 Z" fill="#FEF08A" opacity="0.75"/>
  <path d="M220 30 Q220 35 215 35 Q220 35 220 40 Q220 35 225 35 Q220 35 220 30 Z" fill="#FEF08A" opacity="0.85"/>
  <path d="M390 26 Q390 32 384 32 Q390 32 390 38 Q390 32 396 32 Q390 32 390 26 Z" fill="#FEF08A" opacity="0.9"/>

  <!-- Tiny Distant Bats (Inspo 5) -->
  <path d="M100 70 Q106 64 112 70 Q118 64 124 70 Q118 73 112 71 Q106 73 100 70 Z" fill="#140624" opacity="0.55"/>
  <path d="M490 65 Q495 60 500 65 Q505 60 510 65 Q505 68 500 66 Q495 68 490 65 Z" fill="#140624" opacity="0.55"/>

  <!-- Grassy Embankment Base -->
  <path d="M0 190 Q 150 170 300 178 T 600 174 L 600 240 L 0 240 Z" fill="#170B2B"/>
  <path d="M0 205 Q 160 195 320 202 T 600 198 L 600 240 L 0 240 Z" fill="#100720"/>

  <!-- 1. GOGGLE SHEET GHOST (Pinterest Inspo 4) -->
  <g transform="translate(145, 95)">
    <path d="M38 18 C18 18 10 38 8 68 C7 82 4 98 10 102 C15 105 20 96 26 99 C32 102 36 94 42 98 C48 101 54 94 60 98 C66 102 70 88 68 68 C66 38 58 18 38 18 Z" fill="url(#ghostGrad)" stroke="#4A2674" stroke-width="2.5" stroke-linejoin="round"/>
    <path d="M22 68 Q24 88 20 97" stroke="#DDD6FE" stroke-width="2" stroke-linecap="round"/>
    <path d="M42 66 Q40 86 42 96" stroke="#DDD6FE" stroke-width="2" stroke-linecap="round"/>
    <path d="M55 64 Q53 82 58 94" stroke="#DDD6FE" stroke-width="2" stroke-linecap="round"/>
    <!-- Cute Goggles -->
    <path d="M8 48 Q38 46 68 48" stroke="#311347" stroke-width="3" stroke-linecap="round"/>
    <circle cx="28" cy="48" r="10" fill="#FAF5EF" stroke="#311347" stroke-width="3"/>
    <circle cx="28" cy="48" r="7.5" fill="#1E0B36"/>
    <circle cx="25" cy="45" r="2.2" fill="#FFFFFF"/>
    <line x1="38" y1="48" x2="42" y2="48" stroke="#311347" stroke-width="3"/>
    <circle cx="50" cy="48" r="10" fill="#FAF5EF" stroke="#311347" stroke-width="3"/>
    <circle cx="50" cy="48" r="7.5" fill="#1E0B36"/>
    <circle cx="47" cy="45" r="2.2" fill="#FFFFFF"/>
    <!-- Cheeks & Smile -->
    <ellipse cx="18" cy="62" rx="4" ry="2.5" fill="#F472B6" opacity="0.6"/>
    <ellipse cx="60" cy="62" rx="4" ry="2.5" fill="#F472B6" opacity="0.6"/>
    <path d="M34 62 Q39 67 44 62" stroke="#311347" stroke-width="2.5" stroke-linecap="round"/>
  </g>

  <!-- 2. WITCHY YELLOW DUCKLING (Center Mascot) -->
  <g transform="translate(262, 92)">
    <ellipse cx="38" cy="74" rx="28" ry="22" fill="url(#duckGrad)" stroke="#4A2674" stroke-width="2.5"/>
    <path d="M12 70 Q2 65 6 76 Q12 80 18 76 Z" fill="#EAB308"/>
    <ellipse cx="32" cy="74" rx="13" ry="9" transform="rotate(-8 32 74)" fill="#FACC15" stroke="#4A2674" stroke-width="2"/>
    <circle cx="46" cy="50" r="19" fill="url(#duckGrad)" stroke="#4A2674" stroke-width="2.5"/>
    <ellipse cx="50" cy="46" rx="4.5" ry="6" fill="#1E0A38"/>
    <circle cx="52" cy="44" r="2" fill="#FFFFFF"/>
    <circle cx="49" cy="48" r="1" fill="#FFFFFF"/>
    <path d="M57 50 Q70 52 66 58 Q57 60 53 54 Z" fill="#F97316" stroke="#4A2674" stroke-width="2"/>
    <ellipse cx="42" cy="54" rx="3.5" ry="2" fill="#F472B6" opacity="0.6"/>
    <!-- Crooked Witch Hat -->
    <polygon points="46,12 30,34 68,34" fill="#581C87" stroke="#3B0764" stroke-width="2.5"/>
    <ellipse cx="48" cy="34" rx="19" ry="4.5" fill="#6B21A8" stroke="#3B0764" stroke-width="2"/>
    <rect x="38" y="30" width="18" height="3" fill="#F59E0B"/>
    <rect x="44" y="29.5" width="6" height="4" fill="#FEF08A"/>
  </g>

  <!-- 3. CHIBI BABY DRAGON WITH FLOWER (Pinterest Inspo 5) -->
  <g transform="translate(378, 102)">
    <ellipse cx="36" cy="65" rx="21" ry="20" fill="url(#dragonGrad)" stroke="#3B0764" stroke-width="2.5"/>
    <ellipse cx="42" cy="68" rx="13" ry="12" fill="#E9D5FF"/>
    <path d="M16 70 Q5 76 9 86 Q15 84 18 78 Z" fill="#7E22CE"/>
    <polygon points="4,88 10,82 14,88" fill="#F59E0B"/>
    <circle cx="44" cy="42" r="17" fill="url(#dragonGrad)" stroke="#3B0764" stroke-width="2.5"/>
    <polygon points="34,22 36,32 30,32" fill="#FBBF24" stroke="#3B0764" stroke-width="1.8"/>
    <polygon points="46,20 48,30 42,30" fill="#FBBF24" stroke="#3B0764" stroke-width="1.8"/>
    <ellipse cx="49" cy="40" rx="4.5" ry="5.5" fill="#18072B"/>
    <circle cx="51" cy="38" r="1.8" fill="#FFFFFF"/>
    <ellipse cx="56" cy="46" rx="7" ry="5" fill="#A855F7"/>
    <path d="M54 48 Q57 51 60 48" stroke="#4C1D95" stroke-width="1.8" stroke-linecap="round"/>
    <path d="M26 55 Q14 42 22 35 Q30 41 27 55 Z" fill="#D8B4FE" stroke="#3B0764" stroke-width="2"/>
    <!-- Autumn Flower (Inspo 5) -->
    <circle cx="58" cy="62" r="3" fill="#F59E0B"/>
    <circle cx="56" cy="60" r="2.5" fill="#FB923C"/>
    <circle cx="60" cy="60" r="2.5" fill="#FB923C"/>
    <circle cx="58" cy="65" r="2.5" fill="#FB923C"/>
    <line x1="58" y1="65" x2="56" y2="72" stroke="#4ADE80" stroke-width="2"/>
  </g>

  <!-- 4. CARVED SMILING PUMPKINS (Inspo 5) -->
  <g transform="translate(90, 168)">
    <ellipse cx="24" cy="20" rx="20" ry="16" fill="url(#pumpGrad)" stroke="#431407" stroke-width="2"/>
    <ellipse cx="24" cy="20" rx="13" ry="16" fill="#F97316"/>
    <path d="M22 4 Q23 0 27 2 L25 5 Z" fill="#22C55E"/>
    <polygon points="16,15 20,20 13,20" fill="#FEF08A"/>
    <polygon points="32,15 35,20 28,20" fill="#FEF08A"/>
    <path d="M16 26 Q24 32 32 26 Q28 29 24 28 Q20 29 16 26 Z" fill="#FEF08A"/>
  </g>
  <g transform="translate(485, 164)">
    <ellipse cx="22" cy="18" rx="18" ry="15" fill="url(#pumpGrad)" stroke="#431407" stroke-width="2"/>
    <ellipse cx="22" cy="18" rx="12" ry="15" fill="#F97316"/>
    <path d="M20 3 Q21 0 25 1 L23 4 Z" fill="#22C55E"/>
    <polygon points="15,13 19,18 13,18" fill="#FEF08A"/>
    <polygon points="29,13 32,18 26,18" fill="#FEF08A"/>
    <path d="M15 24 Q22 29 29 24 Q26 27 22 26 Q18 27 15 24 Z" fill="#FEF08A"/>
  </g>
</svg>"""
    return svg.strip()
