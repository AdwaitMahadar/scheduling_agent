# core/utils.py

import os
import json
from datetime import datetime
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_sender(msg):
    return msg["sender"]

def extract_thread_id(thread):
    return thread["thread_id"]

def get_cycle_number_from_filename(filename):
    # Assumes filename like: emails_cycle_1.json
    return filename.split("_")[-1].split(".")[0]

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def call_llm_for_event_attrs(sender, recipient, body):
    prompt = f"""
You are an assistant that extracts structured event details from an email message.

Here is the email:
From: {sender}
To: {recipient}
Body: {body}

Extract the following:
- A concise summary (1 line, like "Lunch with Sam at 1pm at Thai Place")
- Title (e.g., "Lunch", "Dentist Appointment")
- Priority (High, Medium, or Low)
- Time (24hr format like 13:00 if available)
- Venue (if mentioned)

Respond in JSON:
{{
  "summary": "...",
  "title": "...",
  "priority": "...",
  "time": "...",
  "venue": "..."
}}
If any value is not available, set it to null.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"LLM error: {e}")
        return {
            "summary": body[:100],
            "title": "Unknown Event",
            "priority": "Low",
            "time": None,
            "venue": None
        }

def call_llm_for_event_match(event_a, event_b):
    """
    (Optional) Use LLM to determine if two events are same. 
    For now, fall back to thread_id + sender logic.
    """
    return (event_a["sender"] == event_b["sender"]) and (event_a["thread_id"] == event_b["thread_id"])


def save_schedule(events, output_dir="output/schedules"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(output_dir, f"schedule_{timestamp}.json")
    with open(path, "w") as f:
        json.dump(events, f, indent=2)
    return path

def save_responses(events, output_dir="output/emails"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(output_dir, f"emails_{timestamp}.json")
    responses = []
    for event in events:
        if event.get("schedule_change"):
            email = generate_email_response(event)
            responses.append(email)
    with open(path, "w") as f:
        json.dump(responses, f, indent=2)
    return path

def generate_email_response(event):
    status = event["scheduling_status"]
    time = event.get("time", "TBD")
    title = event.get("title", "your event")

    if status == "Scheduled":
        body = f"Hi, just confirming {title} is scheduled today at {time}."
    elif status == "Cancelled":
        body = f"Hi, unfortunately we couldn't fit {title} into today's schedule. Let's reschedule another day."
    elif status == "Hold":
        body = f"Hi, we're holding {title} for now — will confirm if a slot opens up."

    return {
        "recipient": event["sender"],
        "sender": "you@example.com",
        "thread_id": event["thread_id"],
        "event_id": event["event_id"],
        "body": body
    }
