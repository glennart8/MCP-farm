INBOX = [
    {"from": "kund1@example.com", "subject": "Reklamation av produkt", "body": "Produkten gick sönder efter en dag."},
    {"from": "kund5@example.com", "subject": "Vill köpa 100 enheter", "body": "Kan ni ge offert på 100 st?"},
    {"from": "kund4@example.com", "subject": "Möte på måndag", "body": "Vi behöver en presentation om kundsupporten."},
    {"from": "kund2@example.com", "subject": "Offert på virke", "body": "Vad kostar detta?"},
    {"from": "kund3@example.com", "subject": "Kostnad", "body": "Vad vill ni ha för denna inköpslista?"},
]

class EmailClient:
       
    def get_new_emails(self):
        if INBOX:
            return [INBOX.pop(0)]
        return []


