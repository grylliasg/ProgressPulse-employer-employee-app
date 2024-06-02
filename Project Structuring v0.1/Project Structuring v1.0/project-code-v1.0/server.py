import socket
import threading
import mysql.connector

# Ρυθμίσεις server
HOST = '127.0.0.1'
PORT = 9090

# Σύνδεση στη βάση δεδομένων
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="iwanna",
    database="progresspusle_db"
)

cursor = db.cursor()

# Ρυθμίσεις socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Λίστα με τους συνδεδεμένους clients και τα usernames τους
clients = []
usernames = []

# Αποστολή μηνύματος σε όλους τους clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Συνάρτηση για τη χειριστή των συνδέσεων των clients
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"{usernames[clients.index(client)]} says {message}")
                broadcast(message.encode('utf-8'))
        except:
            # Αν υπάρξει κάποιο σφάλμα, κλείνει τη σύνδεση με τον client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} left the chat!'.encode('utf-8'))
            usernames.remove(username)
            break

# Αποδοχή νέων συνδέσεων
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Διαδικασία σύνδεσης χρήστη
        username = client.recv(1024).decode('utf-8')
        password = client.recv(1024).decode('utf-8')

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()

        if result:
            client.send("SUCCESS".encode('utf-8'))
            usernames.append(username)
            clients.append(client)
            print(f"Username of the client is {username}")
            broadcast(f"{username} connected to the server!\n".encode('utf-8'))
            client.send("Connected to the server".encode('utf-8'))

            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        else:
            client.send("ERROR".encode('utf-8'))
            client.close()

print("Server is running...")
receive()
