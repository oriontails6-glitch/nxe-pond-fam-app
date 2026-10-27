"""
Seed script to load questions.json into Supabase questions table.
Run locally once:
    python seed_questions.py
"""
import os
import json
import toml
from supabase import create_client


def get_secrets():
    secrets_path = os.path.join(".streamlit", "secrets.toml")
    if not os.path.exists(secrets_path):
        raise FileNotFoundError(
            f"Secrets file not found at {secrets_path}. Please create it before running seed_questions.py."
        )
    with open(secrets_path, "r", encoding="utf-8") as f:
        return toml.load(f)


def seed():
    secrets = get_secrets()
    url = secrets.get("SUPABASE_URL")
    key = secrets.get("SUPABASE_SERVICE_KEY")

    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY must be defined in .streamlit/secrets.toml")
        return

    client = create_client(url, key)

    if not os.path.exists("questions.json"):
        print("ERROR: questions.json not found.")
        return

    with open("questions.json", "r", encoding="utf-8") as f:
        questions_data = json.load(f)

    print(f"Loaded {len(questions_data)} questions from questions.json.")

    # Clear existing active questions to prevent duplication
    client.table("questions").delete().neq("id", 0).execute()

    for idx, q in enumerate(questions_data, start=1):
        payload = {
            "text": q["text"],
            "options": q["options"],
            "correct_index": q["correct_index"],
            "active": True
        }
        res = client.table("questions").insert(payload).execute()
        print(f"  [{idx}/{len(questions_data)}] Inserted question: {q['text'][:50]}...")

    print("SUCCESS: Questions seeded into Supabase!")


if __name__ == "__main__":
    seed()
