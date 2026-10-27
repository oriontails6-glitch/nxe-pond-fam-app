# NXE Pond Fam: Spooky Halloween Avatar & Costume Competition

A mobile-first community web app for King Shot alliance **NXE** featuring a fantasy-lore trivia gate, anonymous costume gallery, community voting, and grand champion reveal.

---

## 🏰 Setup Guide

### 1. Supabase Setup
1. Create a project at [supabase.com](https://supabase.com).
2. Go to **SQL Editor**, paste the contents of `schema.sql`, and click **Run**.
3. Go to **Storage**, create a new bucket named `avatars`, and toggle **Public bucket** to **ON**.
4. Go to **Project Settings > API** (or Connect button) and note your **Project URL** and **`service_role` secret key**.

### 2. Configure Local Secrets
Inside `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_SERVICE_KEY = "your-service-role-key"

JOIN_CODE = "NXEHALLOWEEN2026"
SESSION_SECRET = "your-random-signing-secret"
TEST_MODE = true

[ADMIN_USERS]
admin1 = "YourPassword1!"
admin2 = "YourPassword2!"
admin3 = "YourPassword3!"
admin4 = "YourPassword4!"
```

### 3. Seed Trivia Questions
Run the seed script once to populate the 15 fantasy lore questions:
```powershell
python seed_questions.py
```

### 4. Run Locally & Mobile Phone Testing
Run the app:
```powershell
python -m streamlit run app.py
```
To test on your phone over the local WiFi network, open the **Network URL** displayed in the terminal (e.g., `http://192.168.x.x:8501`) on your mobile browser.

---

## 🚀 Deployment to Streamlit Community Cloud

### Pre-Push Secrets Checklist
Before pushing to GitHub, verify that no private secrets or database keys are tracked:
```powershell
git status
```
* Ensure `.streamlit/secrets.toml` is NOT listed (blocked by `.gitignore`).
* Ensure `questions.json` is NOT committed.

### Streamlit Cloud Deployment Steps
1. Push this directory to a **Private GitHub Repository**.
2. Visit [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Select your repository, branch (`main`), and main file path (`app.py`).
4. Click **Advanced settings...** and open the **Secrets** tab.
5. Paste the entire contents of your `.streamlit/secrets.toml`.
6. For official public launch, set `TEST_MODE = false`.
7. Click **Deploy!**

> **Note on Free Tier Sleep:** Streamlit Community Cloud apps enter a sleep state after a period of inactivity. Always open the competition URL 3–5 minutes before announcing it in alliance chat to wake up the container!

---

## 🛠️ Operations & Management

* **Access the Admin Panel:** Navigate directly to `https://your-app-url/?page=admin` and log in with any of your 4 admin credentials.
* **Add Roster IDs:** In the Admin Panel under **Roster Manager**, paste Governor IDs or upload a CSV. Duplicates and non-digit entries are automatically filtered.
* **Hide / Restore an Entry:** In the Admin Panel under **Submissions**, click Hide or Restore with a mandatory reason.
* **Adjust Phase Deadlines:** In the Admin Panel under **Phase Settings**, edit the UTC deadlines and click Save.
* **Replace the Sponsor Image:** Drop any image into `assets/sponsor.png`. The app will automatically optimize and display it with the golden crown frame.
