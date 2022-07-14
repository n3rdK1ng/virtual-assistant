from __future__ import print_function

import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

with open('/Users/marcovelan/Desktop/AP/virtual-assistant/shifts.json') as json_file:
    shifts = json.load(json_file)

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/Users/marcovelan/Desktop/AP/virtual-assistant/token.json'):
        creds = Credentials.from_authorized_user_file('/Users/marcovelan/Desktop/AP/virtual-assistant/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:

        service = build('calendar', 'v3', credentials=creds)

        # Create event

        """event = {
            'summary': 'Test',
            'location': 'Čs. exilu 669, 708 00 Ostrava-Poruba',
            'description': 'testing',
            'start': {
                'dateTime': '2022-5-1T4:00:00+02:00',
                'timeZone': 'Europe/Prague',
            },
            'end': {
                'dateTime': '2022-5-1T5:00:00+02:00',
                'timeZone': 'Europe/Prague',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},
                ],
            },
        }"""

        for shift in shifts:

            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            duplicateEvents = True

            while duplicateEvents == True:

                events_result = service.events().list(calendarId='primary', timeMin=now,
                                                    maxResults=1, singleEvents=True,
                                                    orderBy='startTime').execute()
                events = events_result.get('items', [])

                if not events:
                    print('No upcoming events found.')
                    return

                event = events[0]
                eventID = event['id']
                eventSummary = event['summary']
                eventStart = event['start'].get('dateTime', event['start'].get('date'))
                eventDate = eventStart[5:10]
                
                #shift = service.events().insert(calendarId='primary', body=event).execute()
                #print('Event created: %s' % (shift.get('htmlLink')))
                shiftStart = shift['start'].get('dateTime', shift['start'].get('date'))
                shiftDate = shiftStart[5:10]
                shiftSummary = shift['summary']

                if (eventSummary == shiftSummary) and (eventDate == shiftDate):
                    service.events().delete(calendarId='primary', eventId=eventID).execute()
                    print('Duplicate event deleted.')
                else:
                    duplicateEvents = False
                    shift = service.events().insert(calendarId='primary', body=event).execute()
                    print('Event created: %s' % (shift.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()