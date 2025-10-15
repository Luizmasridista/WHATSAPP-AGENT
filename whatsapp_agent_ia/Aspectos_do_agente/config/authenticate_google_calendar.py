import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_google_calendar():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # The credentials.json file should be downloaded from Google Cloud Console
            # and placed in the same directory as this script.
            flow = InstalledAppFlow.from_client_secrets_file(
                'Aspectos_do_agente/config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

if __name__ == '__main__':
    print("Running Google Calendar authentication flow...")
    print("Please ensure you have 'credentials.json' in the same directory.")
    authenticate_google_calendar()
    print("Authentication successful! 'token.json' has been created.")
    print("You can now proceed to define the Google Calendar tool for the agent.")
