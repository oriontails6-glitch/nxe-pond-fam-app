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
        "rank": "🥇 1st Place Champion (THE TOURNAMENT HIGHLIGHT)",
        "title": "💎 1 Month Card (Grand High Benefactor Trophy)",
        "desc": "The supreme crown jewel of the Halloween Championship! Funded directly from Papa Mo's royal platinum vault of infinite riches. A full month of royal King Shot glory and endless power for the crowned spooky monarch of the pond!",
        "badge": "👑 Grand Benefactor Crown",
        "color": "#FBBF24"
    },
    {
        "rank": "🥈 2nd Place Victor (Mischief Edition)",
        "title": "🫡 Everyone Obeys You for 24 Hours... With A Catch!",
        "desc": "Absolute alliance obedience! For 24 full hours, every duck, fish, and governor in NXE must follow your every quack, decree, or ridiculous command! HOWEVER: 1) Sponsor Papa Mo is 100% EXEMPT (nobody bosses the checkbook!). 2) The mischievous Ghost Twinns (Orion & Nobu) officially reserve the ghostly right to flat-out REFUSE any command they deem boring, unspooky, or lacking snacks!",
        "badge": "👻 Obedience with Ghostly Rebellion",
        "color": "#E2E8F0"
    },
    {
        "rank": "🥉 3rd Place Hero (Feast of Honor)",
        "title": "🍲 150M RSS Dinner at Orion's Pax (PLEASE BE GENTLE!)",
        "desc": "A staggering 150,000,000 resource banquet served fresh at Orion's Pax! Orion's personal royal plea: 'Pax is my absolute favorite child in all the kingdoms! Feast with pride, but please wipe your webbed duck feet and BE GENTLE with Pax's furniture!'",
        "badge": "🌾 150M RSS Feast (Wipe Your Feet!)",
        "color": "#FB923C"
    }
]

# Fun lore quotes from Papa Mo and the Ghost Twinns
PAPA_MO_QUOTES = [
    "Papa Mo on Funding the 1-Month Card: 'I checked my gold pouch and accidentally dropped a Month Card. Whoever wins it better flex in alliance chat 24/7!' 💳👑",
    "Papa Mo's Alliance Decree: 'Every duck shall wear a witch hat, and all candy corn must be shared... except mine. Mine is in a vault.' 🦆🎃💎",
    "Papa Mo's Royal Clarification: 'Whoever wins 2nd place commands the entire alliance, but if anyone orders me to do pond pushups, I will revoke everyone's lily pad heating privileges!' 🫡❄️",
    "Official Guarantee from Papa Mo: 100% Certified Spooky, 0% Organic Swamp Slime, and 200% funded by my sheer golden wealth! 💰🐸",
    "Papa Mo: 'The Ghost Twinns asked for a budget increase for fake spiderwebs. I bought real spiders. You are welcome, NXE.' 🕷️🤣",
    "Papa Mo's Economic Warning: 'The 150M RSS banquet at Orion's Pax is fully insured, but if anyone spills pumpkin soup on Orion's silk carpets, the bill goes to your farm account!' 🍲🧾",
    "Papa Mo: 'I paid the mist-goblins triple overtime in pumpkin scones to ensure zero mobile lag. If your phone buffers, blame Nobu!' 📱💨",
    "Papa Mo's Supreme Order: 'Win the 1-Month Card or spend the rest of autumn paddling against the pond current!' 🦆💨"
]

TWINNS_QUOTES = [
    "Orion: 'Nobu, did you save the candy corn like Papa Mo asked?' Nobu: 'What candy corn? *burrrrp*' Orion: 'Nobu you ate 40 pounds of sugar in 6 seconds.' 🦆🎃🍭",
    "Orion: 'Regarding the 3rd place 150M RSS banquet: BE GENTLE! Pax is my absolute favorite, my pride, my joy! Eat the corn, but don't kick the furniture!' 🍲🥺",
    "Nobu: 'If the 2nd place victor orders us to stop haunting the pond reeds, we officially invoke Article 4 of the Ghost Twinns Charter: NOPE!' 👻📜",
    "The Ghost Twinns: 'We may be ghosts among the triplets, but our mischief has a 100% success rate and Papa Mo pays the repair bills!' ✨👻👑",
    "Nobu: 'Orion, is 150M RSS enough for a dinner party?' Orion: 'Nobu, 150M can feed three kingdoms and six dragons!' Nobu: 'Cool, I will take a pre-dinner snack then.' 🐉🥐",
    "Orion: 'Nobu, why is there ectoplasm on the 1-Month Card trophy?' Nobu: 'It was a ghost kiss of good luck! It wipes off... mostly.' 💎👻",
    "Nobu's Decree: 'Any order given to us during the 24-hour 2nd place rule must be submitted in triplicate, signed in pumpkin juice, and accompanied by glazed donuts.' 🍩🎃",
    "The Twinns: 'May the spookiest avatar win the Month Card! And remember: Pax has feelings, treat the RSS dinner with tender love and care!' 🏰🍲"
]
