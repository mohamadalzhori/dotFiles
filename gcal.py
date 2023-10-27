from __future__ import print_function

import datetime
import os.path
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

IGNORED_CALENDAR_IDS = ['l5kpvt181if6m1m03g66ugpehs@group.calendar.google.com','agdt2hkur9djcabtnlp1fif4unhmj456@import.calendar.google.com']  # Add calendar IDs to ignore


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next event on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/home/zhori/.local/bin/scripts/token.json'):
        creds = Credentials.from_authorized_user_file('/home/zhori/.local/bin/scripts/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/zhori/.local/bin/scripts/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/home/zhori/.local/bin/scripts/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        earliest_event = None
        earliest_event_time = None

        for calendar in calendars:
            calendar_id = calendar['id']
            if calendar_id in IGNORED_CALENDAR_IDS:
                #print(f"Ignoring calendar: {calendar['summary']}")
                continue
            #print(f"Fetching events from calendar: {calendar['summary']}")

            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                                  maxResults=1, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            if events:
                event = events[0]
                start = event['start'].get('dateTime', event['start'].get('date'))

                event_start_time_utc = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                event_start_time = event_start_time_utc.replace(tzinfo=pytz.UTC)

                if earliest_event_time is None or event_start_time < earliest_event_time:
                    earliest_event = event
                    earliest_event_time = event_start_time

        if earliest_event:
            event_time_formatted = earliest_event_time.strftime('%I:%M %p')
            print(f"{event_time_formatted}, {earliest_event['summary']}")
        else:
            print('No upcoming events found in any calendar.')

    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    main()
