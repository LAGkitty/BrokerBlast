import smtplib
import tkinter as tk
from tkinter import ttk, messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading

# =====================================================================
# DATA BROKER DATABASE (UPDATED 2026)
# Oracle removed (email decommissioned). Replaced with Intelius.
# Acxiom updated to their active 'askprivacy' endpoint.
# =====================================================================
DATA_BROKERS = [
    {"name": "Acxiom", "email": "askprivacy@acxiom.com"},
    {"name": "Epsilon", "email": "privacy@epsilon.com"},
    {"name": "Experian Marketing", "email": "optout@experian.com"},
    {"name": "Equifax Commercial", "email": "cust.serv@equifax.com"},
    {"name": "LexisNexis", "email": "privacy.policy@lexisnexis.com"},
    {"name": "LiveRamp", "email": "optout@liveramp.com"},
    {"name": "CoreLogic", "email": "privacy@corelogic.com"},
    {"name": "Intelius / PeopleConnect", "email": "privacy@peopleconnect.us"}
]

# =====================================================================
# GUI APPLICATION CLASS
# =====================================================================
class PrivacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoPrivacy - Data Broker Eraser")
        self.root.geometry("650x550")
        self.root.minsize(550, 450)
        
        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(root)
        # BUGFIX: Using pady=10 (not py=10)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Define Tabs
        self.tab_app = ttk.Frame(self.notebook)
        self.tab_tutorial = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_app, text="Automation Tool")
        self.notebook.add(self.tab_tutorial, text="How to Use (Tutorial)")
        
        self.build_app_tab()
        self.build_tutorial_tab()

    # --- MAIN AUTOMATION INTERFACE ---
    def build_app_tab(self):
        # Configuration Frame
        config_frame = ttk.LabelFrame(self.tab_app, text=" Step 1: Email Configuration ", padding=10)
        config_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(config_frame, text="Your Gmail Account:").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_email_sender = ttk.Entry(config_frame, width=40)
        self.ent_email_sender.grid(row=0, column=1, pady=2, padx=5, sticky="ew")
        
        ttk.Label(config_frame, text="Google App Password:").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_email_pass = ttk.Entry(config_frame, width=40, show="*")
        self.ent_email_pass.grid(row=1, column=1, pady=2, padx=5, sticky="ew")
        
        config_frame.columnconfigure(1, weight=1)

        # Personal Details Frame
        details_frame = ttk.LabelFrame(self.tab_app, text=" Step 2: Target Information to Delete ", padding=10)
        details_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(details_frame, text="Full Name:").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_name = ttk.Entry(details_frame, width=40)
        self.ent_name.grid(row=0, column=1, pady=2, padx=5, sticky="ew")
        
        ttk.Label(details_frame, text="Phone Number:").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_phone = ttk.Entry(details_frame, width=40)
        self.ent_phone.grid(row=1, column=1, pady=2, padx=5, sticky="ew")
        
        ttk.Label(details_frame, text="Target Email:").grid(row=2, column=0, sticky="w", pady=2)
        self.ent_target_email = ttk.Entry(details_frame, width=40)
        self.ent_target_email.grid(row=2, column=1, pady=2, padx=5, sticky="ew")
        
        details_frame.columnconfigure(1, weight=1)

        # Action Frame
        action_frame = ttk.Frame(self.tab_app, padding=5)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        self.btn_run = ttk.Button(action_frame, text="🚀 Blast Deletion Requests", command=self.start_automation_thread)
        self.btn_run.pack(fill="x", ipady=5)

        # Console Log Output
        log_frame = ttk.LabelFrame(self.tab_app, text=" Status Log ", padding=5)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.txt_log = tk.Text(log_frame, height=10, state="disabled", wrap="word", bg="#f4f4f4", font=("Courier", 9))
        self.txt_log.pack(fill="both", expand=True)

    # --- TUTORIAL DOCUMENTATION TAB ---
    def build_tutorial_tab(self):
        tutorial_text = tk.Text(self.tab_tutorial, wrap="word", padx=15, pady=15, font=("Arial", 10))
        tutorial_text.pack(fill="both", expand=True)
        
        tutorial_content = """# AutoPrivacy Script Tutorial & Guide

Welcome to the Data Broker Eraser app! This tool automates the process of exercising your GDPR Article 17 "Right to Be Forgotten" by emailing legal data removal demands directly to data broker infrastructure.

## 🛠 Prerequisites: Getting a Google App Password
Standard passwords will NOT work with this tool because Google blocks automated scripts from logging in directly for security profiles.

Follow these quick steps to get a usable password:
1. Go to your Google Account Dashboard (https://myaccount.google.com).
2. Click on 'Security' in the left-hand navigation pane.
3. Scroll down to 'How you sign in to Google' and verify that '2-Step Verification' is turned ON.
4. Click inside '2-Step Verification', scroll all the way to the absolute bottom of the screen, and click 'App passwords'.
5. Enter an app name (e.g., "Privacy Script") and click 'Create'.
6. Google will give you a 16-character code. Copy this code directly into the 'Google App Password' field on the first tab of this application.

## 📈 Execution
1. Fill in your Name, Phone Number, and Primary Email exactly as they appear across online profiles (use international formatting for numbers).
2. Hit 'Blast Deletion Requests'.
3. Keep an eye on your actual Gmail inbox over the next 48 hours. Several data brokers will automatically reply with confirmation or verification links that you MUST click to confirm ownership.

---
Disclaimer: This software acts as an automated transport mechanism for processing user-specified legal communications. Use responsibly.
"""
        tutorial_text.insert("1.0", tutorial_content)
        tutorial_text.config(state="disabled")

    # --- LOGIC & THREADING ENGINE ---
    def log(self, message):
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

    def start_automation_thread(self):
        # Validate inputs are not empty
        if not all([self.ent_email_sender.get(), self.ent_email_pass.get(), 
                    self.ent_name.get(), self.ent_phone.get(), self.ent_target_email.get()]):
            messagebox.showwarning("Missing Fields", "Please populate all configuration and target data fields before continuing.")
            return
            
        self.btn_run.config(state="disabled")
        # Run execution inside a separate worker thread to prevent GUI freezing
        threading.Thread(target=self.execute_blast, daemon=True).start()

    def execute_blast(self):
        sender = self.ent_email_sender.get().strip()
        password = self.ent_email_pass.get().strip()
        name = self.ent_name.get().strip()
        phone = self.ent_phone.get().strip()
        target_email = self.ent_target_email.get().strip()
        
        self.log("Connecting securely to smtp.gmail.com (TLS)...")
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            self.log("✓ Authentication Successful. Processing broker batch queue...\n")
        except Exception as e:
            self.log(f"✗ ERROR: Authentication failed: {e}")
            self.log("\nPlease confirm your App Password is correct and that 2-Step verification is enabled.")
            self.root.after(0, lambda: self.btn_run.config(state="normal"))
            return

        subject = "Data Erasure Request (GDPR Article 17 / Right to Be Forgotten)"
        body_template = """Dear Privacy Team at {broker_name},

I am writing to you in my capacity as a data subject to exercise my Right to Erasure under Article 17 of the General Data Protection Regulation (GDPR). 

Please permanently delete all personal data and records associated with me from your systems, databases, and marketing lists. This includes, but is not limited to, my name, phone number, and any associated tracking or identity records.

My Identifiable Information:
- Full Name: {user_name}
- Phone Number: {user_phone}
- Primary Email: {user_email}

Please confirm via email once the erasure process has been completed. 

Sincerely,
{user_name}"""

        for broker in DATA_BROKERS:
            b_name = broker["name"]
            b_email = broker["email"]
            
            self.log(f"Assembling legal request -> {b_name} ({b_email})")
            body = body_template.format(broker_name=b_name, user_name=name, user_phone=phone, user_email=target_email)
            
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = b_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            try:
                server.send_message(msg)
                self.log(f"  -> SUCCESS: Outbound request dispatched.")
            except Exception as e:
                self.log(f"  -> FAILED: System transmission error: {e}")
                
        server.quit()
        self.log("\n=======================================================")
        self.log("🎉 Automation Loop Finished!")
        self.log("Check your inbox for incoming verification tickets.")
        self.log("=======================================================")
        
        # Re-enable button on complete
        self.root.after(0, lambda: self.btn_run.config(state="normal"))
        messagebox.showinfo("Success", "All privacy requests have been broadcast successfully!")

# =====================================================================
# RUN APPLICATION ENTRYPOINT
# =====================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = PrivacyApp(root)
    root.mainloop()