from googleapiclient.discovery import build
from langchain.tools import Tool
from datetime import datetime, timedelta
import pytz

from ..config.authenticate_google_calendar import authenticate_google_calendar

# Authenticate and build the Google Calendar service
creds = authenticate_google_calendar()
service = build('calendar', 'v3', credentials=creds)

def create_calendar_event(summary: str, start_datetime_str: str, end_datetime_str: str, attendees: str = None, description: str = None) -> str:
    """
    Creates a new event on the Google Calendar.
    Args:
        summary (str): The title of the event.
        start_datetime_str (str): The start date and time of the event in ISO format (e.g., "2023-10-27T10:00:00-03:00").
        end_datetime_str (str): The end date and time of the event in ISO format (e.g., "2023-10-27T11:00:00-03:00").
        attendees (str, optional): Comma-separated email addresses of attendees. Defaults to None.
        description (str, optional): A description for the event. Defaults to None.
    Returns:
        str: A confirmation message with the event details or an error message.
    """
    if not start_datetime_str or not end_datetime_str:
        return "Error: Both start_datetime_str and end_datetime_str are required to create an event."

    try:
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_datetime_str,
                'timeZone': 'America/Sao_Paulo', # Assuming default timezone for Brazil
            },
            'end': {
                'dateTime': end_datetime_str,
                'timeZone': 'America/Sao_Paulo', # Assuming default timezone for Brazil
            },
        }
        if attendees:
            event['attendees'] = [{'email': email.strip()} for email in attendees.split(',')]

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f'Event created: {event.get("htmlLink")}'
    except Exception as e:
        return f"Error creating event: {e}"

def list_upcoming_events(max_results: int = 10) -> str:
    """
    Lists upcoming events from the Google Calendar.
    Args:
        max_results (int, optional): The maximum number of events to retrieve. Defaults to 10.
    Returns:
        str: A formatted string of upcoming events or a message indicating no events.
    """
    try:
        # Ensure max_results is an integer, handling potential string input from LLM
        if isinstance(max_results, str):
            try:
                max_results = int(max_results)
            except ValueError:
                return "Error: max_results must be an integer."

        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=max_results, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return 'No upcoming events found.'
        
        events_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            events_list.append(f"{start} - {event['summary']}")
        return "\n".join(events_list)
    except Exception as e:
        return f"Error listing events: {e}"

google_calendar_create_event_tool = Tool(
    name="create_calendar_event",
    func=create_calendar_event,
    description="""
    Creates a new event on the Google Calendar.
    Input should be a comma-separated string of arguments. All arguments are required unless specified as optional:
    summary (str): The title of the event.
    start_datetime_str (str): The start date and time of the event in ISO format (e.g., "2023-10-27T10:00:00-03:00").
    end_datetime_str (str): The end date and time of the event in ISO format (e.g., "2023-10-27T11:00:00-03:00").
    attendees (str, optional): Comma-separated email addresses of attendees. Defaults to None.
    description (str, optional): A description for the event. Defaults to None.
    Example: "Meeting with John, 2023-10-27T10:00:00-03:00, 2023-10-27T11:00:00-03:00, john@example.com, Discuss project progress"
    """
)

google_calendar_list_upcoming_events_tool = Tool(
    name="list_upcoming_events",
    func=list_upcoming_events,
    description="""
    Lists upcoming events from the Google Calendar.
    Input is optional and should be an integer representing the maximum number of events to retrieve. 
    If provided, the input must be a plain integer (e.g., 5), not a string like '5'. If no input, defaults to 10.
    """
)

google_calendar_list_upcoming_events_tool = Tool(
    name="list_upcoming_events",
    func=list_upcoming_events,
    description="""
    Lists upcoming events from the Google Calendar.
    Input is optional and should be an integer representing the maximum number of events to retrieve. 
    If provided, the input must be a plain integer (e.g., 5), not a string like '5'. If no input, defaults to 10.
    """
)

# List of all tools
google_calendar_tools = [google_calendar_create_event_tool, google_calendar_list_upcoming_events_tool]
