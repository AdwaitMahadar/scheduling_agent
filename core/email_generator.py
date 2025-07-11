# core/email_generator.py

from core.utils import call_llm_for_response_email

def generate_response_emails(final_events):
    responses = []

    for event in final_events:
        if not event.get("schedule_change"):
            continue

        # LLM generates subject + body
        reply = call_llm_for_response_email(event)

        if reply:
            email_obj = {
                "to": event["sender"],
                "subject": reply.get("subject", "Regarding your event"),
                "body": reply.get("body", "Thanks for the update."),
                "status": event["scheduling_status"]
            }
            responses.append(email_obj)

    return responses
