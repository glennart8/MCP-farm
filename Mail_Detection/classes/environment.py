import json
from pathlib import Path
from classes.complaints import ComplaintsSystem
from classes.mail import EmailClient
from classes.sales import SalesSystem
from classes.autoresponder import AutoResponder


class Environment:
    """Hantera e-postflödet och exekvering av AI-beslut."""
    def __init__(self):
        self.email_client = EmailClient()
        self.complaints = ComplaintsSystem()
        self.sales = SalesSystem()
        self.auto = AutoResponder()
        
        self.logs = [] 
        self.logs_path = Path("logs/logs.json")
        self.logs_path.parent.mkdir(parents=True, exist_ok=True)

    def observe(self):
        return self.email_client.get_new_emails()

    def act(self, email, decision):
        action_info = ""

        if decision == "support":
            self.complaints.create_complaint(email)
            action_info = "Skapade supportärende"
        elif decision == "sales":
            self.sales.forward_to_sales(email)
            action_info = "Vidarebefordrade till försäljning"
        elif decision == "meeting":
            print(f"Lägger till i kalendern: '{email['subject']}'")
            action_info = "Lade till möte i kalendern"
        else:
            self.auto.send_auto_reply(email)
            action_info = "Skickade autosvar"

        # 👇 Lägg till i logglistan
        self.logs.append({
            "from": email["from"],
            "subject": email["subject"],
            "decision": decision,
            "action": action_info
        })
        
    def save_logs(self):
        with open(self.logs_path, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)