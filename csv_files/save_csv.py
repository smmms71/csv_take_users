import csv
from datetime import datetime

# Function to write data to a CSV file
def save_to_csv(data_list, msg_user_name, filename='csv_files/data.csv'):
    # Define the header of the CSV file
    headers = ['type','name','email', 'user_id', 'img_link', 'time']
    
    data_list = [{'type': data_list.service_type,'name': msg_user_name, 'email': data_list.mail_name, 'user_id': data_list.id, 'img_link': data_list.files_link,'time':data_list.date}]
    # Open the CSV file for writing
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(headers)
        
        # Write each row of data
        for data in data_list:
            writer.writerow([
                data.get('type', ''),
                data.get('name', ''),
                data.get('email', ''),
                data.get('user_id', ''),
                data.get('img_link', ''),
                data.get('time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # Formatting time as a string
            ])

# # Example usage:
# # Ensure you replace below example_data with your actual list of data dictionaries
# example_data = [
#     {'name': 'Alice', 'email': 'alice@example.com', 'user_id': '1', 'img_link': 'http://image.link/alice.png'},
#     {'name': 'Bob', 'email': 'bob@example.com', 'user_id': '2', 'img_link': 'http://image.link/bob.png'},
#     # ... add more dictionary entries as needed
# ]

# save_to_csv(example_data)


