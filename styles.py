"""
Professional Halloween UI Theme for NXE Pond Fam.
Inspired by modern flat/paper-cut Halloween game art:
- Rich royal twilight purple & warm autumn pumpkin orange palette
- Crisp vector illustrations: Yellow Cartoon Duck, Cute Baby Dragon, and Playful Pond Fish
- Layered paper-cut cards, glowing buttons, and mobile-first responsive layout
"""

def get_css(theme_name: str = "moonlit pond") -> str:
    # Palette matching the uploaded reference banners:
    # Deep twilight purple, glowing amber-orange, soft violet, pure white
    bg_deep = "#16092B"          # Midnight blackberry purple
    bg_surface = "#231140"       # Layered violet card surface
    card_border = "#49227A"      # Crisp glowing purple border
    card_accent_orange = "#FF7A00" # Rich pumpkin orange
    text_white = "#FFFFFF"       # Crisp header white
    text_sub = "#D6C7EB"         # Soft lilac body text
    pumpkin_glow = "rgba(255, 122, 0, 0.45)"
    purple_glow = "rgba(157, 78, 221, 0.35)"

    css = f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:wght@400;600;700;800&display=swap');

:root {{
    --bg-deep: #16092B;
    --bg-surface: #231140;
    --border-purple: #49227A;
    --orange-primary: #FF7A00;
    --pumpkin: #FF7A00;
    --candy: #FFD166;
    --slime: #7CF2D0;
    --sky: #7CC8FF;
    --text-main: #FFFFFF;
    --text-primary: #FFFFFF;
    --text-muted: #D6C7EB;
    --text-secondary: #D6C7EB;
    --pumpkin-glow: rgba(255, 122, 0, 0.45);
    --purple-glow: rgba(157, 78, 221, 0.35);
}}

/* Base Streamlit App Background */
.stApp {{
    background: {bg_deep};
    background-image: 
        radial-gradient(circle at 50% 0%, #35145E 0%, transparent 65%),
        radial-gradient(circle at 15% 45%, #250C44 0%, transparent 45%),
        radial-gradient(circle at 85% 85%, #2B0D52 0%, transparent 50%);
    color: var(--text-main);
    font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
}}

/* Hide default Streamlit chrome */
#MainMenu, header, footer, .stDeployButton {{
    visibility: hidden !important;
    display: none !important;
}}

/* Crisp Typography with Fredoka */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Fredoka', 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.2px;
}}

.block-container {{
    max-width: 720px !important;
    padding-top: 0.6rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 0.9rem !important;
    padding-right: 0.9rem !important;
}}

/* Modern Vector Hero Banner (Paper-Cut Style matching Reference 1 & 2) */
.vector-halloween-hero {{
    background: linear-gradient(180deg, #441875 0%, #2A0F50 100%);
    border: 3px solid #6E2EB5;
    border-radius: 28px;
    padding: 1.6rem 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.2rem;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45), inset 0 2px 0 rgba(255, 255, 255, 0.15);
}}

