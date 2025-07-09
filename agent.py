import os
from dotenv import load_dotenv
from core.ingest import load_emails_from_file
from core.event_parser import extract_events_from_emails
from core.event_store import load_event_store, update_event_store
from core.schedule_manager import schedule_events
from core.email_generator import generate_response_emails
from core.utils import save_json, get_cycle_number_from_filename

# Load API keys and config
load_dotenv()

DATA_DIR = "data/ingested_emails"
SCHEDULE_DIR = "output/schedules"
EMAIL_OUTBOX_DIR = "output/emails"
STORE_PATH = "store/event_store.json"

# Ensure output directories exist
os.makedirs(SCHEDULE_DIR, exist_ok=True)
os.makedirs(EMAIL_OUTBOX_DIR, exist_ok=True)
os.makedirs("store", exist_ok=True)

def main():
    print(" Running scheduling agent...")

    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(DATA_DIR, filename)
        print(f"\n Ingesting file: {filename}")
        raw_emails = load_emails_from_file(filepath)

        # 1. Parse events from emails
        new_events = extract_events_from_emails(raw_emails)

        # 2. Load + update event store
        event_store = load_event_store(STORE_PATH)
        updated_store = update_event_store(event_store, new_events)

        # 3. Schedule
        final_store = schedule_events(updated_store)

        # 4. Save schedule
        cycle = get_cycle_number_from_filename(filename)
        save_json(final_store, f"{SCHEDULE_DIR}/schedule_cycle_{cycle}.json")

        # 5. Generate and save emails
        emails = generate_response_emails(final_store)
        save_json(emails, f"{EMAIL_OUTBOX_DIR}/emails_cycle_{cycle}.json")

        # 6. Save updated store
        save_json(final_store, STORE_PATH)

    print("\n All cycles processed.")

if __name__ == "__main__":
    main()
