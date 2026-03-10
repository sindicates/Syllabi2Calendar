import os.path
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import json as _json
import time as _time

SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('calendar', 'v3', credentials=creds)


def create_event(event_data, school_tz):
    service = get_calendar_service()
    
    start_str = str(event_data.get('start'))
    is_timed = "T" in start_str
    event = {
        'summary': event_data['summary'],
        'description': event_data['description'],
        'start': {},
        'end': {},
    }

    # region agent log
    try:
        with open("debug-b18514.log", "a", encoding="utf-8") as _f:
            _f.write(_json.dumps({
                "sessionId": "b18514",
                "runId": "pre-fix",
                "hypothesisId": "H4",
                "location": "calendar_service.py:create_event",
                "message": "Entering create_event",
                "data": {
                    "summary": event_data.get("summary"),
                    "start": event_data.get("start"),
                    "end": event_data.get("end"),
                    "school_tz": school_tz,
                    "is_timed": is_timed
                },
                "timestamp": int(_time.time() * 1000)
            }) + "\n")
    except Exception:
        pass
    # endregion agent log

    if is_timed:

        event['start']['dateTime'] = event_data['start']
        event['end']['dateTime'] = event_data['end']

        event['start']['timeZone'] = school_tz
        event['end']['timeZone'] = school_tz

    else:

        try:

            start_date = datetime.strptime(start_str, "%Y-%m-%d")
            end_date = start_date + timedelta(days=1)
            event['start']['date'] = start_str
            event['end']['date'] = end_date.strftime("%Y-%m-%d")

        except Exception as e:
            
            print(f"Date parsing error: {e}")

            # region agent log
            try:
                with open("debug-b18514.log", "a", encoding="utf-8") as _f:
                    _f.write(_json.dumps({
                        "sessionId": "b18514",
                        "runId": "pre-fix",
                        "hypothesisId": "H5",
                        "location": "calendar_service.py:create_event",
                        "message": "Date parsing error",
                        "data": {
                            "start_str": start_str,
                            "error": str(e)
                        },
                        "timestamp": int(_time.time() * 1000)
                    }) + "\n")
            except Exception:
                pass
            # endregion agent log

            return None


    try:

        event_result = service.events().insert(calendarId='primary', body=event).execute()

        # region agent log
        try:
            with open("debug-b18514.log", "a", encoding="utf-8") as _f:
                _f.write(_json.dumps({
                    "sessionId": "b18514",
                    "runId": "pre-fix",
                    "hypothesisId": "H6",
                    "location": "calendar_service.py:create_event",
                    "message": "Event created via API",
                    "data": {
                        "event_id": event_result.get("id"),
                        "htmlLink": event_result.get("htmlLink")
                    },
                    "timestamp": int(_time.time() * 1000)
                }) + "\n")
        except Exception:
            pass
        # endregion agent log

        return event_result.get('htmlLink')

    except Exception as e:

        print(f"Error creating event: {e}")

        # region agent log
        try:
            with open("debug-b18514.log", "a", encoding="utf-8") as _f:
                _f.write(_json.dumps({
                    "sessionId": "b18514",
                    "runId": "pre-fix",
                    "hypothesisId": "H7",
                    "location": "calendar_service.py:create_event",
                    "message": "API error creating event",
                    "data": {
                        "error": str(e)
                    },
                    "timestamp": int(_time.time() * 1000)
                }) + "\n")
        except Exception:
            pass
        # endregion agent log

        return None
