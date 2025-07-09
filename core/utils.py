import json
from datetime import datetime

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

def call_llm_for_event_attrs(text):
    """
    Stub: Replace this with real OpenAI call later.
    For now, use simple if-else based dummy return to simulate.
    """
    if "dentist" in text.lower():
        return {"title": "Dentist Appointment", "priority": "High", "time": "10:00", "venue": "Bright Smiles Clinic"}
    elif "lunch" in text.lower():
        return {"title": "Lunch", "priority": "Medium", "time": "13:00"}
    elif "electronics sale" in text.lower():
        return {"title": "Visit Electronics Sale", "priority": "Low", "time": "11:00", "venue": "BestBuy"}
    elif "bank" in text.lower():
        return {"title": "Visit Bank", "priority": "Medium", "time": "16:00"}
    elif "team call" in text.lower():
        return {"title": "Team Call", "priority": "High", "time": "14:00"}
    elif "coffee" in text.lower():
        return {"title": "Coffee", "priority": "Low", "time": "17:00"}
    else:
        return {}

