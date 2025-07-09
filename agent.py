# agent.py

from core.ingest import load_emails
from core.event_parser import extract_events_from_emails
from core.event_store import load_event_store, update_event_store
from core.schedule_manager import schedule_events
from core.email_generator import generate_response_emails
from core.utils import save_json, get_cycle_number_from_filename
from config import EMAIL_FILES, EVENT_STORE_PATH, OUTPUT_SCHEDULES_DIR, OUTPUT_EMAILS_DIR, get_schedule_output_path, get_email_output_path

import os

# Ensure output dirs exist
os.makedirs(OUTPUT_SCHEDULES_DIR, exist_ok=True)
os.makedirs(OUTPUT_EMAILS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(EVENT_STORE_PATH), exist_ok=True)

def main():
    print("🧠 Running scheduling agent...")

    for cycle_name, filepath in EMAIL_FILES.items():
        print(f"\n📩 Ingesting: {filepath}")
        raw_emails = load_emails(filepath)

        # 1. Extract structured event objects from the emails
        new_events = extract_events_from_emails(raw_emails)
        # print(new_events)

        # 2. Load event store and update it with new/changed events
        event_store = load_event_store(EVENT_STORE_PATH)
        updated_store = update_event_store(event_store, new_events)

        # 3. Run scheduling logic (LLM or rule-based) on updated events
        final_store = schedule_events(updated_store)

        # 4. Save full schedule for this cycle
        schedule_path = get_schedule_output_path(cycle_name)
        save_json(final_store, schedule_path)

        # 5. Generate response emails for any schedule changes
        email_responses = generate_response_emails(final_store)
        email_path = get_email_output_path(cycle_name)
        save_json(email_responses, email_path)

        # 6. Persist updated event store
        save_json(final_store, EVENT_STORE_PATH)

    print("\n✅ All cycles processed.")

if __name__ == "__main__":
    main()
