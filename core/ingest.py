import json

def load_emails_from_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
