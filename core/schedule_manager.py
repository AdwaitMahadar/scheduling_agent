# core/schedule_manager.py

from datetime import time, timedelta, datetime

# Priority weights for ordering
PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3}

# Define available time slots (assume 9 AM to 6 PM in 1-hr blocks)
def generate_day_slots():
    return [f"{h:02d}:00" for h in range(9, 18)]

def is_time_conflict(assigned_time, scheduled):
    return any(e["time"] == assigned_time and e["scheduling_status"] == "Scheduled" for e in scheduled)

def schedule_events(event_store):
    # Copy to avoid mutation
    updated_events = []
    scheduled_today = []

    used_slots = set(
        e["time"] for e in event_store if e["scheduling_status"] == "Scheduled" and e["time"]
    )

    all_slots = generate_day_slots()

    # Sort by priority and thread timestamp
    sorted_events = sorted(
        event_store,
        key=lambda e: (PRIORITY_ORDER.get(e["priority"], 4), e["last_updated"])
    )

    for event in sorted_events:
        prev_status = event["scheduling_status"]
        prev_time = event.get("time")

        if prev_status == "Cancelled":
            updated_events.append(event)
            continue

        assigned_time = prev_time

        if not prev_time or is_time_conflict(prev_time, scheduled_today):
            # Find a new available slot
            for slot in all_slots:
                if slot not in used_slots:
                    assigned_time = slot
                    break

        if assigned_time:
            event["time"] = assigned_time
            event["scheduling_status"] = "Scheduled"
            used_slots.add(assigned_time)
        else:
            # Could not schedule due to conflict
            if event["priority"] == "High":
                event["scheduling_status"] = "Scheduled"  # Force it even if overlaps (future: handle smarter)
            else:
                event["scheduling_status"] = "Cancelled"

        # Update change status
        event["schedule_change"] = (
            prev_status != event["scheduling_status"]
            or prev_time != event["time"]
        )

        updated_events.append(event)
        scheduled_today.append(event)

    return updated_events
