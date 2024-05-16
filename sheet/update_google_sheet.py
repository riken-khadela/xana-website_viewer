from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import gspread, os

# Define the scope of the Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_google_sheets():
    creds = None

    # Load existing credentials from the credentials.json file if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Create a Google Sheets client
    client = gspread.authorize(creds)

    return client

def read_google_sheet(sheet_id, sheet_name):
    # Authenticate with Google Sheets
    client = authenticate_google_sheets()

    # Open the Google Sheet by its ID
    sheet = client.open_by_key(sheet_id)

    # Get a specific worksheet by its name
    worksheet = sheet.worksheet(sheet_name)

    # Read data from the worksheet
    data = worksheet.get_all_records()

    return data

# Example usage
if __name__ == "__main__":
    sheet_id = 'YOUR_SHEET_ID'
    sheet_name = 'YOUR_SHEET_NAME'
    sheet_data = read_google_sheet(sheet_id, sheet_name)
    print(sheet_data)
