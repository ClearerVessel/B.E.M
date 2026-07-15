from getpass import getpass
from art import vault_art
from utils import clear_screen


def setup_usb(vault):
    vault.setup_key()


def list_accounts_ui(vault):
    vault.list_accounts()


def add_password_ui(vault):
    account = input("Enter account name: ").strip()

    if not account:
        print("Account name cannot be empty.")
        return

    password = getpass(f"Enter password for '{account}': ")
    confirm = getpass("Confirm password: ")

    if password != confirm:
        print("Passwords do not match!")
        return

    vault.add_password(account, password)


def get_password_ui(vault):
    account = input("Enter account name: ").strip()

    if not account:
        print("Account name cannot be empty.")
        return

    password = vault.get_password(account)

    print(f"\n🔑 Password for '{account}': {password}")


def update_password_ui(vault):
    account = input("Enter account name: ").strip()

    if not account:
        print("Account name cannot be empty.")
        return

    password = getpass(f"Enter NEW password for '{account}': ")
    confirm = getpass("Confirm NEW password: ")

    if password != confirm:
        print("Passwords do not match!")
        return

    vault.update_password(account, password)


def remove_password_ui(vault):
    account = input("Enter account to remove: ").strip()

    if not account:
        print("Account name cannot be empty.")
        return

    confirm = input(
        f"Delete '{account}'? "
        "This cannot be undone. "
        "Type 'DELETE' to confirm: "
    ).strip()

    if confirm != "DELETE":
        print("Cancelled.")
        return

    vault.remove_password(account)


def display_menu():
    clear_screen()

    print(vault_art,"\n")
    print("========================================")
    print("1. Setup USB Drive")
    print("2. List all accounts")
    print("3. Add new password")
    print("4. Get password")
    print("5. Update password")
    print("6. Remove account")
    print("7. Exit")
    print("========================================")
    print()


def run_menu(vault):

    actions = {
        "1": setup_usb,
        "2": list_accounts_ui,
        "3": add_password_ui,
        "4": get_password_ui,
        "5": update_password_ui,
        "6": remove_password_ui,
    }

    while True:

        display_menu()

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "7":
            print("Goodbye!")
            break

        action = actions.get(choice)

        if action:
            try:
                action(vault)

            except Exception as e:
                print(f"Error: {e}")

        else:
            print("Please choose a number from 1 to 7.")

        input("\nPress Enter to continue . . .")