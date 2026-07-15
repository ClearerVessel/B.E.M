import json
from pathlib import Path
from cryptography.fernet import Fernet

class KeyVault:
    def __init__(self, usb_path: str, local_db_path: str = "passwords.json"):
        self.usb_path = Path(usb_path)
        self.keys_dir = self.usb_path / "vault_keys"
        self.local_db_path = Path(local_db_path)
        self.marker_file = self.usb_path / ".vault_active"


    def verify_key(self):
        if not self.usb_path.exists():
            raise FileNotFoundError(f"key drive not detected at '{self.usb_path}'. Please plug it in.")
        if not self.marker_file.exists():
            raise PermissionError("key drive detected, but vault marker is missing. Run setup first.")


    def setup_key(self):
        if not self.usb_path.exists():
            raise FileNotFoundError(f"Cannot find drive path '{self.usb_path}'.")
        self.keys_dir.mkdir(exist_ok=True)
        self.marker_file.touch(exist_ok=True)
        print(f"KEY Drive at '{self.usb_path}' initialized successfully!")


    def add_password(self, account_name: str, raw_password: str):
        self.verify_key()
        key = Fernet.generate_key()
        key_path = self.keys_dir / f"{account_name}.key"
        key_path.write_bytes(key)

        f = Fernet(key)
        encrypted_password = f.encrypt(raw_password.encode('utf-8')).decode('utf-8')

        db = self.load_db()
        db[account_name] = encrypted_password
        self.save_db(db)
        print(f"Password for '{account_name}' secured.")


    def update_password(self, account_name: str, new_password: str):
        self.verify_key()
        db = self.load_db()
        if account_name not in db:
            raise KeyError(f"Account '{account_name}' not found.")

        # generat a new key
        key = Fernet.generate_key()
        key_path = self.keys_dir / f"{account_name}.key"
        key_path.write_bytes(key)

        f = Fernet(key)
        enc_pass = f.encrypt(new_password.encode('utf-8')).decode('utf-8')

        db[account_name] = enc_pass
        self.save_db(db)
        print(f"Password for '{account_name}' has been updated.")


    def remove_password(self, account_name: str):
        self.verify_key()
        db = self.load_db()
        if account_name not in db:
            raise KeyError(f"Account '{account_name}' not found.")

        # Remove local encrypted password
        del db[account_name]
        self.save_db(db)

        # Remove key from USB
        key_path = self.keys_dir / f"{account_name}.key"
        if key_path.exists():
            key_path.unlink()

        print(f"Account '{account_name}' and its data have been ~Yeetus Deletus~.")


    def get_password(self, account_name: str) -> str:
        self.verify_key()
        db = self.load_db()
        if account_name not in db:
            raise KeyError(f"Account '{account_name}' not found.")

        encrypted_password = db[account_name].encode('utf-8')
        key_path = self.keys_dir / f"{account_name}.key"

        if not key_path.exists():
            raise FileNotFoundError(f"Key for '{account_name}' is missing from KEY drive!")

        key = key_path.read_bytes()
        f = Fernet(key)
        return f.decrypt(encrypted_password).decode('utf-8')


    def list_accounts(self):
        db = self.load_db()
        if not db:
            print("Bbbbut... its empty!")
            return
        print("\nStored accounts:")
        for account in sorted(db.keys()):
            print(f"  • {account}")


    def load_db(self) -> dict:
        if not self.local_db_path.exists():
            return {}
        try:
            return json.loads(self.local_db_path.read_text())
        except json.JSONDecodeError:
            return {}


    def save_db(self, db: dict):
        self.local_db_path.write_text(json.dumps(db, indent=4))