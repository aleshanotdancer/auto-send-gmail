import os
import sys
from dotenv import load_dotenv, set_key
import BabyHi    
import send_mail  

ENV_PATH = ".env"
load_dotenv(ENV_PATH)

def force_exit():
    print("\n🛑 Stopping tool and exiting terminal... Goodbye!")
    sys.exit()

def update_sender_info():
    while True:
        print("\n--- [1] Update Sender Settings ---")
        print("1. Change Email only")
        print("2. Run Security Setup (Password)")
        print("3. Change Both")
        print("4. BACK TO MENU")
        print("5. STOP TOOL (EXIT)")
        sub_choice = input("Select (1-5): ").strip()

        if not sub_choice:
            print("⚠️ You must input a number to trigger the module!")
            continue

        if sub_choice == "1":
            new_email = input("Enter new sender email: ").strip()
            if not new_email: print("⚠️ No value to change, back to previous menu.")
            else:
                set_key(ENV_PATH, "EMAIL_USER", new_email)
                print("✅ Email updated.")
        elif sub_choice == "2":
            BabyHi.run_setup_wizard()
        elif sub_choice == "3":
            new_email = input("New email (leave blank to skip): ").strip()
            if new_email: set_key(ENV_PATH, "EMAIL_USER", new_email)
            BabyHi.run_setup_wizard()
        elif sub_choice == "4": break
        elif sub_choice == "5": force_exit()
        else: print(f"❌ '{sub_choice}' is not valid.")

def update_sheet_info():
    while True:
        print("\n--- [2] Update Google Sheet Settings ---")
        print("1. Change Source Sheet URL")
        print("2. Change GIDs (Summary, Template, List)")
        print("3. Change Everything")
        print("4. BACK TO MENU")
        print("5. STOP TOOL (EXIT)")
        sub_choice = input("Select (1-5): ").strip()

        if not sub_choice:
            print("⚠️ You must input a number!")
            continue

        if sub_choice == "1":
            new_url = input("Paste Sheet URL: ").strip()
            if not new_url: print("⚠️ No value to change.")
            else:
                set_key(ENV_PATH, "SOURCE_SHEET", new_url)
                print("✅ Source URL updated.")
        elif sub_choice == "2":
            new_sum = input("New GID Summary: ").strip()
            new_temp = input("New GID Template: ").strip()
            new_list = input("New GID List: ").strip()
            if not new_sum and not new_temp and not new_list: 
                print("⚠️ No values to change.")
            else:
                if new_sum: set_key(ENV_PATH, "GID_SUMMARY", new_sum)
                if new_temp: set_key(ENV_PATH, "GID_TEMPLATE", new_temp)
                if new_list: set_key(ENV_PATH, "GID_LIST", new_list)
                print("✅ GIDs updated.")
        elif sub_choice == "3":
            new_url = input("Paste Sheet URL (blank to skip): ").strip()
            new_sum = input("New GID Summary (blank to skip): ").strip()
            new_temp = input("New GID Template (blank to skip): ").strip()
            new_list = input("New GID List (blank to skip): ").strip()
            if not new_url and not new_sum and not new_temp and not new_list: 
                print("⚠️ No values to change.")
            else:
                if new_url: set_key(ENV_PATH, "SOURCE_SHEET", new_url)
                if new_sum: set_key(ENV_PATH, "GID_SUMMARY", new_sum)
                if new_temp: set_key(ENV_PATH, "GID_TEMPLATE", new_temp)
                if new_list: set_key(ENV_PATH, "GID_LIST", new_list)
                print("✅ All Sheet settings updated.")
        elif sub_choice == "4": break
        elif sub_choice == "5": force_exit()

def update_cooldown_settings():
    while True:
        load_dotenv(ENV_PATH, override=True)
        current_cd = os.getenv("COOLDOWN", "0")
        print(f"\n--- [3] Cooldown Settings (Current: {current_cd}s) ---")
        print("1. Change Cooldown Seconds")
        print("2. BACK TO MENU")
        print("3. STOP TOOL (EXIT)")
        sub_choice = input("Select (1-3): ").strip()

        if sub_choice == "1":
            new_cd = input("Enter cooldown seconds: ").strip()
            if not new_cd: print("⚠️ No value to change.")
            elif not new_cd.isdigit(): print("❌ Invalid input! Numbers only.")
            else:
                set_key(ENV_PATH, "COOLDOWN", new_cd)
                print(f"✅ Cooldown updated to {new_cd}s.")
        elif sub_choice == "2": break
        elif sub_choice == "3": force_exit()

def main():
    while True:
        print("\n==============================")
        print("      MACRO SENDING GMAIL     ")
        print("==============================")
        print("1. RUN MAILING JOB")
        print("2. Setup Sender (Email/Pass)")
        print("3. Setup Sheet (URL/GIDs)")
        print("4. Setup Cooldown Timer")
        print("5. EXIT")
        
        choice = input("\nSelect option (1-4). To exit select 5 then Enter: ").strip()

        if not choice:
            print("⚠️ You must input a number!")
            continue

        if choice == "1":
            load_dotenv(ENV_PATH, override=True)
            send_mail.run_job()
        elif choice == "2": update_sender_info()
        elif choice == "3": update_sheet_info()
        elif choice == "4": update_cooldown_settings()
        elif choice == "5": break
        else: print(f"❌ '{choice}' is an invalid choice.")

if __name__ == "__main__":
    main()
