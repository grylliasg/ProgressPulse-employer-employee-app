from tkinter import *
import tkinter as tk
from tkinter import Label, Button, Frame, Text,messagebox, PhotoImage
from employee import *
import connect
from employer import *
from employerinterface import *
from meetings import Meeting
from leaves import Leave
from tasks import Task 



# Function for Login (+ Check credentials)
def login(username, password, window):
    #EMPLOYEE __init__(self, name, id, username, password, role, assignedTasks, meetingSchedule, leaveRequests):
    global histeam
    global userID
    query = "SELECT name, UserID, Username, Password, UserRole FROM users WHERE Username = %s AND Password = %s"
    connect.cursor.execute(query, (username, password))
    result = connect.cursor.fetchall()
    # VRES SE POIA OMADA ANHKEI AUTOS O EMPLOYEE
    
    if result != []:
        userID = result[0][1]
        userRole = result[0][4]

        quer = "SELECT Team FROM users WHERE UserID = %s"
        connect.cursor.execute(quer, (userID, ))
        resul = connect.cursor.fetchall()
        histeam = resul[0][0]
        if userRole == 'employee': # FTIAKSE TON EMPLOYEE XWRIS TASKS, MEETINGS, LEAVES
            globals()[username] = Employee(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], [], [], [])
            employeeInterface(globals()[username], histeam, username)
        elif userRole == 'employer':
            globals()[username] = Employer(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], resul[0][0])
            window.destroy()
            employerInterface(globals()[username],result[0][0])
           

    else:
        messagebox.showerror("Invalid Credentials", "Invalid Username or Password, please try again")
        window.destroy()
        createWindow()


