import mysql.connector

db_config = {
    'user': 'Enter your database username here',  # Use your MySQL username
    'password': 'Enter your password here',  # Use the password you set
    'host': '127.0.0.1',
    'database': 'integrity_checker'
}

try:
    conn = mysql.connector.connect(**db_config)
    print("Connection to MySQL successful!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
