import json
from pathlib import Path
from classes.complaints import ComplaintsSystem
from classes.mail import EmailClient, MAIL_ACCOUNTS
from classes.sales import SalesSystem
from classes.autoresponder import AutoResponder
from classes.calendar import CalendarHandler
from datetime import datetime, timedelta

class Environment:
    """Hantera exekvering av AI-beslut."""
    def __init__(self):
        self.email_client = EmailClient()
        self.complaints = ComplaintsSystem()
        self.sales = SalesSystem()
        self.auto = AutoResponder()
        self.calendar = CalendarHandler()
        
        self.logs = [] 
        self.logs_path = Path("logs/logs.json")
        self.logs_path.parent.mkdir(parents=True, exist_ok=True)

    def observe(self):
        return self.email_client.get_new_emails()

    def act(self, email, decision, product=None, meeting_time=None):
        action_info = ""

        # Om klagomål: Logga klagomålet och skicka ett AI-genererat mail till brevskrivaren
        if decision == "support":  
            self.complaints.log_complaint(email)
    
            to = "henrikpilback@gmail.com"  # support-mail
            self.auto.create_auto_response_complaint(email, to)
            print(f"Support-mail ska skickas till: {to}")
            
            action_info = f"Skapade supportärende och skickade till {to}"
        
        # Om offer: AI läser mail - plockar ut vad som vill köpas, mappar mot produkter, om en vara saknas föreslås ett likvädigt alternativ - skicakr bekräftelsemail
        elif decision == "sales":
            if product:
                # Skicka offert baserat på produkt(er) i mailet
                self.sales.create_quote(email)
                action_info = f"Offert skickad för produkter från mail"
            else:
                # Om LLM inte hittade produkter, skicka mail om att klargöra
                self.sales.create_quote(email)  # eller separat logik för "okänd produkt"
                action_info = "Offert skickad (okända produkter, LLM försöker extrahera)"

        # Om möte: Skapar ett event i google calender, om mötestid nämndes i mailet, sätt tiden till detta, annars sätt till nu.
        elif decision == "meeting":
            if meeting_time:
                start_time = datetime.fromisoformat(meeting_time) 
            else:
                start_time = datetime.now() + timedelta(hours=1)
            self.calendar.create_event(
                subject=email['subject'],
                body=email['body'],
                start_time=start_time,
                duration_minutes=30
    )

        # Other: ger autosvar just nu. Kan ju ändras till " om ett visst tillstånd - anropa"
        else:
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
        
        
    # Logga alla mail    
    def save_logs(self):
        with open(self.logs_path, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)