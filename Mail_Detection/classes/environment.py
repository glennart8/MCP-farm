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

    def act(self, email, decision, product=None):
        action_info = ""

        if decision == "support":  
            self.complaints.create_complaint(email)
            
            print("Skapar svar till klagomål")
            self.auto.create_auto_response_complaint(email)
            
            action_info = "Skapade supportärende"

        elif decision == "sales":
            # Skicka med produkten om den finns
            if product:
                self.sales.forward_to_sales(email, product)
                action_info = f"Vidarebefordrade till försäljning: {product}"
            else:
                self.sales.forward_to_sales(email)
                action_info = "Vidarebefordrade till försäljning (ingen produkt angiven)"

        elif decision == "meeting":
            print(f"Lägger till i kalendern: '{email['subject']}'")
            action_info = "Lade till möte i kalendern"

        else:
            # Låt LLM skapa autoreply utifrån meddelandet och den kontexten företaget befinner sig i
            # agent.create_auto_reply()
            self.auto.create_and_send_auto_reply(email)
            action_info = "Skickade autosvar"

        # Logga allt
        self.logs.append({
            "from": email["from"],
            "subject": email["subject"],
            "decision": decision,
            "action": action_info,
            "product": product
        })
        
    def save_logs(self):
        with open(self.logs_path, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)