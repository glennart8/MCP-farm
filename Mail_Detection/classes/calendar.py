import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarHandler:
    def __init__(self):
        self.service = self.authenticate_calendar()

    def authenticate_calendar(self):
        creds = None
        if os.path.exists('token_calendar.pickle'):
            with open('token_calendar.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token_calendar.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return build('calendar', 'v3', credentials=creds)

from datetime import datetime, timedelta

class CalendarHandler(CalendarHandler): 
    def create_event(self, subject, body, start_time, duration_minutes=60):
        end_time = start_time + timedelta(minutes=duration_minutes)
        event = {
            'summary': subject,       # <--- rätt fält för titel
            'description': body,      # <--- rätt fält för beskrivning
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Europe/Stockholm',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Europe/Stockholm',
            },
        }
        created_event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f"Möte skapat: {created_event.get('htmlLink')}")