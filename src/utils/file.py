import os
import json

def save_json(path, data):
    text = json.dumps(data, sort_keys=True, indent=4, separators=(", ", ": "))
    save_file(path, text)


def save_file(path, text):
    with open(path, mode="w") as f:
        f.write(text)

def load_json(path):
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return json.load(f)

def load_jsons(data):
    return json.loads(data)
