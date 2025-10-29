import time

""" Kan användas för:
        - Sortera inkommande mejl
        - Skapa automatiska ärenden i Zendesk/Jira
        - Göra regelbaserade beslut i kundservice
        - Automatiskt svara på enklare frågor
"""

# --- Mockdata: nya mejl som dyker upp ---
INBOX = [
    {"from": "kund1@example.com", "subject": "Reklamation av produkt", "body": "Produkten gick sönder efter en dag."},
    {"from": "kund5@example.com", "subject": "Vill köpa 100 enheter", "body": "Kan ni ge offert på 100 st?"},
    {"from": "kund4@example.com", "subject": "Möte på måndag", "body": "Vi behöver en presentation om kundsupporten."},
    {"from": "kund2@example.com", "subject": "Offert på virke", "body": "Vad kostar detta?"},
    {"from": "kund3@example.com", "subject": "Kostnad", "body": "Vad vill ni ha för denna inköptslista?"},
]

class EmailClient:
    """Simulerar en e-postklient."""
    def get_new_emails(self):
        if INBOX:
            return [INBOX.pop(0)]
        return []

class TicketSystem:
    """Simulerar ett supportsystem."""
    def create_ticket(self, email):
        print(f"Skapar ärende: '{email['subject']}' från {email['from']}")

class SalesSystem:
    """Simulerar ett försäljningssystem."""
    def forward_to_sales(self, email):
        print(f"Vidarebefordrar till försäljning: '{email['subject']}'")

class AutoResponder:
    """Skickar automatiska svar."""
    def send_auto_reply(self, email):
        print(f"Autosvar till {email['from']}. Ditt meddelande har tagit emot och vi återkommer snarast.")

class MCP_Email_Agent:
    def __init__(self):
        self.client = EmailClient()
        self.tickets = TicketSystem()
        self.sales = SalesSystem()
        self.auto = AutoResponder()

    def observe(self):
        emails = self.client.get_new_emails()
        print(f"Hittade {len(emails)} nya mejl")
        return emails

    # Här skulle en AI-AGENT användas för att slippa tusen if-satser
    def decide(self, email):
        text = (email["subject"] + email["body"]).lower()
        if "reklamation" in text or "problem" in text or "trasig" in text:
            return "support"
        elif "köp" in text or "offert" in text or "kostar" in text:
            return "sales"
        else:
            return "auto_reply"

    def act(self, email, decision):
        if decision == "support":
            self.tickets.create_ticket(email)
        elif decision == "sales":
            self.sales.forward_to_sales(email)
        else:
            self.auto.send_auto_reply(email)

# --- Kör loopen ---
agent = MCP_Email_Agent()

for _ in range(5):
    emails = agent.observe()
    for email in emails:
        decision = agent.decide(email)
        agent.act(email, decision)
    time.sleep(2)
