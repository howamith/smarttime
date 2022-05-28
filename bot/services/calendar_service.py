from datetime import datetime, timedelta
from typing import List, Tuple

from helpers import datetime_utils
from repos.google_calendar_repo import GoogleCalendarRepository
from helpers.pairwise import pairwise


class CalendarService:
    def __init__(self, email: str) -> None:
        self.__email = email
        self.__repo = GoogleCalendarRepository(
            "credentials.json", "token.json"
        )

    def get_focus_time_opportunities(self, threshold: timedelta) -> dict:
        """Get a list of focus time opportunies"""
        # Get the current working week's events.
        week_start, week_end = datetime_utils.get_current_working_week()
        events = self.__repo.get_calendar_events_for_period(
            week_start, week_end
        )

        # Filter out events we aren't attending then convert timestamps into
        # datetime objects.
        events = [e for e in events if self.__is_attending(self.__email, e)]
        self.__convert_event_timestamps(events)

        opportunities = {}
        days = self.__split_week(events)
        for day in days:
            day_opportunities = []
            for first, second in pairwise(day):
                # Ensure this isn't a clash.
                if second["start"] > first["end"]:
                    time_between = second["start"] - first["end"]
                    if time_between >= threshold:
                        t = datetime_utils.format_timedelta(
                            second["start"] - first["end"]
                        )
                        day_opportunities.append(
                            f"{t} between {first['summary']} and {second['summary']}"
                        )

            if day_opportunities:
                date = day[0]["start"].date().strftime("%d/%m/%Y")
                opportunities[date] = day_opportunities

        return opportunities

    def __convert_event_timestamps(self, events: List[dict]) -> None:
        """Convert a events' timestamps to datetime objects."""
        for event in events:
            start, end = self.__get_event_start_and_end(event)
            event["start"] = start
            event["end"] = end

    def __get_event_start_and_end(
        self,
        event: dict,
    ) -> Tuple[datetime, datetime]:
        """Get the start and end datetime's for an event."""
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["start"].get("date"))

        if start.endswith("Z"):
            start = start[:-1] + "+00:00"
        if end.endswith("Z"):
            end = end[:-1] + "+00:00"

        return (
            datetime.fromisoformat(start),
            datetime.fromisoformat(end),
        )

    def __split_week(self, events: List[dict]) -> List[List[dict]]:
        """Split a week's events into separate lists of days events."""
        days = []
        while events:
            # Start with the first event's start date - we'll then find all events
            # with this date (we rely on events being in the right order).
            date_time = events[0]["start"].date()

            # Find the index of the last event on this day.
            i = 0
            try:
                while events[i]["start"].date() == date_time:
                    i += 1
            except IndexError:
                pass

            # Add this day's events, and remove them from the list.
            days.append(events[:i])
            events = events[i:]

        return days

    def __is_attending(self, user: str, event: dict) -> bool:
        """Establish whether or not a given user is attending a given event."""
        attending = (
            any(
                (
                    attendee.get("email") == user
                    and attendee.get("responseStatus") == "accepted"
                )
                for attendee in event.get("attendees", [])
            )
            or event.get("organizer", {}).get("email") == user
        )
        busy = event.get("transparency", "opaque") == "opaque"
        return attending and busy
