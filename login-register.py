# CONNECT TO PROGRESSPULSE DATABASE AND LOGIN TO AN ACCOUNT

import mysql.connector
from tkinter import *
from tkinter import messagebox

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
    cursor.execute("SELECT * FROM employees")
    result = cursor.fetchall()
    print(result)

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL database: {e}")
    exit()


# Function for Login (+ Check credentials)
def login(username, password, window):
    # SQL QUERY 
    query = "SELECT COUNT(*) FROM employees WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchall()
    count = result[0][0]
    if result[0][0] == 0:
        messagebox.showerror("Invalid Credentials", "Invalid Username or Password, please try again")
        conn.close()
        window.destroy()
    elif result[0][0] == 1:
        query = "SELECT fname FROM employees WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchall()
        name = result[0][0]
        messagebox.showinfo("Welcome", f"Welcome to ProgressPulse, {name}!")
        conn.close()
        window.destroy() 

# Function to create a new account 
def register(fname, lname, username, password, password2, window):
    if password != password2:
        messagebox.showerror("Error", "Passwords don't match, try again")
        conn.close()
        window.destroy()
    elif len(password) == 0:
        messagebox.showerror("Error", "Password must be at least one (1) character, try again")
        conn.close()
        window.destroy()
    else:
        # SQL QUERY
        query = "INSERT INTO employees VALUES (null, %s, %s, %s, %s)"
        cursor.execute(query, (fname, lname, username, password))
        conn.commit()
        messagebox.showinfo("Success", f"Your account has been created, {fname}!")
        conn.close()
        window.destroy()

# Function to make transition from login to register
def transitionToRegister(event):
    window.geometry("350x420")
    window.title("ProgressPulse Register")


    # Forget the Login Widgets
    widgets_to_forget = [username_label, username_entry, password_label, password_entry, login_button, clickForRegisterLabel, clickForRegister]
    
    for widget in widgets_to_forget:
        widget.forget()

    # Create new widgets for register
    fname_label = Label(window,
                        text="Enter your first name:",
                        padx=10,
                        pady=10,
                        )
    fname_label.pack()
    fname_entry = Entry(window)
    fname_entry.pack()

    lname_label = Label(window,
                        text="Enter your last name:",
                        padx=10,
                        pady=10,
                        )
    lname_label.pack()
    lname_entry = Entry(window)
    lname_entry.pack()

    reg_username_label = Label(window,
                        text="Enter your username:",
                        padx=10,
                        pady=10,
                        )
    reg_username_label.pack()
    reg_username_entry = Entry(window)
    reg_username_entry.pack()

    reg_password_label = Label(window,
                        text="Enter your password:",
                        padx=10,
                        pady=10,
                        )
    reg_password_label.pack()
    reg_password_entry = Entry(window, show="*")
    reg_password_entry.pack()

    reg_password2_label = Label(window,
                        text="reEnter your password:",
                        padx=10,
                        pady=10,
                        )
    reg_password2_label.pack()
    reg_password2_entry = Entry(window, show="*")
    reg_password2_entry.pack()

    # if reg_password2_entry.get() != reg_password_entry.get():
    #     messagebox.errorinfo("Error", "The passwords you have given don't match, try again")
        
    register_button = Button(window,
                    text="Sign Up",
                    border=3,
                    padx=15,
                    pady=5,
                    command=lambda: register(fname_entry.get(), lname_entry.get(), reg_username_entry.get(), reg_password_entry.get(), reg_password2_entry.get(), window)
                    )
    register_button.pack()


window = Tk()
window.geometry("350x300")
window.title("ProgressPulse Login")

# Welcome label
welcome_label = Label(window,
                      text="  Welcome to \n ProgressPulse",
                      font=("Arial", 20, "bold"),
                      fg="#2456ed"
                      )
welcome_label.pack()

# Username Label and Entry
username_label = Label(window,
                        text="Username:",
                        padx=10,
                        pady=10,
                        )
username_label.pack()
username_entry = Entry(window)
username_entry.pack()

# Password Label and Entry
password_label = Label(window,
                        text="Password:")
password_label.pack()
password_entry = Entry(window, show="*")  # Show * for password
password_entry.pack()

# Login button
login_button = Button(window,
                    text="Login",
                    border=3,
                    padx=15,
                    pady=5,
                    command=lambda: login(username_entry.get(), password_entry.get(), window)
                    )
login_button.pack()

# Regiter option label
clickForRegisterLabel = Label(window,
                 text="If you don't have an account \n create one",
                 pady=5)
clickForRegisterLabel.pack()

# "here" button to go for create account
clickForRegister = Label(window,
             text="here",
             fg="blue",
             cursor="hand2",
             )
clickForRegister.pack()
clickForRegister.bind("<Button-1>", transitionToRegister)


window.mainloop()


