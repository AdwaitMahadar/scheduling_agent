# core/schedule_manager.py

from collections import defaultdict
from core.utils import (
    call_llm_for_event_match,
    call_llm_merge_event_group,
    call_llm_schedule_events,
    save_json,
)

def schedule_events(event_store):
    """
    Step 1: Group events by (sender-recipient pair, thread_id)
    Step 2: Merge each group via LLM
    Step 3: Assign scheduling status
    """
    # === Step 1: Group events ===
    groups = defaultdict(list)
    for event in event_store:
        key = (frozenset([event["sender"], event["recipient"]]), event["thread_id"])
        groups[key].append(event)

    grouped_events = list(groups.values())
    # save_json(grouped_events, "output/groups.json")

    # === Step 2: Merge each group ===
    merged_events = []
    for group in grouped_events:
        merged = call_llm_merge_event_group(group)
        merged_events.append(merged)
    
    # save_json(merged_events, "output/merged_events.json")

    # === Step 3: Schedule final merged events ===
    scheduled_events = call_llm_schedule_events(merged_events)

    return scheduled_events