.hero-full-moon {{
    position: absolute;
    top: -25px;
    left: 50%;
    transform: translateX(-50%);
    width: 130px;
    height: 130px;
    background: radial-gradient(circle, #FFF8E1 40%, #FFE082 85%, rgba(255, 224, 130, 0) 100%);
    border-radius: 50%;
    box-shadow: 0 0 45px rgba(255, 224, 130, 0.6);
    z-index: 1;
    pointer-events: none;
}}

.hero-title-box {{
    position: relative;
    z-index: 2;
}}

.hero-halloween-title {{
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 2.25rem;
    font-weight: 800;
    color: #FF9E00;
    text-shadow: 0 3px 0 #9E2A00, 0 0 25px rgba(255, 158, 0, 0.6);
    margin: 0;
    line-height: 1.15;
    letter-spacing: 0.5px;
}}

.hero-sub-badge {{
    display: inline-block;
    background: linear-gradient(90deg, #FF7A00, #FF5100);
    color: #FFFFFF;
    font-family: 'Fredoka', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 4px 14px;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.5rem;
    box-shadow: 0 4px 12px rgba(255, 81, 0, 0.4);
}}

/* Professional Layered Paper-Cut Cards */
.pond-card {{
    background: linear-gradient(180deg, #241142 0%, #1A0B33 100%);
    border: 2px solid #532587;
    border-radius: 24px;
    padding: 1.35rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 2;
}}

.pumpkin-accent-card {{
    border: 2px solid #FF8500 !important;
    background: linear-gradient(180deg, #30144A 0%, #1D0B33 100%) !important;
    box-shadow: 0 8px 30px rgba(255, 133, 0, 0.25) !important;
}}

/* Phase Schedule Banner */
.phase-banner {{
    background: linear-gradient(135deg, #2C104F 0%, #1A0935 100%);
    border: 2px solid #FF9500;
    border-radius: 20px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 6px 20px rgba(255, 149, 0, 0.25);
    position: relative;
    z-index: 2;
}}

.phase-badge {{
    display: inline-block;
    padding: 5px 14px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Elegant Royal Amethyst Pill Buttons (Replaces bright orange) */
div.stButton > button:first-child {{
    font-family: 'Fredoka', sans-serif !important;
    font-size: 1.08rem !important;
    font-weight: 700 !important;
    min-height: 48px !important;
    padding: 10px 24px !important;
    border-radius: 9999px !important;
    background: linear-gradient(180deg, #7C3AED 0%, #6D28D9 55%, #4C1D95 100%) !important;
    color: #FFFFFF !important;
    border: 2px solid #C4B5FD !important;
    box-shadow: 0 4px 16px rgba(109, 40, 217, 0.45), inset 0 2px 0 rgba(255, 255, 255, 0.25) !important;
    transition: all 0.18s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}}

div.stButton > button:first-child:hover {{
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 6px 22px rgba(139, 92, 246, 0.65), inset 0 2px 0 rgba(255, 255, 255, 0.35) !important;
    background: linear-gradient(180deg, #8B5CF6 0%, #7C3AED 55%, #5B21B6 100%) !important;
    border-color: #DDD6FE !important;
}}

div.stButton > button:first-child:active {{
    transform: translateY(1px) scale(0.98) !important;
}}

/* Form Inputs (16px to prevent iOS auto-zoom) */
input, textarea, select {{
    font-size: 16px !important;
    border-radius: 16px !important;
    background-color: #190B30 !important;
    color: #FFFFFF !important;
    border: 2px solid #4D217D !important;
    padding: 12px 16px !important;
}}

input:focus, textarea:focus {{
    border-color: #FF9E00 !important;
    box-shadow: 0 0 15px rgba(255, 158, 0, 0.4) !important;
}}

/* Sticky Mobile Chip for Votes */
.sticky-votes-chip {{
    position: sticky;
    top: 0.5rem;
    z-index: 99;
    background: rgba(36, 17, 66, 0.95);
    backdrop-filter: blur(10px);
    border: 2px solid #FF9500;
    border-radius: 9999px;
    padding: 10px 22px;
    text-align: center;
    font-family: 'Fredoka', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #FFD166;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.5);
    margin-bottom: 1.2rem;
}}

/* Gallery Item Cards */
.gallery-item {{
    background: linear-gradient(180deg, #2A134D 0%, #1C0B35 100%);
    border: 2px solid #542588;
    border-radius: 24px;
    padding: 1.1rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}}

/* Responsive Mobile-Friendly Gallery Card & Image Fitting (No overflow on phone) */
.gallery-card-details {{
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
}}

.gallery-card-details summary {{
    list-style: none;
    cursor: pointer;
    outline: none;
}}

.gallery-card-details summary::-webkit-details-marker {{
    display: none;
}}

.gallery-img-container {{
    width: 100%;
    max-width: 100%;
    height: 280px;
    max-height: 280px;
    background: #110522;
    border-radius: 18px;
    border: 2px solid #4D217D;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.6);
    transition: transform 0.2s ease, border-color 0.2s ease;
}}

.gallery-card-details:hover .gallery-img-container {{
    border-color: #A78BFA;
    transform: scale(1.008);
}}

.gallery-fit-image {{
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 14px;
    display: block;
}}

.tap-reveal-pill {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    background: rgba(124, 58, 237, 0.25);
    border: 1px solid #7C3AED;
    border-radius: 9999px;
    color: #DDD6FE;
    font-size: 0.84rem;
    font-weight: 600;
    padding: 5px 14px;
    margin: 8px auto 4px auto;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.gallery-card-details[open] .tap-reveal-pill {{
    background: rgba(52, 211, 153, 0.2);
    border-color: #34D399;
    color: #6EE7B7;
}}

.story-revealed-panel {{
    background: linear-gradient(180deg, #1D0C33 0%, #150826 100%);
    border: 1px solid #5B21B6;
    border-radius: 16px;
    padding: 0.9rem 1.1rem;
    margin-top: 8px;
    margin-bottom: 8px;
    animation: fadeInStory 0.25s ease-out;
}}

@keyframes fadeInStory {{
    from {{ opacity: 0; transform: translateY(-6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.story-header {{
    font-family: 'Fredoka', sans-serif;
    color: #FBBF24;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 4px;
}}

.story-body {{
    color: #E2E8F0;
    font-size: 0.92rem;
    line-height: 1.45;
    margin: 0;
}}

/* Clean Minimal Step Wizard Bar */
.step-stepper-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #1D0B33;
    border: 1px solid #4D217D;
    border-radius: 9999px;
    padding: 6px 10px;
    margin-bottom: 1.2rem;
}}

.step-chip {{
    flex: 1;
    text-align: center;
    font-size: 0.82rem;
    font-weight: 700;
    color: #A78BFA;
    padding: 6px 4px;
    border-radius: 9999px;
    transition: all 0.2s ease;
}}

.step-chip.active {{
    background: linear-gradient(180deg, #7C3AED 0%, #5B21B6 100%);
    color: #FFFFFF;
    box-shadow: 0 2px 10px rgba(124, 58, 237, 0.5);
}}

.non-qualified-badge {{
    background: #39175C;
    border: 1px solid #9D4EDD;
    color: #E0AAFF;
    font-size: 0.85rem;
    font-weight: 700;
    border-radius: 12px;
    padding: 6px 12px;
    display: inline-block;
    margin-top: 8px;
}}

/* Character Showcase Strip (Yellow Ducks, Fishes, Baby Dragons) */
.creature-strip {{
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: rgba(40, 18, 73, 0.6);
    border: 1px solid #572A8C;
    border-radius: 20px;
    padding: 0.8rem 0.5rem;
    margin-bottom: 1.2rem;
}}

/* Floating Cartoon Ducks, Dragons, Fishes, and Pumpkins Layer */
.pond-creatures-layer {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none !important;
    z-index: 1;
    overflow: hidden;
}}

@keyframes floatCreature1 {{
    0% {{ transform: translate(0, 0) rotate(0deg); }}
    50% {{ transform: translate(18px, -24px) rotate(4deg); }}
    100% {{ transform: translate(0, 0) rotate(0deg); }}
}}

@keyframes floatCreature2 {{
    0% {{ transform: translate(0, 0) rotate(0deg); }}
    50% {{ transform: translate(-20px, -28px) rotate(-4deg); }}
    100% {{ transform: translate(0, 0) rotate(0deg); }}
}}

@keyframes fishSwim {{
    0% {{ transform: translate(0, 0) scaleX(1); }}
    50% {{ transform: translate(25px, -15px) scaleX(1); }}
    51% {{ transform: translate(25px, -15px) scaleX(-1); }}
    100% {{ transform: translate(0, 0) scaleX(-1); }}
}}

.anim-duck {{
    position: absolute;
    top: 14%;
    right: 6%;
    width: 68px;
    animation: floatCreature1 6.5s ease-in-out infinite;
}}

.anim-dragon {{
    position: absolute;
    top: 48%;
    left: 4%;
    width: 72px;
    animation: floatCreature2 7s ease-in-out infinite 0.5s;
}}

.anim-fish {{
    position: absolute;
    bottom: 40px;
    left: 12%;
    width: 58px;
    animation: fishSwim 9s ease-in-out infinite;
}}

.anim-pumpkin {{
    position: absolute;
    bottom: 25px;
    right: 10%;
    width: 62px;
    animation: floatCreature1 5s ease-in-out infinite 1s;
}}

/* Prevent horizontal overflow on all mobile screens */
html, body, [data-testid="stAppViewContainer"] {{
    overflow-x: hidden !important;
    max-width: 100vw !important;
}}

/* Comprehensive Mobile Responsiveness (360px - 600px phones) */
@media (max-width: 600px) {{
    .block-container {{
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-top: 0.35rem !important;
        padding-bottom: 2rem !important;
    }}
    .vector-halloween-hero {{
        padding: 1.1rem 0.6rem !important;
        border-radius: 18px !important;
        margin-bottom: 0.8rem !important;
    }}
    .hero-halloween-title {{
        font-size: 1.55rem !important;
        letter-spacing: -0.2px !important;
    }}
    .hero-sub-badge {{
        font-size: 0.75rem !important;
        padding: 3px 10px !important;
    }}
    .hero-full-moon {{
        width: 85px !important;
        height: 85px !important;
    }}
    .creature-strip {{
        padding: 0.45rem 0.3rem !important;
        border-radius: 14px !important;
        margin-bottom: 0.8rem !important;
    }}
    div[data-testid="stHorizontalBlock"] {{
        gap: 0.25rem !important;
    }}
    div[data-testid="column"] {{
        min-width: 0 !important;
        padding: 0 !important;
    }}
    div.stButton > button:first-child {{
        font-size: 0.86rem !important;
        padding: 8px 6px !important;
        min-height: 42px !important;
        white-space: nowrap !important;
        border-radius: 12px !important;
    }}
    .phase-banner {{
        padding: 0.65rem 0.8rem !important;
        border-radius: 16px !important;
        font-size: 0.86rem !important;
        margin-bottom: 0.8rem !important;
    }}
    .gallery-img-container {{
        height: 220px !important;
        max-height: 220px !important;
        border-radius: 14px !important;
    }}
    .gallery-item {{
        padding: 0.8rem !important;
        border-radius: 18px !important;
        margin-bottom: 1rem !important;
    }}
    .pond-card {{
        padding: 0.9rem !important;
        border-radius: 18px !important;
        margin-bottom: 0.9rem !important;
    }}
    input, textarea, select {{
        font-size: 16px !important;
        padding: 10px 12px !important;
        border-radius: 12px !important;
    }}
    .sticky-votes-chip {{
        padding: 7px 16px !important;
        font-size: 1rem !important;
        margin-bottom: 0.8rem !important;
    }}
    .anim-duck {{
        width: 44px !important;
        top: 8% !important;
        right: 2% !important;
    }}
    .anim-dragon {{
        width: 46px !important;
        left: 2% !important;
        top: 55% !important;
    }}
    .anim-pumpkin {{
        width: 40px !important;
        right: 3% !important;
        bottom: 15px !important;
    }}
    .anim-fish {{
        display: none !important;
    }}
}}

@media (prefers-reduced-motion: reduce) {{
    .anim-duck, .anim-dragon, .anim-fish, .anim-pumpkin, div.stButton > button:first-child {{
        animation: none !important;
        transition: none !important;
        transform: none !important;
    }}
}}
</style>"""
    return css.strip()


def get_floating_ghosts_html() -> str:
    """
    Returns crisp vector SVG illustrations:
    1. Cute Yellow Cartoon Duck with orange bill and witch hat
    2. Adorable Baby Dragon with wings and friendly horns
    3. Playful Pond Fish with bubble trail
    4. Glowing Jack-o'-Lantern from Reference 1
    """
    html_str = """<div class="pond-creatures-layer" aria-hidden="true">
<!-- 1. Cute Yellow Cartoon Duck -->
<svg class="anim-duck" viewBox="0 0 100 100" fill="none">
    <!-- Shadow -->
    <ellipse cx="50" cy="90" rx="30" ry="6" fill="#0E051C" opacity="0.4"/>
    <!-- Yellow Body -->
    <ellipse cx="50" cy="58" rx="28" ry="24" fill="#FFD000"/>
    <ellipse cx="48" cy="62" rx="22" ry="16" fill="#FFDC33"/>
    <!-- Little Tail Feathers -->
    <path d="M22 56 Q12 50 16 62 Q22 66 26 62 Z" fill="#FFC400"/>
    <!-- Wing -->
    <ellipse cx="42" cy="60" rx="14" ry="10" transform="rotate(-10 42 60)" fill="#FFBA00"/>
    <!-- Round Head -->
    <circle cx="64" cy="40" r="19" fill="#FFD000"/>
    <circle cx="62" cy="38" r="15" fill="#FFDC33"/>
    <!-- Big Anime Eyes with Sparkles -->
    <ellipse cx="69" cy="36" rx="4.5" ry="6" fill="#1A0B33"/>
    <circle cx="71" cy="34" r="2" fill="#FFFFFF"/>
    <circle cx="68" cy="38" r="1" fill="#FFFFFF"/>
    <!-- Cheerful Orange Bill -->
    <path d="M76 40 Q88 42 84 48 Q76 50 72 44 Z" fill="#FF7A00"/>
    <ellipse cx="78" cy="44" rx="4" ry="1.5" fill="#FF9E00"/>
    <!-- Rosy Cheek -->
    <circle cx="60" cy="44" r="3.5" fill="#FF6B6B" opacity="0.6"/>
    <!-- Witch Hat -->
    <polygon points="62,6 48,26 80,26" fill="#6A1B9A"/>
    <ellipse cx="64" cy="26" rx="18" ry="4" fill="#8E24AA"/>
    <rect x="56" y="23" width="16" height="3" fill="#FF9E00"/>
</svg>

<!-- 2. Adorable Baby Dragon -->
<svg class="anim-dragon" viewBox="0 0 100 100" fill="none">
    <!-- Shadow -->
    <ellipse cx="50" cy="92" rx="26" ry="5" fill="#0E051C" opacity="0.4"/>
    <!-- Chubby Baby Dragon Body -->
    <ellipse cx="48" cy="62" rx="22" ry="22" fill="#9D4EDD"/>
    <!-- Belly -->
    <ellipse cx="54" cy="66" rx="14" ry="14" fill="#E0AAFF"/>
    <line x1="46" y1="62" x2="62" y2="62" stroke="#C77DFF" stroke-width="1.5"/>
    <line x1="47" y1="68" x2="61" y2="68" stroke="#C77DFF" stroke-width="1.5"/>
    <!-- Dragon Tail with Spade Tip -->
    <path d="M26 68 Q14 74 18 84 Q24 82 28 76 Z" fill="#7B2CBF"/>
    <polygon points="12,86 18,80 22,86" fill="#FF9E00"/>
    <!-- Dragon Head -->
    <circle cx="58" cy="38" r="18" fill="#9D4EDD"/>
    <!-- Horns -->
    <polygon points="46,16 48,26 42,26" fill="#FFD166"/>
    <polygon points="60,14 62,24 56,24" fill="#FFD166"/>
    <!-- Big Cute Dragon Eyes -->
    <ellipse cx="64" cy="35" rx="5" ry="6" fill="#16082B"/>
    <circle cx="66" cy="33" r="2.2" fill="#FFFFFF"/>
    <circle cx="63" cy="37" r="1" fill="#FFFFFF"/>
    <!-- Snout & Tiny Smile -->
    <ellipse cx="72" cy="42" rx="8" ry="6" fill="#9D4EDD"/>
    <circle cx="74" cy="40" r="1.2" fill="#5A189A"/>
    <circle cx="77" cy="41" r="1.2" fill="#5A189A"/>
    <path d="M68 44 Q72 47 75 44" stroke="#5A189A" stroke-width="1.5" stroke-linecap="round"/>
    <!-- Cute Wings -->
    <path d="M38 52 Q24 38 32 30 Q42 36 38 52 Z" fill="#C77DFF"/>
    <path d="M34 32 L38 50" stroke="#7B2CBF" stroke-width="1.5"/>
</svg>

<!-- 3. Playful Pond Fish (Koi) with Bubbles -->
<svg class="anim-fish" viewBox="0 0 100 80" fill="none">
    <!-- Bubble Trail -->
    <circle cx="82" cy="22" r="3.5" fill="#7CC8FF" opacity="0.6"/>
    <circle cx="88" cy="14" r="2" fill="#7CC8FF" opacity="0.7"/>
    <circle cx="94" cy="8" r="4" fill="#7CC8FF" opacity="0.5"/>
    <!-- Fish Body -->
    <ellipse cx="50" cy="44" rx="26" ry="16" fill="#FF7A00"/>
    <path d="M40 48 Q52 56 66 48 Q56 42 40 48 Z" fill="#FFF3E0"/>
    <!-- Tail Fin -->
    <path d="M26 44 Q10 32 12 44 Q10 56 26 44 Z" fill="#FF5100"/>
    <!-- Dorsal Fin -->
    <path d="M46 28 Q54 20 62 30 Z" fill="#FF9E00"/>
    <!-- Pectoral Fin -->
    <path d="M52 48 Q58 56 64 50 Z" fill="#FFA726"/>
    <!-- Eye -->
    <circle cx="66" cy="40" r="4" fill="#FFFFFF"/>
    <circle cx="67" cy="40" r="2.5" fill="#1A0B33"/>
    <circle cx="68" cy="39" r="1" fill="#FFFFFF"/>
</svg>

<!-- 4. Glowing Jack-o'-Lantern (from Reference 1) -->
<svg class="anim-pumpkin" viewBox="0 0 90 80" fill="none">
    <ellipse cx="45" cy="46" rx="36" ry="28" fill="#FF7A00"/>
    <ellipse cx="45" cy="46" rx="24" ry="28" fill="#FF9500"/>
    <rect x="42" y="10" width="6" height="12" rx="2" fill="#52B788"/>
    <!-- Carved Face Glow -->
    <polygon points="30,36 38,44 26,44" fill="#FFE082"/>
    <polygon points="60,36 64,44 52,44" fill="#FFE082"/>
    <polygon points="45,43 48,48 42,48" fill="#FFE082"/>
    <path d="M26 54 L32 52 L36 56 L42 52 L48 56 L54 52 L58 56 L64 53 C58 64, 32 64, 26 54 Z" fill="#FFE082"/>
</svg>
</div>"""
    return html_str.strip()
