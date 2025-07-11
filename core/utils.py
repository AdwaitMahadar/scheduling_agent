# core/utils.py

import os
import json
from datetime import datetime
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

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
    Use LLM to decide if event_a and event_b are updates of the same real-world event.
    """
    prompt = f"""
You are a scheduling assistant helping group events.

Here are two event objects:

Event A:
{json.dumps(event_a, indent=2)}

Event B:
{json.dumps(event_b, indent=2)}

Do these refer to the same real-world event (like the same lunch, appointment, or task)?
Answer only with true or false.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        answer = response.choices[0].message.content.strip().lower()
        return "true" in answer
    except Exception as e:
        print(f"LLM match error: {e}")
        return False

def call_llm_merge_event_group(group):
    """
    Merge a group of events (updates to same task) into one canonical event.
    """
    prompt = f"""
You are an assistant helping merge event updates into one final event.

Below is a list of related events. Please combine them into a single final event that preserves useful information, gives the latest updates, and infers missing values when needed.

Rules:
- Preserve the event_id from the earliest message.
- Use latest 'last_updated' timestamp.
- Merge fields: title, priority, time, venue, recipient, and body (generate a good summary of the situation).
- Use common sense while merging: look at all the events, understand their chornology and context and then update the fields accordingly.

Events:
{json.dumps(group, indent=2)}

Respond in JSON with the merged event:
{{
  "event_id": "...",
  "thread_id": "...",
  "sender": "...",
  "recipient": "...",
  "title": "...",
  "priority": "...",
  "time": "...",
  "venue": "...",
  "body": "...",
  "scheduling_status": null,
  "schedule_change": false,
  "last_updated": "..."
}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"LLM merge error: {e}")
        return group[-1]  # fallback to latest

def call_llm_schedule_events(events):
    """
    Ask LLM to assign scheduling_status and schedule_change for each final merged event.
    """
    prompt = f"""
You are a calendar assistant deciding how to schedule events based on user preferences.

Each event has title, priority, time, venue, body (summary), and past status.

Instructions:
- Set scheduling_status to one of: "Scheduled", "Hold", or "Cancelled".
- Set schedule_change to true if the status or time is different from before.
- Use time and priority to resolve conflicts — high-priority items can preempt others.
- Cancel an event if the body says things like "canceled", "not happening", "skip", etc.

Here is the list of events:
{json.dumps(events, indent=2)}

Respond with the full updated list of events (same structure), but with scheduling_status and schedule_change fields filled in.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"LLM scheduling error: {e}")
        return events  # fallback

def call_llm_for_response_email(event):
    """
    Uses LLM to generate a natural language response email for an event.
    """
    prompt = f"""
You are an assistant helping a user write polite and informative email replies about schedule changes.

Here is the event:
- Title: {event['title']}
- Sender: {event['sender']}
- Status: {event['scheduling_status']}
- Time: {event.get('time')}
- Venue: {event.get('venue')}
- Body: {event.get('body')}

Write a friendly and short email response confirming or acknowledging the change. Include:
1. A subject line (like "Confirming Lunch at 1pm")
2. A brief message body (like "Hey Sam, lunch at 1pm sounds great. See you at Thai Place!")

Respond in JSON:
{{
  "subject": "...",
  "body": "..."
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print(f"LLM email generation error: {e}")
        return None

def save_scheduled_events(events, path):
    """
    Save only the events that are scheduled, with limited fields.
    """
    filtered = []
    for event in events:
        if event.get("scheduling_status") == "Scheduled":
            filtered.append({
                "sender": event.get("sender"),
                "recipient": event.get("recipient"),
                "title": event.get("title"),
                "priority": event.get("priority"),
                "time": event.get("time"),
                "venue": event.get("venue"),
                "body": event.get("body"),
            })

    with open(path, "w") as f:
        json.dump(filtered, f, indent=2)