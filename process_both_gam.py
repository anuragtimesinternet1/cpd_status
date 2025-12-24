from googleads  import ad_manager
from old_gam_report import hourly_impressions_report_for_order_old_gam
from old_gam_report import calculate_average_of_column_d
from old_gam_report import total_impressions
from datetime import datetime
import csv
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

def get_order_name(client,order_id ):
    """Fetch the name of the order for a given order_id."""
    # Initialize the OrderService
    order_service = client.GetService('OrderService')

    # Create a statement to filter the order by its ID
    statement = ad_manager.StatementBuilder().Where('id = :order_id').WithBindVariable('order_id', order_id)

    # Get the orders matching the statement
    response = order_service.getOrdersByStatement(statement.ToStatement())

    if 'results' in response:
        # If results exist, return the name of the first order
        order = response['results'][0]
        return order['name']
    else:
        print(f'No order found for order_id: {order_id}')
        return None
    
def hour_left(csv_file_path):
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            rows = list(csv_reader)  # Convert all rows to a list
            # Iterate through all rows except the last one
            for row in rows[:-1]:
                hour = int(row['Dimension.HOUR'])
        remaining_hour=23-hour
        print(f'hour left for campaign{remaining_hour}')
        return remaining_hour
    except Exception as e:
        print(f'Failed to read CSV or calculate total impressions. Error was: {e}')

        
def processing_both_gam(client1, client2, order_ids,commitment_value):
    result = {}
    try:
        # Process the old GAM
        order_name=get_order_name(client1,order_ids[0])
        old_csv_file_path = hourly_impressions_report_for_order_old_gam(client1, order_ids[0])
        if old_csv_file_path:
            average_value_old_gam = calculate_average_of_column_d(old_csv_file_path)
            total_imps_old_gam = total_impressions(old_csv_file_path)
        else:
            average_value_old_gam = 0
            total_imps_old_gam = 0

        # Process the new GAM
        new_csv_file_path = hourly_impressions_report_for_order_old_gam(client2, order_ids[1])
        if new_csv_file_path:
            average_value_new_gam = calculate_average_of_column_d(new_csv_file_path)
            total_imps_new_gam = total_impressions(new_csv_file_path)
        else:
            average_value_new_gam = 0
            total_imps_new_gam = 0

        # Calculate expected delivery
        remaining_hour_left = hour_left(old_csv_file_path)
        expected_delivery_old_gam = total_imps_old_gam + remaining_hour_left * average_value_old_gam
        expected_delivery_new_gam = total_imps_new_gam + remaining_hour_left * average_value_new_gam

        # Populate the result dictionary
        result = {
            'Order Name':order_name,
            'Hour Left':remaining_hour_left,
            "Current impressions(Old Gam)": int(total_imps_old_gam),
            "Hourly Average(Old Gam)": int(average_value_old_gam),
            "Current impressions(New Gam)": int(total_imps_new_gam),
            "Hourly Average(New Gam)": int(average_value_new_gam),
            "Total Current impressions": int(total_imps_old_gam + total_imps_new_gam),
            "Total Expected Impresions": int(expected_delivery_old_gam + expected_delivery_new_gam),
            "Commitment": commitment_value,
        }

    except Exception as e:
        result["error"] = f"An error occurred: {e}"

    return result

def processing_single_gam(client1,order_ids,commitment_value):
    result = {}
    print(order_ids)
    try:
        # Process the old GAM
        order_name=get_order_name(client1,order_ids)
        old_csv_file_path = hourly_impressions_report_for_order_old_gam(client1, order_ids)
        if old_csv_file_path:
            average_value_old_gam = calculate_average_of_column_d(old_csv_file_path)
            total_imps_old_gam = total_impressions(old_csv_file_path)
        else:
            average_value_old_gam = 0
            total_imps_old_gam = 0

        # Calculate expected delivery
        remaining_hour_left = hour_left(old_csv_file_path)
        expected_delivery_old_gam = total_imps_old_gam + remaining_hour_left * average_value_old_gam
        # Populate the result dictionary
        result = {
            'Order Name':order_name,
            'Hour Left':remaining_hour_left,
            "Current impressions ": int(total_imps_old_gam),
            "Hourly Average": int(average_value_old_gam),
            "Total Expected Impresions": int(expected_delivery_old_gam),
            "Commitment": commitment_value,
        }

    except Exception as e:
        result["error"] = f"An error occurred: {e}"

    return result
