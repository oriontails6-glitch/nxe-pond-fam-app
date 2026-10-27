"""
Seeds test contestants and votes into Supabase for testing Gallery and Podium in TEST_MODE.
"""
import io
import uuid
import toml
from PIL import Image, ImageDraw
from supabase import create_client


def create_avatar(bg_color, emoji_text):
    img = Image.new("RGB", (400, 400), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Draw simple festive shapes
    draw.ellipse([50, 50, 350, 350], fill=(255, 255, 255))
    draw.ellipse([70, 70, 330, 330], fill=bg_color)
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=80)
    return buf.getvalue()


def seed_test_data():
    with open("C:/Users/Zaara/Desktop/nxe-pond-fam-app/.streamlit/secrets.toml", "r") as f:
        sec = toml.load(f)

    client = create_client(sec["SUPABASE_URL"], sec["SUPABASE_SERVICE_KEY"])

    # 1. Add Test Roster IDs
    test_govs = ["100001", "100002", "100003", "200001", "200002", "200003", "200004", "200005"]
    for gid in test_govs:
        client.table("roster").upsert({"governor_id": gid}).execute()

    print("Added test roster IDs.")

    # 2. Upload test avatars & create entries
    test_entries = [
        {
            "governor_id": "100001",
            "ingame_name": "Count Quackula",
            "backstory": "A dashing nocturnal duckling wearing an oversized velvet cape. Only drinks tomato juice and flies across the lily pads during full moons.",
            "quiz_score": 5,
            "qualified": True,
            "color": (123, 44, 191)
        },
        {
            "governor_id": "100002",
            "ingame_name": "Pumpkin Knight",
            "backstory": "Forged in the enchanted pumpkin patch! Armed with a toothpick lance and an impenetrable turnip helmet. Pledged to protect all ducklings from cold water.",
            "quiz_score": 4,
            "qualified": True,
            "color": (255, 117, 24)
        },
        {
            "governor_id": "100003",
            "ingame_name": "Goblin Snackmaster",
            "backstory": "Failed the book lore exam because he was too busy eating Don Pengucci's secret taco recipe in the swamp bushes. Outstanding costume, zero reading comprehension.",
            "quiz_score": 1,
            "qualified": False,
            "color": (57, 255, 20)
        }
    ]

    created_eids = {}
    for te in test_entries:
        existing = client.table("entries").select("id").eq("governor_id", te["governor_id"]).execute()
        if existing.data:
            created_eids[te["ingame_name"]] = existing.data[0]["id"]
            continue

        raw_bytes = create_avatar(te["color"], te["ingame_name"])
        u_name = f"test_{te['governor_id']}.webp"
        client.storage.from_("avatars").upload(u_name, raw_bytes, file_options={"content-type": "image/webp", "upsert": "true"})
        img_url = client.storage.from_("avatars").get_public_url(u_name)

        ins = client.table("entries").insert({
            "governor_id": te["governor_id"],
            "ingame_name": te["ingame_name"],
            "backstory": te["backstory"],
            "image_path": img_url,
            "thumb_path": img_url,
            "quiz_score": te["quiz_score"],
            "qualified": te["qualified"],
            "hidden": False
        }).execute()

        created_eids[te["ingame_name"]] = ins.data[0]["id"]
        print(f"Created entry for {te['ingame_name']}")

    # Find Orion's entry ID
    orion_res = client.table("entries").select("id").eq("governor_id", "296378532").execute()
    if orion_res.data:
        orion_id = orion_res.data[0]["id"]
        # Add votes:
        # Give Orion 5 votes (Champion!)
        # Give Count Quackula 3 votes (#2)
        # Give Pumpkin Knight 2 votes (#3)
        voters = ["200001", "200002", "200003", "200004", "200005"]
        for v in voters:
            client.table("votes").upsert({"voter_id": v, "entry_id": orion_id}, on_conflict="voter_id,entry_id").execute()

        if "Count Quackula" in created_eids:
            for v in voters[:3]:
                client.table("votes").upsert({"voter_id": v, "entry_id": created_eids["Count Quackula"]}, on_conflict="voter_id,entry_id").execute()

        if "Pumpkin Knight" in created_eids:
            for v in voters[:2]:
                client.table("votes").upsert({"voter_id": v, "entry_id": created_eids["Pumpkin Knight"]}, on_conflict="voter_id,entry_id").execute()

        print("Seeded test community votes successfully!")


if __name__ == "__main__":
    seed_test_data()
