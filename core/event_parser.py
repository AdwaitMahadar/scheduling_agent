import uuid
from datetime import datetime
from core.utils import extract_sender, extract_thread_id, call_llm_for_event_attrs

def extract_events_from_emails(email_threads):
    events = []

    for thread in email_threads:
        thread_id = thread["thread_id"]
        messages = thread["messages"]

        latest_msg = messages[-1]  # Assume latest message is most relevant
        sender = extract_sender(latest_msg)
        body = latest_msg["body"]
        timestamp = latest_msg["timestamp"]

        # Use LLM to extract title, priority, time, venue
        llm_result = call_llm_for_event_attrs(body)

        # If LLM fails to return title or priority, skip this event
        if not llm_result.get("title") or not llm_result.get("priority"):
            continue

        event = {
            "event_id": None,  # Will be filled during store update
            "thread_id": thread_id,
            "sender": sender,
            "title": llm_result["title"],
            "priority": llm_result["priority"],
            "time": llm_result.get("time"),      # Optional
            "venue": llm_result.get("venue"),    # Optional
            "body": body,
            "scheduling_status": None,           # Will be set in scheduling phase
            "schedule_change": False,
            "last_updated": timestamp
        }

        events.append(event)

    return events