def employeeInterface(name, team, username):
    if team == None:  # If the user is not part of a team
        window.destroy()
        global teamNone
        teamNone = tk.Tk()
        teamNone.geometry('800x600')
        teamNone.title('User Interface')
        teamNone.config(bg="#fbfaf2")

        label = Label(teamNone, text='You are not working for a team.', font=('Verdana', 15))
        label.pack(pady=(300, 20), anchor="center")

        checkinv = Button(teamNone, text='Check for Invitation', cursor='hand2', command=globals()[username].check_team_invitation)
        checkinv.pack(anchor="center")

        logout = Button(teamNone,
                        text='Logout',
                        font=('Verdana', 12, 'bold'),
                        fg='white',
                        bg='tomato',
                        cursor='hand2',
                        padx=10,
                        pady=5,
                        command=lambda: (teamNone.destroy(), window.destroy(), createWindow()))

        logout.place(x=680, y=20)

    else:  # If the user is part of a team
        # Retrieve tasks for the employee
        window.destroy()
        query2 = "SELECT TaskName, TaskDescription, TaskDeadline, TaskStatus FROM tasks WHERE UserID = %s"
        connect.cursor.execute(query2, (userID,))
        result2 = connect.cursor.fetchall()

        if result2:  # If there are tasks, create the objects and add them to employee.assignedTasks
            for task in result2:
                taskname = task[0]
                description = task[1]
                deadline = task[2]
                iscompleted = task[3]
                globals()[taskname] = Task(taskname, description, deadline, iscompleted)  # Create the Task object
                globals()[username].assignedTasks.append(globals()[taskname])

        # Retrieve meetings for the team
        query3 = "SELECT MeetingName, MeetingDateTime, MeetingAgenda FROM meetings WHERE TeamID = %s"
        connect.cursor.execute(query3, (team,))
        result3 = connect.cursor.fetchall()

        if result3:  # If there are meetings
            for meeting in result3:
                meetingname = meeting[0]
                meetingdate = meeting[1]
                globals()[meetingname] = Meeting(meetingname, meetingdate)  # Create the Meeting object
                globals()[username].meetingSchedule.append(globals()[meetingname])  # Add to meeting.schedule

        # Retrieve leave requests
        query4 = "SELECT LeaveName, LeaveStartDate, LeaveEndDate FROM leaverequests WHERE UserID = %s"
        connect.cursor.execute(query4, (userID,))
        result4 = connect.cursor.fetchall()

        if result4:
            for leave in result4:
                leavename = leave[0]
                start = leave[1]
                end = leave[2]
                globals()[leavename] = Leave(leavename, start, end)  # Create the Leave object
                globals()[username].leaveRequests.append(globals()[leavename])

       

        global if1
        if1 = tk.Tk()
        if1.attributes('-fullscreen', True)
        if1.title('User Interface')

        limg = Label(if1, bg='#fbfaf2')
        limg.place(relheight=1, relwidth=1)

        logout = Button(if1,
                        text='Logout',
                        font=('Verdana', 12),
                        fg='white',
                        bg='tomato',
                        cursor='hand2',
                        command=lambda: (if1.destroy(), createWindow())
                        )
        logout.place(x=1455, y=15)

        welcome = Label(if1,
                        text=f'Welcome, {name.name}',
                        font=('Helvetica', 18, 'bold italic'),
                        border=5,
                        relief="groove",
                        bg='#82924b',
                        padx=10,
                        pady=5)
        welcome.place(x=20, y=20)

        # Get the name of the team the user belongs to
        teamName = "SELECT TeamName FROM teams WHERE TeamID = %s"
        connect.cursor.execute(teamName, (team,))
        resul = connect.cursor.fetchall()
        teamName_res = resul[0][0]

        teamlabel = Label(if1,
                          text=f'Current Team: {teamName_res}',
                          font=('Verdana', 12),
                          fg='grey',
                          bg='lightblue',
                          border=3,
                          padx=5,
                          pady=3)
        teamlabel.place(x=20, y=80)

        settings = Button(if1,
                          text='Settings',
                          font=('Verdana', 12),
                          fg='black',
                          bg='white',
                          cursor='hand2',
                          command=name.profileSettings
                          )
        settings.place(x=1335, y=15)

        # Center frames for tasks, meetings, and chat
        frame_width = 300
        frame_height = 700
        

        # Tasks
        task_frame = Frame(if1, bg="#82924b", bd=4)
        task_frame.place(x=300,
                         y=100,
                         width=frame_width, height=frame_height)

        task_label = Label(task_frame,
                           text='To Do Tasks',
                           font=('Helvetica', 15, 'bold'),
                           bg='#82924b',
                           fg='white')
        task_label.pack(fill='x')

        main_taskframe = Frame(task_frame, bg="#c2d18e",pady=8)
        main_taskframe.pack(fill='both', expand=True)

        # Uncompleted tasks
        uncompleted_tasks = [task for task in name.getAssignedTasks() if task.completed == 'Uncompleted']
        if not uncompleted_tasks:
            notasks = Label(main_taskframe, text='You have no active tasks', bg='#c2d18e', fg='black', font=('bold italic',10,))
            notasks.pack(pady=120)
        for assignedTask in uncompleted_tasks:
            task = Button(main_taskframe, text=assignedTask.title, height=3, width=25, cursor='hand2',
                          command=lambda assignedTask=assignedTask: name.view_assigned_task(assignedTask))  # Adjust height and width as needed
            task.pack(pady=5)

        # Completed Tasks
        completed_task_frame = Frame(if1, bg="#82924b", bd=4)
        completed_task_frame.place(x=300,
                                   y=450,
                                   width=frame_width, height=350)

        completed_task_label = Label(completed_task_frame,
                                     text='Completed Tasks',
                                     font=('Helvetica', 15, 'bold'),
                                     bg='#82924b',
                                     fg='white')
        completed_task_label.pack(fill='x')

        completed_task_frame_inner = Frame(completed_task_frame, bg="#c2d18e",pady=8)
        completed_task_frame_inner.pack(fill='both', expand=True,)

        # Only completed tasks
        completed_tasks = [task for task in name.getAssignedTasks() if task.completed == 'Completed']
        if not completed_tasks:
            nocompletedtasks = Label(completed_task_frame_inner, text='You have no completed tasks',  bg='#c2d18e', fg='black', font=('bold italic',10))
            nocompletedtasks.pack(pady=140)
        for assignedTask in completed_tasks:
            task = Button(completed_task_frame_inner, text=assignedTask.title, height=3, width=25, cursor='hand2',
                          command=lambda assignedTask=assignedTask: name.view_assigned_task(assignedTask))  # Adjust height and width as needed
            task.pack(pady=5)

        # Meetings
        meet_frame = Frame(if1, bg="#82924b", bd=4)
        meet_frame.place(x=700,
                         y=100,
                         width=frame_width, height=700)

        meet_label = Label(meet_frame,
                           text='My Meetings',
                           font=('Helvetica', 15, 'bold'),
                           bg='#82924b',
                           fg='white')
        meet_label.pack(fill='x')

        meetframe = Frame(meet_frame, bg="#c2d18e",pady=8)
        meetframe.pack(fill='both', expand=True)

        meetings = name.getMeetings()
        if len(meetings) == 0:
            nomeets = Label(meetframe, text='You have no active meetings', bg='#c2d18e', fg='black',font=('bold italic',10))
            nomeets.pack(pady=300)
        for meeting in meetings:
            task = Button(meetframe, text=meeting.meetingName, height=3, width=25, cursor='hand2',
                          command=lambda meeting=meeting: name.view_meeting_schedule(meeting))  # Adjust height and width as needed
            task.pack(pady=5)

        # Team Chat
        chat_frame = Frame(if1, bg="#82924b", bd=4,)
        chat_frame.place(x=1100,
                         y=100,
                         width=frame_width, height=700)

        chat_label = Label(chat_frame,
                           text='Team Chat',
                           font=('Helvetica', 15, 'bold'),
                           bg='#82924b',
                           fg='white')
        chat_label.pack(fill='x')

        chat = Text(chat_frame, height=40, width=30, bg='white', fg='black')
        chat.pack(fill='both', expand=True)

        # Make Leave Request
        newLeave = Button(if1, text='Leave Request', fg='white', bg='#008080', cursor='hand2', font=('Verdana', 12), command=name.request_leave)
        newLeave.place(x=990, y=15)

        # See Leave Request Status
        leavereqButton = Button(if1, text='Leave Status', cursor='hand2', font=('Verdana', 12), bg='grey', fg='white', command=name.show_request_status)
        leavereqButton.place(x=1170, y=15)

        # REQUEST WITHDRAWAL
        withdr = Button(if1, text='Request Withdrawal', cursor='hand2', font=('Verdana', 12), bg='#d10f3f', fg='white', command= name.request_withdrawal)
        withdr.place(x=770, y=15)

        if1.mainloop()

