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


def hourly_impressions_report_for_order_old_gam(client,order_id):
    order_id = order_id.strip() if isinstance(order_id, str) else order_id
    print("Starting report download for hourly impressions")
    today = datetime.date.today()
    start_date = today
    end_date = today
    report_downloader = client.GetDataDownloader(version='v202502')
    report_job = {
        'reportQuery': {
            'dimensions': ['ORDER_ID', 'ORDER_NAME', 'HOUR'],
            'columns': ['AD_SERVER_IMPRESSIONS'],
            'statement': {
                'query': 'WHERE ORDER_ID = :orderId',
                'values': [{'key': 'orderId', 'value': {'value': order_id, 'xsi_type': 'NumberValue'}}]
            },
            'dateRangeType': 'CUSTOM_DATE',
            'startDate': {'year': start_date.year, 'month': start_date.month, 'day': start_date.day},
            'endDate': {'year': end_date.year, 'month': end_date.month, 'day': end_date.day}
        }
    }

    try:
        report_job_id = report_downloader.WaitForReport(report_job)
        print(f'Report generation successful. Job ID: {report_job_id}')
    except errors.AdManagerReportError as e:
        print(f'Failed to generate report. Error was: {e}')
        return None  

    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    export_format = 'CSV_DUMP'
    report_file_path = f'order_hourly_report_{order_id}_{current_time}.csv.gz'
    csv_file_path = f'order_hourly_report_{order_id}_{current_time}.csv'

    try:
        with open(report_file_path, 'wb') as report_file:
            report_downloader.DownloadReportToFile(report_job_id, export_format, report_file)
        with gzip.open(report_file_path, 'rb') as f_in:
            with open(csv_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        print(f'Hourly impressions report downloaded to:\n{csv_file_path}')
        return csv_file_path
    except Exception as e:
        print(f'Failed to download or process report. Error was: {e}')
        return None
    finally:
        if os.path.exists(report_file_path):
            os.remove(report_file_path)

def total_impressions(csv_file_path):
    try:
        column_d_values = []
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if len(row) >= 4:  # Ensure there is a 4th column.
                    try:
                        value = float(row[3])  # Column D is at index 3 (0-based).
                        column_d_values.append(value)
                    except ValueError:
                        continue  # Skip rows where the value cannot be converted to float.

        # If the list is empty or has only one value, return 0 (nothing to sum).
        if len(column_d_values) <= 1:
            print("Not enough data points to calculate the total impressions.")
            return 0

        # Exclude the last value in column D and calculate the sum of the remaining values.
        total = sum(column_d_values[:-1])  # Exclude the last value using slicing.

        return total

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

def calculate_average_of_column_d(csv_file_path):
    try:
        # Read the CSV file and collect the values in column D (4th column).
        column_d_values = []
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row.
            next(reader)
            for row in reader:
                if len(row) >= 4:  # Ensure there is a 4th column.
                    try:
                        value = float(row[3])  # Column D is at index 3 (0-based).
                        column_d_values.append(value)
                    except ValueError:
                        continue  # Skip rows where the value cannot be converted to float.

        # Check if we have enough data points to extract the second-to-last to eighth-to-last values.
        # print(column_d_values)
        if len(column_d_values) < 2:
            print("Not enough data points to calculate the average for the specified range.")
            return None

        # Get the range from the second-to-last value to the eighth-to-last value.
        range_to_average = column_d_values[-2:-1]  # Python slicing gets from the 8th last to the second last.
        print(range_to_average)
        

        # Calculate the average of the selected range.
        average = sum(range_to_average) / len(range_to_average)

        # Round to the nearest integer and return.
        rounded_average = round(average)
        return rounded_average

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
