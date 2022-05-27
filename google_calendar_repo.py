import datetime
import os.path
from typing import List, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

import datetime_utils
from pairwise import pairwise

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

NUM_EVENTS = 1000


class GoogleCalendarRepository:
    def __init__(self, cred_file: str, token_file: str) -> None:
        """Initialise a GoogleCalendar object."""

        creds = self.__authenticate(token_file, cred_file)
        self.__service: Resource = build("calendar", "v3", credentials=creds)

    def get_calendar_events_for_period(
        self, start: datetime.datetime, end: datetime.datetime
    ) -> List[dict]:
        """Get calendar events."""
        event_results = {}
        try:
            event_results = (
                self.__service.events()
                .list(
                    calendarId="primary",
                    timeMin=start.isoformat() + "Z",
                    timeMax=end.isoformat() + "Z",
                    maxResults=NUM_EVENTS,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
        except HttpError as error:
            print(f"An error occurred while invoking Google API: ${error}")

        return event_results.get("items", [])

    def __authenticate(self, token_path: str, creds_path: str) -> Credentials:
        """Authenticate the application for use with Google APIs."""
        # The token file stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the
        # first time.
        creds: Credentials = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            if creds.valid:
                return creds

        # If there are no (valid) credentials available, let the user log in.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())

        return creds
