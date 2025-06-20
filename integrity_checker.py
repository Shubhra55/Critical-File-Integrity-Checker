import os
import hashlib
import mysql.connector
import pandas as pd
from win10toast import ToastNotifier
from datetime import datetime

# Configure database connection
db_config = {
    'user': 'root',
    'password': 'Neminath@22',  # Use the new password you set
    'host': '127.0.0.1',
    'database': 'integrity_checker'
}

# Test database connection
def test_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        print("Database connection successful!")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

test_db_connection()

# Function to calculate file hash
def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
    except PermissionError as e:
        print(f"PermissionError: {e} - Skipping file: {file_path}")
        return None
    except Exception as e:
        print(f"Error: {e} - Skipping file: {file_path}")
        return None
    return hasher.hexdigest()

# Function to store initial file hashes
def store_initial_hashes(directory):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_file_hash(file_path)
                if file_hash is not None:  # Only store hashes of files we could read
                    cursor.execute('REPLACE INTO file_hashes (file_path, hash_value, scan_time) VALUES (%s, %s, %s)', (file_path, file_hash, scan_time))
        conn.commit()
        conn.close()
        print("Initial hashes stored successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to scan files and compare hashes
def scan_files_and_compare(directory):
    discrepancies = []
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                current_hash = calculate_file_hash(file_path)
                if current_hash is not None:
                    cursor.execute('SELECT hash_value FROM file_hashes WHERE file_path = %s', (file_path,))
                    result = cursor.fetchone()
                    if result and result[0] != current_hash:
                        discrepancies.append(file_path)
                    cursor.execute('UPDATE file_hashes SET hash_value = %s, scan_time = %s WHERE file_path = %s', (current_hash, scan_time, file_path))
                else:
                    cursor.execute('UPDATE file_hashes SET scan_time = %s WHERE file_path = %s', (scan_time, file_path))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return discrepancies

# Function to send desktop notifications
def send_desktop_notification(discrepancies):
    toaster = ToastNotifier()
    notification_message = "The following files have been modified:\n" + '\n'.join(discrepancies)
    toaster.show_toast("Integrity Checker Alert", notification_message, duration=10, icon_path=None)

# Function to export MySQL records to Excel
def export_to_excel():
    try:
        conn = mysql.connector.connect(**db_config)
        query = "SELECT * FROM file_hashes"
        df = pd.read_sql(query, conn)
        print("Data fetched from MySQL:", df.head())  # Debugging: Print the first few rows of the DataFrame
        # Specify the output path for the Excel file
        output_path = r'E:\Projects\INTEGRITY_CHECKER\file_hashes.xlsx'  
        print(f"Attempting to save the file to: {output_path}")
        df.to_excel(output_path, index=False)  # Save as Excel file
        conn.close()
        print("Records exported to file_hashes.xlsx successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to schedule scans at regular intervals
def schedule_scan():
    import time
    while True:
        discrepancies = scan_files_and_compare(r'C:\Windows\System32')
        if discrepancies:
            send_desktop_notification(discrepancies)
        export_to_excel()  # Export records to Excel after each scan
        time.sleep(3600)  # Scan every hour

# Initial setup: Store initial file hashes (run once)
# Uncomment this line for the initial setup
store_initial_hashes(r'C:\Windows\System32')

# Schedule scans
schedule_scan()
