# CONNECT TO PROGRESSPULSE DATABASE AND LOGIN TO AN ACCOUNT
from tkinter import *
from tkinter import messagebox
from user import *
import connect


# Function for Login (+ Check credentials)
def login(username, password, window):
    # SQL QUERY 
    query = "SELECT * FROM employee WHERE username = %s AND password = %s"
    connect.cursor.execute(query, (username, password))
    result = connect.cursor.fetchall()
    if result:
        globals()[username] = Employee(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7], result[0][8])
        employeeInterface(globals()[username])
    else:
        messagebox.showerror("Invalid Credentials", "Invalid Username or Password, please try again")
        window.destroy()
        createWindow()

def employeeInterface(fname):
    global if1

    if1 = Tk()
    if1.geometry('700x650')
    if1.title('User Interface')
    logout = Button(if1,
                    text='Logout',
                    font=('Arial', 10),
                    fg='white',
                    bg='red',
                    cursor='hand2',
                    command= lambda: (if1.destroy(), createWindow())
                    )
    logout.pack(side=RIGHT, anchor=NE)

    welcome = Label(if1, text=f'Welcome, {fname.name}', font=('Arial', 15), border=3)
    welcome.place(x=0, y=0)

    # TASKS
    task_label = Label(if1, text='my Tasks', font=('Arial', 18))
    task_label.place(x=48, y=90)
    main_taskframe = Frame(if1, bg="lightgrey", bd=4)
    main_taskframe.place(x=40, y=130)

    assignedTasks = fname.getAssignedTasks() 
    if all(globals()[assignedTasks].completed == 1 for assignedTask in assignedTasks) or len(assignedTasks) == 0:
        notasks = Label(main_taskframe, text='You have not active tasks')
        notasks.pack()
    for assignedTask in assignedTasks:
        if assignedTask.completed != 1:
            task = Button(main_taskframe, text=assignedTask.title, height=5, width=15, cursor='hand2',  command= lambda assignedTask=assignedTask: fname.view_assigned_task(assignedTask))  # Adjust height and width as needed
            task.pack()


    # MEETINGS
    meet_label = Label(if1, text='my Meetings', font=('Arial', 18))
    meet_label.place(x=218, y=90)
    meetframe = Frame(if1, bg="lightgrey", bd=4)
    meetframe.place(x=230, y=130)

    meetings = fname.getMeetings()  
    if len(meetings) == 0:
        nomeets = Label(meetframe, text='You have not active meetings')
        nomeets.pack()
    for meeting in meetings:
        task = Button(meetframe, text=meeting.meetingName, height=5, width=15, cursor='hand2', command= lambda meeting=meeting:fname.view_meeting_schedule(meeting))  # Adjust height and width as needed
        task.pack()

    # CHAT
    chatLabel = Label(if1, text='Chat:', font=('Arial', 18))
    chatLabel.place(x=490, y=90)
    chat = Text(if1, height=20, width=30)
    chat.place(x=390, y=130)

    # Completed Tasks
    comTasks = Button(if1, text='Show Completed Tasks', fg='white', bg='green', cursor='hand2', command= fname.show_completed_tasks)
    comTasks.place(x=5, y=530)


    if1.mainloop()


# Function to create a new account 
def register(fname, lname, username, password, password2, window):
    if password != password2:
        messagebox.showerror("Error", "Passwords don't match, try again")
        forgetRegisterWidgets()
        registerWidgets(Event)
    elif len(password) == 0:
        messagebox.showerror("Error", "Password must be at least one (1) character, try again")
        forgetRegisterWidgets()
        registerWidgets(Event)
    else:
        # SQL QUERY
        query = "INSERT INTO employee VALUES (%s, null, %s, %s, %s, %s, %s, %s, %s)"
        connect.cursor.execute(query, (f'{fname} {lname}', username, password, '', '', '', '', ''))
        connect.conn.commit()
        messagebox.showinfo("Success", f"Your account has been created, {fname}!")
        forgetRegisterWidgets()
        createWindow()

def forgetRegisterWidgets():
    widgets_to_forget = [
                        fname_label,
                        fname_entry,
                        lname_label,
                        lname_entry,
                        reg_username_label,
                        reg_username_entry,
                        reg_password_label,
                        reg_password_entry,
                        reg_password2_label,
                        reg_password2_entry,
                        register_button,
                        ]
    
    for widget in widgets_to_forget:
        widget.forget()


# Function to make transition from login to register
def forgetLoginWidgets():
    # Forget the Login Widgets
    widgets_to_forget = [username_label, 
                         username_entry, 
                         password_label,
                         password_entry, 
                         login_button, 
                         clickForRegisterLabel, 
                         clickForRegister,
                         ]
    
    for widget in widgets_to_forget:
        widget.forget()

def registerWidgets(event):
    global fname_label
    global fname_entry
    global lname_label
    global lname_entry
    global reg_username_label
    global reg_username_entry
    global reg_password_label
    global reg_password_entry
    global reg_password2_label
    global reg_password2_entry
    global register_button

    if username_label:
        forgetLoginWidgets()
    # Create new widgets for register
    window.geometry("350x420")
    window.title("ProgressPulse Register")

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

    register_button = Button(window,
                         text="Sign Up",
                         border=3,
                         padx=15,
                         pady=5,
                         command=lambda: register(fname_entry.get(), lname_entry.get(), reg_username_entry.get(), reg_password_entry.get(), reg_password2_entry.get(), window)
                         )
    register_button.pack()




def createWindow():
    global window
    global welcome_label
    global username_label
    global username_entry
    global password_label
    global password_entry
    global login_button
    global clickForRegisterLabel
    global clickForRegister

    
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
                        cursor='hand2',
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
    clickForRegister.bind("<Button-1>", registerWidgets)


    window.mainloop()

# RUN window function to start the program ...
if __name__ == "__main__":
    connect.connectToDatabase()
    createWindow()