# Function to create a new account 
def register(fname, lname, username, password, password2):
    if password != password2:
        messagebox.showerror("Error", "Passwords don't match, try again")
        window2.destroy()
    elif len(password) == 0:
        messagebox.showerror("Error", "Password must be at least one (1) character, try again")
        window2.destroy()
        registerWidgets(Event)
    else:
        # SQL QUERY
        query = "INSERT INTO users VALUES (null, %s, %s, %s, %s, null)"
        connect.cursor.execute(query, (username, password, 'employee', f'{fname} {lname}', ))
        connect.conn.commit()
        messagebox.showinfo("Success", f"Your account has been created, {fname}!")



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
    global window2


    
    # Create new widgets for register
    window2 = Tk()
    window2.geometry("350x420")
    window2.title("ProgressPulse Register")
    window2.config(bg="#bdc1b2")
    
    
    
    label_style = {'font': ('Verdana', 12, ), 'bg': '#bdc1b2', 'fg': 'black', 'padx': 10, 'pady': 5}
    entry_style = {'font': ('Verdana', 10), 'width': 25}
    button_style = {'font': ('Verdana', 12, ), 'bg': '#82924b', 'fg': 'white', 'padx': 15, 'pady': 5, 'cursor': 'hand2'}

    fname_label = Label(window2, text="Enter your first name:", **label_style)
    fname_label.pack(pady=(20, 5))
    fname_entry = Entry(window2, **entry_style)
    fname_entry.pack()

    lname_label = Label(window2, text="Enter your last name:", **label_style)
    lname_label.pack(pady=(10, 5))
    lname_entry = Entry(window2, **entry_style)
    lname_entry.pack()

    reg_username_label = Label(window2, text="Enter your username:", **label_style)
    reg_username_label.pack(pady=(10, 5))
    reg_username_entry = Entry(window2, **entry_style)
    reg_username_entry.pack()

    reg_password_label = Label(window2, text="Enter your password:", **label_style)
    reg_password_label.pack(pady=(10, 5))
    reg_password_entry = Entry(window2, show="*", **entry_style)
    reg_password_entry.pack()

    reg_password2_label = Label(window2, text="Re-enter your password:", **label_style)
    reg_password2_label.pack(pady=(10, 5))
    reg_password2_entry = Entry(window2, show="*", **entry_style)
    reg_password2_entry.pack()

    register_button = Button(window2, text="Sign Up", **button_style, command=lambda: register(fname_entry.get(), lname_entry.get(), reg_username_entry.get(), reg_password_entry.get(), reg_password2_entry.get()))
    register_button.pack(pady=(20, 10))





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
    window.geometry("800x600")
    window.title("ProgressPulse Login")
    #window.config(bg="#bdc1b2")  
    
    # Load the background image
    background_image = PhotoImage(file="images/image.png")  # Replace with the path to your image file

    # Create a label to hold the image
    background_label = Label(window, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    

    # Create a frame for the welcome label
    welcome_frame = Frame(window)
    welcome_frame.place(relx=0.5, rely=0.1, anchor="center")

    # Welcome label
    welcome_label = Label(welcome_frame,
                        text="  Welcome to ProgressPulse",
                        font=("Impact", 32, "bold"),
                        fg="white",
                        bg="#bdc1b2",  # Ορισμός του χρώματος φόντου του ετικέτας
                        )
    welcome_label.pack()

    # Create a frame for the login form
    login_frame = Frame(window, bd=1, relief="groove", padx=45, pady=80, bg="#f0f0f0", highlightbackground="#565d34", highlightthickness=2)  # Ορισμός του χρώματος φόντου του πλαισίου σύνδεσης
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Username Label and Entry
    username_label = Label(login_frame,
                            text="Username:",
                            padx=10,
                            pady=10,
                            font=("Verdana", 12),  # Χρήση διαφορετικής γραμματοσειράς
                            bg="#f0f0f0"  # Ορισμός του χρώματος φόντου του ετικέτας
                            )
    username_label.grid(row=0, column=0, sticky="w")
    username_entry = Entry(login_frame, font=("Verdana", 12))  # Χρήση διαφορετικής γραμματοσειράς
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    # Password Label and Entry
    password_label = Label(login_frame,
                            text="Password:",
                            font=("Verdana", 12),  # Χρήση διαφορετικής γραμματοσειράς
                            bg="#f0f0f0"  # Ορισμός του χρώματος φόντου του ετικέτας
                            )
    password_label.grid(row=1, column=0, sticky="w")
    password_entry = Entry(login_frame, show="*", font=("Verdana", 12))  # Χρήση διαφορετικής γραμματοσειράς και εμφάνιση * για τον κωδικό
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Login button
    login_button = Button(login_frame,
                        text="Login",
                        border=3,
                        padx=15,
                        pady=5,
                        cursor='hand2',
                        font=("Verdana", 12, "bold"),  # Χρήση διαφορετικής γραμματοσειράς και έντονη γραφή
                        bg="#82924b",
                        fg="white",
                        activebackground="#3d4122",
                        activeforeground="white",
                        command=lambda: login(username_entry.get(), password_entry.get(), window)
                        )
    login_button.grid(row=2, columnspan=2, pady=20)

    # Register option label
    clickForRegisterLabel = Label(login_frame,
                    text="If you don't have an account \n create one",
                    pady=5,
                    font=("Verdana", 10),  # Χρήση διαφορετικής γραμματοσειράς
                    bg="#f0f0f0"  # Ορισμός του χρώματος φόντου του ετικέτας
                    )
    clickForRegisterLabel.grid(row=3, columnspan=2)

    # "here" button to go for create account
    clickForRegister = Label(login_frame,
                text="here",
                fg="blue",
                cursor="hand2",
                font=("Verdana", 10, "underline"),  # Χρήση διαφορετικής γραμματοσειράς και υπογράμμιση
                bg="#f0f0f0"  # Ορισμός του χρώματος φόντου του ετικέτας
                )
    clickForRegister.grid(row=4, columnspan=2)
    clickForRegister.bind("<Button-1>", registerWidgets)

    window.mainloop()

    
# RUN window function to start the program ...
if __name__ == "__main__":
    connect.connectToDatabase()
    createWindow()