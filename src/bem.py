VERSION = "0.3.1"

from vault import KeyVault
from utils import clear_screen
from setup import  initialize_paths
from menu import run_menu
from art import banner_art

def main():
    clear_screen()

    print(banner_art)

    usb_path, db_path = initialize_paths()

    vault = KeyVault(
        usb_path=usb_path,
        local_db_path=db_path
    )

    run_menu(vault)

if __name__ == "__main__":
    main()