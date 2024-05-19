import mysql.connector

def connectToDatabase():
    global conn
    global cursor
    global result
    # Create the connection
    try:
        # Connect to MySQL database on port 3307
        conn = mysql.connector.connect(
            host="localhost",
            port="3307",  
            user="root",
            password="",
            database="progresspulse"
        )
        # If the connection is successful, print a success message
        print("Connected to MySQL database successfully.")
        cursor = conn.cursor()
        

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        exit()