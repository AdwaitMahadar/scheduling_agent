# core/event_parser.py

from core.utils import call_llm_for_event_attrs
from judgeval_integration.tracer import judgment

@judgment.observe(span_type="function")
def extract_events_from_emails(email_threads):
    events = []

    for thread in email_threads:
        thread_id = thread["thread_id"]
        messages = thread["messages"]
        latest_msg = messages[-1]

        sender = latest_msg["sender"]
        recipient = latest_msg["recipient"]
        body = latest_msg["body"]
        timestamp = latest_msg["timestamp"]

        llm_data = call_llm_for_event_attrs(sender, recipient, body)

        event = {
            "event_id": None,
            "thread_id": thread_id,
            "sender": sender,
            "recipient": recipient,
            "title": llm_data.get("title") or "Unknown Event",
            "priority": llm_data.get("priority") or "Low",
            "time": llm_data.get("time"),
            "venue": llm_data.get("venue"),
            "body": llm_data.get("summary") or body,
            "scheduling_status": None,
            "schedule_change": True,
            "last_updated": timestamp
        }

        events.append(event)

    return events
