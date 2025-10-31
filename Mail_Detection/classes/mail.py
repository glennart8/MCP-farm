# INBOX = [
#     # klagomål
#     {"from": "kund1@example.com", "subject": "Reklamation av produkt", "body": "Produkten gick sönder efter en dag."},
    # {"from": "kund2@example.com", "subject": "Fel leverans", "body": "Jag fick fel produkt i min beställning."},
    # {"from": "kund3@example.com", "subject": "Försenad leverans", "body": "Min leverans har inte kommit trots att det gått två veckor."},
    # {"from": "kund4@example.com", "subject": "Skadad vara", "body": "Förpackningen var trasig och produkten skadad vid leverans."},
    # {"from": "kund5@example.com", "subject": "Faktureringsproblem", "body": "Jag har blivit debiterad två gånger för samma beställning."}
    
    # {"from": "kund5@example.com", "subject": "Vill köpa 100 enheter", "body": "Kan ni ge offert på 100 st?"},
    # {"from": "kund4@example.com", "subject": "Möte på måndag", "body": "Vi behöver en presentation om kundsupporten."},
    # {"from": "kund2@example.com", "subject": "Offert på virke", "body": "Vad kostar detta?"},
    # {"from": "kund3@example.com", "subject": "Kostnad", "body": "Vad vill ni ha för denna inköpslista?"},
    # {"from": "kund6@example.com", "subject": "Köpa mat", "body": "Jag skulle vilja köpa en banan"},
    
    # Other för autosvar
    # from: defineras i klassen just nu, sender_email
    # {"from": "testuser@example.com", "subject": "Hej där!", "body": "Ville bara säga hej och testa ditt system"},
    # {"from": "henrikpilback@gmail.com", "subject": "Test autosvar", "body": "Hej, detta är ett test."},
    
    # För möten
    # {"from": "kund_test@example.com", "subject": "Möte fastighet", "body": "Hej! Jag vill boka ett möte den 2:a november klockan 10.00. Funkar det?"}
# ]

MAIL_ACCOUNTS = [
    {"email": "henrikpilback@gmail.com", "label": "Support"},
    {"email": "nanformav@gmail.com", "label": "Sales"},
]

INBOX = [
    # {"from": "kund1@example.com", "subject": "Reklamation av produkt", "body": "Produkten gick sönder efter en dag."},
    # {"from": "kund2@example.com", "subject": "Vill köpa", "body": "Jag skulle vilja köpa en banan?"},
    # {"from": "kund3@example.com", "subject": "Vill köpa", "body": "Kan du lämna offert på detta: 10 st plywood, 5 st regel 45x95 och 10 st bräda 22x145?"},
    {"from": "henrikpilback@blinksbuy.com",
     "subject": "Vill köpa",
     "body": "Kan du lämna offert på detta: 10 st plywood, 5 st regel 45x95, 10 st bräda 22x145 och en låda spik 55mm?"},
]


class EmailClient:
       
    def get_new_emails(self):
        if INBOX:
            return [INBOX.pop(0)]
        return []
    


