import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print("Connected to server.")
        
        self.username = None

        self.gui_done = False
        self.running = True

        login_thread = threading.Thread(target=self.login)
        login_thread.start()

    def login(self):
        self.login_win = tkinter.Tk()
        self.login_win.title("Login")
        self.login_win.configure(bg="lightgray")

        self.username_label = tkinter.Label(self.login_win, text="Username:", bg="lightgray")
        self.username_label.grid(row=0, column=0, padx=20, pady=5)
        self.username_entry = tkinter.Entry(self.login_win)
        self.username_entry.grid(row=0, column=1, padx=20, pady=5)

        self.password_label = tkinter.Label(self.login_win, text="Password:", bg="lightgray")
        self.password_label.grid(row=1, column=0, padx=20, pady=5)
        self.password_entry = tkinter.Entry(self.login_win, show="*")
        self.password_entry.grid(row=1, column=1, padx=20, pady=5)

        self.login_button = tkinter.Button(self.login_win, text="Login", command=self.perform_login)
        self.login_button.grid(row=2, columnspan=2, padx=20, pady=5)

        self.login_win.mainloop()

    def perform_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        self.sock.send(username.encode('utf-8'))
        self.sock.send(password.encode('utf-8'))
        response = self.sock.recv(1024).decode('utf-8')
        print(f"Received response: {response}")
        if response == 'SUCCESS':
            self.username = username
            self.login_win.destroy()
            self.gui_loop()
        else:
            print("Invalid username or password. Please try again.")
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.win.title(f"Chat - {self.username}")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        self.win.mainloop()
        print("GUI loop ended.")

    def write(self):
        message = self.input_area.get('1.0', 'end').strip()
        if message:
            self.sock.send(f"{self.username}: {message}".encode('utf-8'))
            self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if self.gui_done:
                    self.text_area.config(state='normal')
                    self.text_area.insert('end', message + '\n')
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(HOST, PORT)

