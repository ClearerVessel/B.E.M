import os
import json

config_f= "BEM_config.json"

def load_config():
    if os.path.exists(config_f):
        try:
            with open(config_f, "r") as f:
                return json.load(f)
        except:
            return None
    return None

def save_config(usb_path, db_folder):
    try:
        with open(config_f, "w") as f:
            json.dump({"usb_path": usb_path, "db_folder": db_folder}, f, indent=4)
    except Exception as e:
        print(f"unable to save config: {e}")