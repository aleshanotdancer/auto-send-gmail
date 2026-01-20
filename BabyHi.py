import sys
from cryptography.fernet import Fernet

def force_exit():
    print("\n🛑 Exiting... Goodbye!")
    sys.exit()

def run_setup_wizard():
    print("\n--- [Baby and Key Setup Wizard] ---")
    raw_baby = input("Enter your Baby (Gmail App Pass): ").strip()
    if not raw_baby:
        print("⚠️ No value entered. Cancelled.")
        return

    key = Fernet.generate_key()
    cipher = Fernet(key)
    enc = cipher.encrypt(raw_baby.encode())

    print(f"\nBABY_KEY={key.decode()}\nENCRYPTED_BABY={enc.decode()}\n")

    while True:
        choice = input("Save to .env? [Y]es / [N]o / [X] Stop Tool: ").strip().lower()
        if choice == 'y':
            from main import set_key, ENV_PATH
            set_key(ENV_PATH, "BABY_KEY", key.decode())
            set_key(ENV_PATH, "ENCRYPTED_BABY", enc.decode())
            print("✅ .env updated.")
            break
        elif choice == 'n' or not choice: break
        elif choice == 'x': force_exit()
