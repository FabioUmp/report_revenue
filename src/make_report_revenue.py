import csv

def process_csv(file_path):
    channels_data = {}
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            sub_id1 = row['Sub Id 1']
            sub_id2 = row['Sub Id 2']
            sub_id3 = row['Sub Id 3']
            event_type = row['Event Type']
            status = row['Status']
            action_earnings = float(row['Action Earnings'])
            
            channel_key = (sub_id1, sub_id2, sub_id3)
            if channel_key not in channels_data:
                channels_data[channel_key] = {
                    'Current Revenue': 0.0,
                    'Free Trial Revenue Forecast': 0.0,
                    'Paid Trial Revenue Forecast': 0.0
                }
            
            channels_data[channel_key]['Current Revenue'] += action_earnings
            
            if event_type == 'Free Trial API' and status != 'Pending':
                channels_data[channel_key]['Free Trial Revenue Forecast'] += action_earnings
            elif event_type == 'Paid Trial API' and status != 'Pending':
                channels_data[channel_key]['Paid Trial Revenue Forecast'] += action_earnings
    
    return channels_data

def write_csv(output_file, channels_data):
    fieldnames = ['Channel', 'Current Revenue', 'Free Trial Revenue Forecast', 'Paid Trial Revenue Forecast']
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for channel_key, data in channels_data.items():
            sub_id1, sub_id2, sub_id3 = channel_key
            current_revenue = data['Current Revenue']
            free_trial_forecast = data['Free Trial Revenue Forecast']
            paid_trial_forecast = data['Paid Trial Revenue Forecast']
            
            writer.writerow({
                'Channel': f"{sub_id1}_{sub_id2}_{sub_id3}",
                'Current Revenue': current_revenue,
                'Free Trial Revenue Forecast': free_trial_forecast,
                'Paid Trial Revenue Forecast': paid_trial_forecast
            })

file_path = '/home/umpierre/Downloads/impact-report.csv'
output_file = '/home/umpierre/Downloads/processed-report.csv'

channels_data = process_csv(file_path)
write_csv(output_file, channels_data)

print(f"New CSV file '{output_file}' has been created.")
