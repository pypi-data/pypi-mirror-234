import json
import os

def load(caller_file_path, json_file_name):
    json_file_path = os.path.join(os.path.dirname(caller_file_path), json_file_name)
    with open(json_file_path, "r") as f:
        data = json.load(f)
        if "options" in data:
            return data["options"]
        else:
            return {}
        
def merge(options_list):
    combined_options = {}
    for options in options_list:
        combined_options.update(options)
    return combined_options
