from googleads import ad_manager
from fetch_sheet_data import fetch_sheet_data
from process_both_gam import processing_both_gam
from process_both_gam import processing_single_gam
from send_email import send_email
from send_email import send_email_single_gam
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

GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
print("APPLICATION_NAME:", os.getenv('APPLICATION_NAME'))
print("NETWORK_CODE1 :", os.getenv('NETWORK_CODE1'))
print("NETWORK_CODE2 :", os.getenv('NETWORK_CODE2'))
print("CLIENT_ID:", os.getenv('CLIENT_ID'))
print("CLIENT_SECRET:", os.getenv('CLIENT_SECRET'))
print("REFRESH_TOKEN:", os.getenv('REFRESH_TOKEN'))
# Google Sheets setup

SPREADSHEET_ID = '1IlvkuwMIYTYUPiU-UNxnHZwVmqYUqMr2ATOBZEwx9Bk'
RANGE_NAME = 'Sheet1!A:C'  # Adjust range if needed (e.g., A1:C100)

# Load AdManager clients
client1 = ad_manager.AdManagerClient.LoadFromString(f"""
   ad_manager:
    application_name: {os.getenv('APPLICATION_NAME')}
    network_code: {os.getenv('NETWORK_CODE1')}
    client_id: {os.getenv('CLIENT_ID')}
    client_secret: {os.getenv('CLIENT_SECRET')}
    refresh_token: {os.getenv('REFRESH_TOKEN')}
  """)
client2 = ad_manager.AdManagerClient.LoadFromString(f"""
   ad_manager:
    application_name: {os.getenv('APPLICATION_NAME')}
    network_code: {os.getenv('NETWORK_CODE2')}
    client_id: {os.getenv('CLIENT_ID')}
    client_secret: {os.getenv('CLIENT_SECRET')}
    refresh_token: {os.getenv('REFRESH_TOKEN')}
  """)

def parse_commitment(commitment_str):
    try:
        if 'Mn' in commitment_str:
            return float(commitment_str.replace('Mn', '').strip()) * 1_000_000
        else:
            return float(commitment_str.strip())  
    except ValueError:
        return 0  # Return 0 for invalid or missing commitments


if __name__ == "__main__":
        # Fetch the sheet data
    sheet_data = fetch_sheet_data(SPREADSHEET_ID, RANGE_NAME)
    print("Sheet Data:", sheet_data)
# Process each row
    for row_key, row_data in sheet_data.items():
        order_ids = row_data.get('Order ID', '')  # Get the Order ID string
        commitment = row_data.get('Commitment', '')  # Get the Commitment string
    
        commitment_value = parse_commitment(commitment)

        order_ids_list = [order_id.strip() for order_id in order_ids.split(',')] if ',' in order_ids else [order_ids.strip()]
    
        if len(order_ids_list) > 1:  # Check if there are multiple IDs
            result = processing_both_gam(client1, client2, order_ids_list,commitment)
            print(result)
            send_email(result,commitment_value)
        else:
            print(order_ids)
            result=processing_single_gam(client2,order_ids,commitment_value)
            print(result)
            send_email_single_gam(result)
