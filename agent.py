# agent.py

from core.ingest import load_emails
from core.event_parser import extract_events_from_emails
from core.event_store import load_event_store, update_event_store
from core.schedule_manager import schedule_events
from core.email_generator import generate_response_emails
from core.utils import save_json, save_scheduled_events
from config import (
    EMAIL_FILES,
    EVENT_STORE_PATH,
    OUTPUT_SCHEDULES_DIR,
    OUTPUT_EMAILS_DIR,
    get_schedule_output_path,
    get_email_output_path,
)

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

        # 2. Load previous event store and append new events
        existing_store = load_event_store(EVENT_STORE_PATH)
        updated_store = update_event_store(existing_store, new_events)

        # 3. Group + merge + schedule using LLM
        final_events = schedule_events(updated_store)

        # 4. Save scheduled events for this cycle
        schedule_path = get_schedule_output_path(cycle_name)
        save_scheduled_events(final_events, schedule_path)

        # 5. Generate and save email responses (only for changed events)
        email_responses = generate_response_emails(final_events)
        email_path = get_email_output_path(cycle_name)
        save_json(email_responses, email_path)

        # 6. Persist updated event store (same as final_events)
        save_json(final_events, EVENT_STORE_PATH)

    print("\n✅ All cycles processed.")

if __name__ == "__main__":
    main()