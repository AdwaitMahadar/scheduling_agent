# core/event_store.py

import os
import uuid
from copy import deepcopy
from core.utils import call_llm_for_event_match
from config import EVENT_STORE_PATH

def load_event_store(path=EVENT_STORE_PATH):
    if os.path.exists(path):
        import json
        with open(path, "r") as f:
            return json.load(f)
    return []

def update_event_store(existing_events, new_events):
    updated_store = deepcopy(existing_events)
    existing_by_thread = {(e["sender"], e["thread_id"]): e for e in existing_events}

    for new_event in new_events:
        key = (new_event["sender"], new_event["thread_id"])

        if key in existing_by_thread:
            existing_event = existing_by_thread[key]
            merged_event, changed = merge_event(existing_event, new_event)
            merged_event["schedule_change"] = changed
            merged_event["event_id"] = existing_event["event_id"]
            updated_store = [
                e if e["event_id"] != merged_event["event_id"] else merged_event
                for e in updated_store
            ]
        else:
            new_event["event_id"] = str(uuid.uuid4())
            new_event["schedule_change"] = True
            updated_store.append(new_event)

    return updated_store

def merge_event(existing, new):
    """
    Compares and merges fields. If anything changed, returns changed=True
    """
    changed = False
    merged = deepcopy(existing)

    for field in ["title", "priority", "time", "venue", "body"]:
        if new.get(field) and new.get(field) != existing.get(field):
            merged[field] = new[field]
            changed = True

    merged["last_updated"] = new["last_updated"]
    return merged, changed

def save_event_store(events, path=EVENT_STORE_PATH):
    import json
    with open(path, "w") as f:
        json.dump(events, f, indent=2)
