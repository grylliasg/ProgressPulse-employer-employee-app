import mysql.connector

# Initialize global variables
conn = None
cursor = None

def connectToDatabase():
    global conn
    global cursor
    # Create the connection
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="progresspulse",
            port='3307'
        )
        # If the connection is successful, print a success message
        print("Connected to MySQL database successfully.")
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        exit()

def get_connection():
    global conn
    if conn is None:
        connectToDatabase()
    return conn

def get_cursor():
    global cursor
    if cursor is None:
        connectToDatabase()
    return cursor
