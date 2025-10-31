import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
from .agents import ComplaintAgent

agent = ComplaintAgent()


# Vilka behörigheter ska appen ha - SEND
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class AutoResponder:
    def __init__(self):
        self.service = self.authenticate_gmail()
        self.sender_email = "henrikpilback@gmail.com"

    def authenticate_gmail(self):
        creds = None
        # kollar autentiserings-token så man slipper logga in varje gång
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token: # om token kan uppdateras - gör det
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES) # innehåller klient-ID och hemlighet från Google Cloud Console.
                creds = flow.run_local_server(port=0) # Öppnar webbläsare,loggar in på gmail ge behörighet och generar ett nytt token
            with open('token.pickle', 'wb') as token: # Sparar token lokalt
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds) # Skapar ett Gmail service-objekt

    def create_and_send_auto_reply(self, email):
        subject = f"Autosvar: {email['subject']}"
        body = f"Hej svejs!\n\nTack för ditt mejl: {email['body']}\nVi återkommer snart."
        self._send_email(email['from'], subject, body)
        
    
    def _send_email(self, to, subject, body):
        message = MIMEText(body)
        message['to'] = to
        message['from'] = self.sender_email
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode() # Kodar mejlet till base64-url (krav för Gmail API).
        self.service.users().messages().send(userId='me', body={'raw': raw}).execute() # Skickar mejlet via Gmail API
        print(f"Autosvar skickat till {to}")

    def create_auto_response_complaint(self, email):
        subject = f"Svar på klagomål: {email['subject']}"
        body = agent.write_response_to_complaint(email)
        self._send_email(email['from'], subject, body)
        