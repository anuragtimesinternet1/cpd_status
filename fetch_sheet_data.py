import smtplib
import requests
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleads import ad_manager
import gspread
import tempfile
import os
import gzip
import pandas as pd
import shutil
import datetime
import pytz
import csv
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleads import errors
import logging
logging.basicConfig(level=logging.DEBUG)
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
SPREADSHEET_ID = '1IlvkuwMIYTYUPiU-UNxnHZwVmqYUqMr2ATOBZEwx9Bk'
RANGE_NAME = 'Sheet1!A:C'  # Adjust range if needed (e.g., A1:C100)
GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')

def fetch_sheet_data(spreadsheet_id, range_name):

    creds_json = json.loads(GOOGLE_CREDENTIALS_JSON)
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
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
