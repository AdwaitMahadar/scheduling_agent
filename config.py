import os
from dotenv import load_dotenv

# Load keys from .env file
load_dotenv()

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JUDGMENT_API_KEY = os.getenv("JUDGMENT_API_KEY")
JUDGMENT_ORG_ID = os.getenv("JUDGMENT_ORG_ID")

# === Root Directory ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === Paths ===
EMAIL_DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_EMAILS_DIR = os.path.join(BASE_DIR, "output", "emails")
OUTPUT_SCHEDULES_DIR = os.path.join(BASE_DIR, "output", "schedules")
EVENT_STORE_PATH = os.path.join(BASE_DIR, "store", "event_store.json")

# === Email Cycles ===
EMAIL_FILES = {
    "cycle_1": os.path.join(EMAIL_DATA_DIR, "emails_cycle_1.json"),
    "cycle_2": os.path.join(EMAIL_DATA_DIR, "emails_cycle_2.json"),
    "cycle_3": os.path.join(EMAIL_DATA_DIR, "emails_cycle_3.json"),
}

# === Output Helpers ===
def get_schedule_output_path(cycle):
    return os.path.join(OUTPUT_SCHEDULES_DIR, f"schedule_{cycle}.json")

def get_email_output_path(cycle):
    return os.path.join(OUTPUT_EMAILS_DIR, f"emails_{cycle}.json")
