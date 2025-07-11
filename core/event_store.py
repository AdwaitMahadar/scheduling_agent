# core/event_store.py

import os
import uuid
import json
from copy import deepcopy
from config import EVENT_STORE_PATH

def load_event_store(path=EVENT_STORE_PATH):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def update_event_store(existing_events, new_events):
    """
    Appends new events directly to the store with new UUIDs.
    """
    updated_store = deepcopy(existing_events)

    for event in new_events:
        event["event_id"] = str(uuid.uuid4())
        event["schedule_change"] = True  # Mark everything as new
        updated_store.append(event)

    return updated_store

def save_event_store(events, path=EVENT_STORE_PATH):
    with open(path, "w") as f:
        json.dump(events, f, indent=2)
