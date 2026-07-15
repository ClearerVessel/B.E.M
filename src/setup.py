import sys
from pathlib import Path
from config import *

def initialize_paths():
    config = load_config()
    use_saved = False
    db_folder_input = ""

    if config:
        print("Configuration loaded...")
        print(f" • USB KEY PATH: {config.get('usb_path')}")
        print(
            f" • Database folder: "
            f"{config.get('db_folder') if config.get('db_folder') else 'Current Folder'}"
        )

        print("\nWelcome back...")
        print("----------------------------------------")

        ans = input(
            "Use previous locations?\n"
            "1. Yes\n"
            "2. No\n"
            "Answer: "
        ).strip().lower()

        if ans in ("1", "yes", "y", ""):
            use_saved = True
            usb_path = config.get("usb_path")
            db_folder_input = config.get("db_folder")

    if not use_saved:
        print("\n--- New Setup ---")
        print("Examples for Key Path:")
        print("  Windows: D:/ or F:/")
        print("  macOS:   /Volumes/MyUSB")
        print("  Linux:   /media/username/MyUSB")
        print("----------------------------------------")

        usb_path = input("Enter the path to your USB drive: ").strip()

        if not usb_path:
            print("Path cannot be empty.")
            sys.exit(1)

        print("\nDatabase File Location")
        print("Press Enter to use the current folder")
        print("or enter a custom folder.")

        db_folder_input = input("Folder path: ").strip()

    if db_folder_input:
        db_dir = Path(db_folder_input)

        try:
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "passwords.json"

        except Exception as e:
            print(f"Unable to use folder ({e})")
            print("Using current directory instead.")
            db_path = Path("passwords.json")

    else:
        db_path = Path("passwords.json")

    save_config(usb_path, db_folder_input)

    return usb_path, db_path