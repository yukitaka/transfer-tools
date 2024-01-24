import json

def save_json(path, data):
    text = json.dumps(data, sort_keys=True, indent=4, separators=(", ", ": "))
    save_file(path, text)


def save_file(path, text):
    with open(path, mode="w") as f:
        f.write(text)
