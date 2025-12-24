from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os


def convert_to_million(number):
    try:
        million_value = number / 1_000_000
        return f"{million_value:.2f} Mn"  
    except (ValueError, TypeError):
        return "Invalid input"

import smtplib


def send_email(result, commitment_value):

    order_name = result['Order Name']
    expected_impressions = result['Total Expected Impresions']
    tenpercent_of_impressions=0.1*int(commitment_value)+commitment_value

    if expected_impressions>tenpercent_of_impressions:
        over_delivery=expected_impressions-commitment_value
        over_delivery_in_million=convert_to_million(over_delivery)
        campaign_status=f'Over Delivery by {over_delivery_in_million}'
        status_color = 'orange'
    elif expected_impressions > commitment_value:
        campaign_status = 'On Track'
        status_color = 'green'
    elif expected_impressions == commitment_value:
        campaign_status = 'On Track'
        status_color = 'green'
    else:
        under_delivery = commitment_value - expected_impressions
        under_delivery_in_million=convert_to_million(under_delivery)
        campaign_status = f'Under Delivery by {under_delivery_in_million}'
        status_color = 'red'

    expected_impressions_in_million = convert_to_million(expected_impressions)

    subject = f"Status of Campaign: {order_name}"

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }}
            h2 {{
                color: #333;
                text-align: center;
                padding: 20px;
                background-color: #4CAF50;
                color: white;
                margin: 0;
            }}
            .table-container {{
                overflow-x: auto;
                margin: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
                color: #333;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
            td {{
                font-size: 14px;
            }}
            .header {{
                font-weight: bold;
                color: #333;
            }}
            .status {{
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                padding: 20px;
                background-color: {status_color};
                color: white;
            }}
            .note {{
                font-size: 14px;
                color: #555;
                text-align: center;
                margin-top: 10px;
                padding: 10px;
                line-height: 1.5;
            }}
        </style>
    </head>
    <body>
        <div class="table-container">
            <table>
                <tr>
                    <th class="header">Order Name</th>
                    <th class="header">Commitment</th>
                    <th class="header">Current Impressions (Old Gam)</th>
                    <th class="header">Current Impressions (New Gam)</th>
                    <th class="header">Total Current Impressions</th>
                    <th class="header">Total Expected Delivery</th>
                </tr>
                <tr>
                    <td>{result['Order Name']}</td>
                    <td>{result['Commitment']}</td>
                    <td>{result['Current impressions(Old Gam)']}</td>
                    <td>{result['Current impressions(New Gam)']}</td>
                    <td>{result['Total Current impressions']}</td>
                    <td>{expected_impressions_in_million}</td>
                </tr>
            </table>
        </div>
        
        <!-- Display campaign status below the table -->
        <div class="status">
            Campaign Status: {campaign_status}
        </div>
        
        <!-- Add a short note about campaign status -->
        <div class="note">
            <p>
                <strong>Note:</strong> The status of the campaign is determined based on the current traffic 
                and performance metrics of the campaign.
            </p>
        </div>
    </body>
    </html>
    """

    sender_email = "anurag.mishra1@timesinternet.in"
    recipient_emails = ["anurag.mishra1@timesinternet.in","colombia.opsqc@timesinternet.in","teamaddelivery@timesinternet.in","customersuccess@timesinternet.in","sagar@timesinternet.in","mdanish.muinuddin@timesinternet.in"]

    msg = MIMEMultipart('alternative')
    msg['From'] = f'AdTech Quality <{sender_email}>'
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = subject

    # Attach the HTML body
    msg.attach(MIMEText(html, 'html'))
    EMAIL_PASSWORD='mswo jphq fmcl djlo'
    try:
        # Set up the server (using Gmail SMTP)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, EMAIL_PASSWORD)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
        print(f"Email sent successfully for Order Name {order_name}")
    except Exception as e:
        print(f"Failed to send email for Order Name {order_name}. Error: {e}")


def send_email_single_gam(result):

    order_name = result['Order Name']
    hour_left = result['Hour Left']
    current_impressions = result['Current impressions ']
    hourly_average = result['Hourly Average']
    total_expected_impressions = result['Total Expected Impresions']
    commitment = result['Commitment']


    if total_expected_impressions > commitment:
        campaign_status = 'On Track'
        status_color = 'green'
    elif total_expected_impressions == commitment:
        campaign_status = 'On Track'
        status_color = 'green'
    else:
        under_delivery = commitment - total_expected_impressions
        under_delivery_in_million=convert_to_million(under_delivery)
        
        campaign_status = f'Under Delivery by {under_delivery_in_million}'
        status_color = 'red'

 
    current_impressions_in_million = convert_to_million(current_impressions)
    total_expected_impressions_in_million = convert_to_million(total_expected_impressions)
    commitment_in_million = convert_to_million(commitment)


    subject = f"Status of Campaign: {order_name}"


    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
            }}
            h2 {{
                color: white;
                text-align: center;
                padding: 10px;
                background-color: #4CAF50;
                margin: 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px auto;
                font-size: 14px;
                border: 1px solid #ddd;
            }}
            th, td {{
                text-align: left;
                padding: 12px;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
                color: #333;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .status {{
                text-align: center;
                padding: 15px;
                background-color: {status_color};
                color: white;
                font-weight: bold;
                font-size: 16px;
            }}
            .note {{
                text-align: center;
                font-size: 14px;
                color: #555;
                margin-top: 10px;
                padding: 10px;
            }}
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>Order Name</th>
                <th>Commitment </th>
                <th>Current Impressions </th>
                <th>Hourly Average</th>
                <th>Hours Left</th>
                <th>Total Expected Delivery </th>
            </tr>
            <tr>
                <td>{order_name}</td>
                <td>{commitment_in_million}</td>
                <td>{current_impressions_in_million}</td>
                <td>{hourly_average:,}</td>
                <td>{hour_left}</td>
                <td>{total_expected_impressions_in_million}</td>
            </tr>
        </table>
        <div class="status">
            Campaign Status: {campaign_status}
        </div>
        <div class="note">
            <strong>Note:</strong> The campaign status is evaluated based on the commitment value, current performance, and expected impressions.
        </div>
    </body>
    </html>
    """

    # Email credentials
    EMAIL_PASSWORD = "mswo jphq fmcl djlo"  # Replace with your app-specific password
    sender_email = "anurag.mishra1@timesinternet.in"
    recipient_emails = ["anurag.mishra1@timesinternet.in","colombia.opsqc@timesinternet.in","teamaddelivery@timesinternet.in","customersuccess@timesinternet.in","sagar@timesinternet.in","mdanish.muinuddin@timesinternet.in"]

    msg = MIMEMultipart('alternative')
    msg['From'] = f'AdTech Quality <{sender_email}>'
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = subject

    # Attach the HTML body
    msg.attach(MIMEText(html, 'html'))

    try:
        # Set up the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, EMAIL_PASSWORD)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
        print(f"Email sent successfully for Order Name {order_name}")
    except Exception as e:
        print(f"Failed to send email for Order Name {order_name}. Error: {e}")

