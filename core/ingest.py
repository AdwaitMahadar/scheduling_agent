# core/ingest.p
import json

def load_emails(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
