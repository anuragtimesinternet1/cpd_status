from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Google Sheets setup
SPREADSHEET_ID = '1IlvkuwMIYTYUPiU-UNxnHZwVmqYUqMr2ATOBZEwx9Bk'
RANGE_NAME = 'Sheet1!A:C'  # Adjust range if needed (e.g., A1:C100)

def fetch_sheet_data(spreadsheet_id, range_name):

    creds = Credentials.from_service_account_file('credentials.json', scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    data_dict = {}
    for idx, row in enumerate(values[1:], start=1): 
        order_id = row[0] if len(row) > 0 else None
        package = row[1] if len(row) > 1 else None
        commitment = row[2] if len(row) > 2 else None
        data_dict[f'Row {idx}'] = {
            'Order ID': order_id,
            'Package': package.replace('\n', ' ') if package else None,  # Replace newlines with spaces
            'Commitment': commitment
        }

    return data_dict

# Example usage
if __name__ == "__main__":
    sheet_data = fetch_sheet_data(SPREADSHEET_ID, RANGE_NAME)
    print(sheet_data)
