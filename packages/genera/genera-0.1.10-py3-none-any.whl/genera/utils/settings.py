import json
import os

def load(caller_file_path, json_file_name):
    json_file_path = os.path.join(os.path.dirname(caller_file_path), json_file_name)
    with open(json_file_path, "r") as f:
        data = json.load(f)
        if "settings" in data:
            return data["settings"]
        else:
            return {}

def merge(setting_list):
    combined_settings = {}
    for settings in setting_list:
        combined_settings.update(settings)
    return combined_settings
