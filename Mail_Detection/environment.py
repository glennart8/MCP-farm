import json

INBOX = [
    {"from": "kund1@example.com", "subject": "Reklamation av produkt", "body": "Produkten gick sönder efter en dag."},
    {"from": "kund5@example.com", "subject": "Vill köpa 100 enheter", "body": "Kan ni ge offert på 100 st?"},
    {"from": "kund4@example.com", "subject": "Möte på måndag", "body": "Vi behöver en presentation om kundsupporten."},
    {"from": "kund2@example.com", "subject": "Offert på virke", "body": "Vad kostar detta?"},
    {"from": "kund3@example.com", "subject": "Kostnad", "body": "Vad vill ni ha för denna inköpslista?"},
]

# --- ANVÄND RIKTIGT MAIL ---
class EmailClient:
    def get_new_emails(self):
        if INBOX:
            return [INBOX.pop(0)]
        return []

# --- SKAPA ETT OBJEKT I RÄTT KATEGORI ---
class TicketSystem:
    def create_ticket(self, email):
        print(f"Skapar ärende: '{email['subject']}'")

# --- VIDAREBEFORDRA MAIL ---
class SalesSystem:
    def forward_to_sales(self, email):
        print(f"Vidarebefordrar till försäljning: '{email['subject']}'")

# --- AUTOGENERERA ETT MAIL ---
class AutoResponder:
    def send_auto_reply(self, email):
        print(f"Skickar autosvar till: {email['from']}")


class Environment:
    """Hantera e-postflödet och exekvering av AI-beslut."""
    def __init__(self):
        self.email_client = EmailClient()
        self.tickets = TicketSystem()
        self.sales = SalesSystem()
        self.auto = AutoResponder()
        
        self.logs = [] 
        
    def log_inbox(self):
        with open("logs.json", "w", encoding="utf-8") as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)  

    def observe(self):
        return self.email_client.get_new_emails()

    def act(self, email, decision):
        action_info = ""

        if decision == "support":
            self.tickets.create_ticket(email)
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