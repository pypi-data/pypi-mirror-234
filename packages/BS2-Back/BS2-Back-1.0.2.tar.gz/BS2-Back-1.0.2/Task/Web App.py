from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import json
with open('Api.json', 'r') as f:
    info = json.load(f)

# Create the credentials object
creds = Credentials.from_authorized_user_info(info)

# Set up the API client
service = build('calendar', 'v3', credentials=creds)

from datetime import datetime, timedelta
import pytz

start_time = datetime(2023, 5, 5, 10, 0, 0, tzinfo=pytz.UTC)
end_time = start_time + timedelta(hours=1)

event = {
    'summary': 'New booking',
    'location': 'Location name',
    'description': 'Booking details',
    'start': {
        'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'UTC',
    },
    'end': {
        'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'UTC',
    },
}

try:
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')
except HttpError as error:
    print(f'An error occurred: {error}')
