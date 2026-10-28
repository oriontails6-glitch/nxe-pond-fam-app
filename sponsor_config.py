"""
Sponsor & Organizers Configuration for NXE Pond Fam Halloween App.
- Official Wealthy Sponsor: Papa Mo
- Mischievous Ghost Organizers: "THE TWINNS among the triplets" (Orion & Nobu)
- Official Prizes sponsored by Papa Mo
"""

import os
import base64

def get_image_base64_data_uri(file_path: str) -> str | None:
    """Reads an image file and converts it into a base64 Data URI for inline HTML rendering."""
    if not file_path or not os.path.exists(file_path):
        return None
    try:
        ext = os.path.splitext(file_path)[1].lower().lstrip(".")
        if ext == "jpg":
            ext = "jpeg"
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/{ext};base64,{encoded}"
    except Exception:
        return None

# Sponsor Details
SPONSOR_NAME = "Papa Mo"
SPONSOR_TITLE = "The Legendary & Wealthy Papa Mo"
SPONSOR_SUBTITLE = "Grand High Patron & Supreme Benefactor of the Lily Pads"
SPONSOR_BADGE = "👑 Official Tournament Benefactor"
SPONSOR_IMAGE = "images/sponsor_web.webp"
SPONSOR_IMAGE_FALLBACK = "images/sponsor.png"

# Organizers Details
ORGANIZERS_NAME = "THE TWINNS (Orion & Nobu)"
ORGANIZERS_TITLE = "The Mischievous Twinns Among the Triplets"
ORGANIZERS_SUBTITLE = "Now Floating as Pond Ghosts 👻 • Masterminds of the Halloween Arena"
ORGANIZERS_BADGE = "👻 Ghostly Tournament Organizers"
ORGANIZERS_IMAGE = "images/organizers_web.webp"
ORGANIZERS_IMAGE_FALLBACK = "images/organizers.png"

# Official Tournament Prizes Sponsored by Papa Mo
TOURNAMENT_PRIZES = [
    {
        "rank": "🥇 1st Place Champion",
        "title": "1 Month Card",
        "desc": "Funded directly from Papa Mo's royal vault of riches! The ultimate trophy for the crowned king/queen of Halloween.",
        "badge": "👑 Champion's Crown",
        "color": "#FBBF24"
    },
    {
        "rank": "🥈 2nd Place Victor",
        "title": "Everyone Obeys You for 24 Hours (EXCEPT Papa Mo!)",
        "desc": "Absolute alliance obedience! For 24 full hours, every alliance member in NXE must follow your every command, quack, or decree — EXCEPT the sponsor Papa Mo, who is strictly exempt & commands from his golden lily pad!",
        "badge": "🫡 Total Alliance Command (Papa Mo Exempt)",
        "color": "#E2E8F0"
    },
    {
        "rank": "🥉 3rd Place Hero",
        "title": "150M RSS Dinner at Orion's Pax",
        "desc": "A legendary banquet of 150,000,000 resources served fresh at Orion's stronghold! Dig in and feast like pond royalty.",
        "badge": "🍲 150M RSS Feast",
        "color": "#FB923C"
    }
]

# Fun lore quotes from Papa Mo and the Ghost Twinns
PAPA_MO_QUOTES = [
    "Papa Mo's Alliance Decree: 'Every duck shall wear a witch hat, and all candy corn must be shared!' 🦆🎃",
    "Papa Mo personally funded the 1-Month Card: 'Only the finest loot for our NXE pond champions!' 💎",
    "Official Guarantee from Papa Mo: 100% Certified Spooky, 0% Organic Swamp Slime!",
    "Funded entirely by Papa Mo's secret vault of pumpkin-spice dragon treats! 🐉🥐",
    "Papa Mo's Royal Clarification: 'Whoever wins 2nd place commands the entire alliance, but nobody orders Papa Mo around!' 👑🫡",
    "Rumor has it Papa Mo unionized the pond frogs to protect the 150M RSS dinner delivery! 🐸🍲",
    "Alliance Rule #1 according to Papa Mo: The Ghost Twinns are allowed to cause chaos, as long as everyone has fun! 👻",
    "Papa Mo paid the mist-goblins triple overtime to ensure buttery-smooth mobile loading! 📱💨"
]

TWINNS_QUOTES = [
    "Orion & Nobu: 'We may be ghosts now, but our mischief is alive and thriving under Papa Mo's golden patronage!' 👻✨",
    "The Twinns Decree: '150M RSS is waiting at Orion's Pax. Come hungry, leave wealthy!' 🍲🌾",
    "Orion: 'Nobu, did you hide the extra candy corn?' Nobu: 'What candy corn? *burp*' 🦆🎃",
    "The Mischievous Twinns: 'May the spookiest avatar win, and remember: runner-up bosses everyone around, except Papa Mo!' 🫡",
    "The Twinns: 'We haunt the pond with love, chaos, and Papa Mo's endless supply of shiny prizes!' 👑"
]
