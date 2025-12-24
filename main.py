from googleads import ad_manager
from fetch_sheet_data import fetch_sheet_data
from process_both_gam import processing_both_gam
from process_both_gam import processing_single_gam
from send_email import send_email
from send_email import send_email_single_gam

# Google Sheets setup
SPREADSHEET_ID = '1IlvkuwMIYTYUPiU-UNxnHZwVmqYUqMr2ATOBZEwx9Bk'
RANGE_NAME = 'Sheet1!A:C'  

client1 = ad_manager.AdManagerClient.LoadFromStorage('googleads.yaml')
client2 = ad_manager.AdManagerClient.LoadFromStorage('googleads1.yaml')

def parse_commitment(commitment_str):
    try:
        if 'Mn' in commitment_str:
            return float(commitment_str.replace('Mn', '').strip()) * 1_000_000
        else:
            return float(commitment_str.strip())  
    except ValueError:
        return 0  


if __name__ == "__main__":
        # Fetch the sheet data
    sheet_data = fetch_sheet_data(SPREADSHEET_ID, RANGE_NAME)
    print("Sheet Data:", sheet_data)
# Process each row
    for row_key, row_data in sheet_data.items():
        order_ids = row_data.get('Order ID', '')  # Get the Order ID string
        commitment = row_data.get('Commitment', '')  
    
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


