import os, requests, pandas as pd, io, smtplib, time
from email.message import EmailMessage
from BabyBye import get_secret_baby
from dotenv import load_dotenv

def fetch_sheet(url):
    """Fetches CSV data with a Retry Mechanism."""
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            raw_data = response.content.decode('utf-8-sig')
            # Using header=None so we can search the entire sheet including the first row
            return pd.read_csv(io.StringIO(raw_data), keep_default_na=False, header=None)
        except Exception as e:
            if attempt < 2:
                print(f"⚠️ Connection glitch, retrying in 3s... (Attempt {attempt+1}/3)")
                time.sleep(3)
            else: raise e

def run_job():
    load_dotenv(override=True)
    
    while True:
        print("\n--- Auto send mail ---")
        print("1. Send to NEW only (Status is EMPTY)")
        print("2. Send to FAILED only")
        print("3. Send to RESEND only")
        print("4. Send to ALL (Ignore Status)")
        print("5. EXIT")
        
        mode = input("Select mode (1-4): ").strip()
        if not mode or mode == "5": return 
        if mode not in ["1", "2", "3", "4"]: continue

        try:
            base_url = os.getenv("SOURCE_SHEET").strip().rstrip('/')
            export_base = f"{base_url}/export?format=csv"
            
            # --- 1. GET SIGNATURE FROM SUMMARY SHEET ---
            summary_url = f"{export_base}&gid={os.getenv('GID_SUMMARY', '0')}"
            summary_df = fetch_sheet(summary_url)
            
            signature_html = ""
            found_sig = False
            for _, s_row in summary_df.iterrows():
                # Search every cell in the row for the keyword
                for i, cell_value in enumerate(s_row):
                    if "emailsignature" in str(cell_value).lower().replace(" ", ""):
                        # Take the cell to the right
                        if i + 1 < len(s_row):
                            signature_html = str(s_row[i + 1])
                            found_sig = True
                            break
                if found_sig: break
            
            if not found_sig:
                print("⚠️ Warning: Could not find cell labeled 'emailSignature' in Summary sheet.")
                signature_html = "<br><br>Sincerely"

            # --- 2. FETCH TEMPLATE & LIST ---
            # Re-fetching with headers for Template and List
            template_url = f"{export_base}&gid={os.getenv('GID_TEMPLATE')}"
            list_url = f"{export_base}&gid={os.getenv('GID_LIST')}"

            # Standard fetch (with headers)
            t_resp = requests.get(template_url)
            template_df = pd.read_csv(io.StringIO(t_resp.content.decode('utf-8-sig')), keep_default_na=False)
            
            l_resp = requests.get(list_url)
            list_df = pd.read_csv(io.StringIO(l_resp.content.decode('utf-8-sig')), keep_default_na=False)
            
            template_df['ID'] = template_df['ID'].astype(str).str.strip()
        except Exception as e:
            print(f"❌ Data Error: {e}"); continue

        # --- 3. SMART FILTERING ---
        list_df['Receiver'] = list_df['Receiver'].astype(str).str.strip()
        list_df['Status'] = list_df['Status'].astype(str).str.strip().str.lower()
        
        filtered_df = list_df[list_df['Receiver'].str.contains("@")].copy()
        filtered_df = filtered_df[filtered_df['Status'] != 'skip']

        if mode == "1": filtered_df = filtered_df[filtered_df['Status'] == ""]
        elif mode == "2": filtered_df = filtered_df[filtered_df['Status'].str.startswith("failed")]
        elif mode == "3": filtered_df = filtered_df[filtered_df['Status'] == "resend"]

        total_to_send = len(filtered_df)
        if total_to_send == 0:
            print("\n💡 INFO: Found 0 rows matching criteria."); continue

        # Cooldown & Login (Rest of your original base logic)
        env_val = os.getenv("COOLDOWN", "0")
        env_cd = int(env_val) if env_val.isdigit() else 0
        effective_cd = env_cd if env_cd >= 1 else 2
        use_cooldown = False

        if total_to_send > 50:
            use_cooldown = True
        elif mode != "4" and total_to_send <= 1:
            use_cooldown = False
        else:
            raw_ans = input(f"❓ Batch size is {total_to_send}. Use cooldown ({effective_cd}s)? (y/n): ").strip()
            if not raw_ans: continue 
            if raw_ans.lower() == 'y': use_cooldown = True

        baby = get_secret_baby()
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(os.getenv("EMAIL_USER"), baby)
            print("✅ Gmail Connected!")
        except Exception as e:
            print(f"❌ Login failed: {e}"); continue

        sent_count = 0
        for index, row in filtered_df.iterrows():
            receiver_email = row['Receiver']
            mail_id = str(row.get('Mail ID', '')).strip()

            try:
                match = template_df[template_df['ID'] == mail_id]
                if match.empty: continue
                
                curr = match.iloc[0]
                subj_tpl = str(curr.get('Subject', '')).replace('\n', '').replace('\r', '')
                body_tpl = str(curr.get('Body', ''))

                p_raw = str(row.get('Pronoun', '')).strip()
                f_name = str(row.get('Fullname', '')).strip().title()
                n_name = str(row.get('Name', '')).strip().title()
                v_key = str(row.get('Key', '')).strip()

                req = {"Fullname": f_name, "Name": n_name, "Pronoun": p_raw, "Key": v_key}
                missing = [p for p, v in req.items() if f"{{{p}}}" in (body_tpl + subj_tpl) and not v]
                if missing: continue

                p_l, p_c = p_raw.lower(), p_raw.capitalize()
                final_subj = subj_tpl.format(Name=n_name, Pronoun=p_l, CPronoun=p_c)
                final_body = (f"Dear {f_name},\n\n" + body_tpl).format(Name=n_name, Pronoun=p_l, CPronoun=p_c, Key=v_key, Fullname=f_name)

                msg = EmailMessage()
                msg['From'] = os.getenv("EMAIL_USER")
                msg['To'] = receiver_email
                msg['Subject'] = final_subj
                msg.set_content(final_body)
                msg.add_alternative(final_body.replace("\n", "<br>") + "<br><br>" + signature_html, subtype='html')

                server.send_message(msg)
                print(f"[{index+1}] SUCCESS: {receiver_email}")
                sent_count += 1
                
                if use_cooldown and receiver_email != filtered_df.iloc[-1]['Receiver']:
                    time.sleep(effective_cd)
            except Exception as e:
                print(f"[{index+1}] FAILED: {receiver_email} | {e}")

        server.quit()
        print(f"\n--- Job Finished. Sent {sent_count} targeted emails. ---\n")

if __name__ == "__main__":
    run_job()
