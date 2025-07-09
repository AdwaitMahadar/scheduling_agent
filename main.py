# main.py

from core.ingest import load_emails
from core.event_parser import extract_events_from_emails
from core.event_store import load_event_store, update_event_store, save_event_store
from core.schedule_manager import schedule_events
from core.utils import save_schedule, save_responses
import os

# -------- CONFIG --------
CYCLE_FILE = "data/emails_cycle_3.json"

# -------- STEP 1: Load Email Threads --------
threads = load_emails(CYCLE_FILE)

# -------- STEP 2: Extract Events from Emails --------
new_events = extract_events_from_emails(threads)

# -------- STEP 3: Load + Update Event Store --------
event_store = load_event_store()
updated_event_store = update_event_store(event_store, new_events)
save_event_store(updated_event_store)

# -------- STEP 4: Schedule Events --------
scheduled_events = schedule_events(updated_event_store)

# -------- STEP 5: Save Schedule + Response Emails --------
schedule_path = save_schedule(scheduled_events)
emails_path = save_responses(scheduled_events)

print(f"\n✅ Ingestion cycle complete!")
print(f"📅 Schedule saved to: {schedule_path}")
print(f"📨 Response emails saved to: {emails_path}")
