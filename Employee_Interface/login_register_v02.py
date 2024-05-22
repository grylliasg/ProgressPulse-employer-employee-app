from tkinter import *
from tkinter import messagebox
from employee import *
import connect

# Function for Login (+ Check credentials)
def login(username, password, window):
    #EMPLOYEE __init__(self, name, id, username, password, role, assignedTasks, meetingSchedule, leaveRequests):
    query = "SELECT name, UserID, Username, Password, UserRole FROM users WHERE Username = %s AND Password = %s"
    connect.cursor.execute(query, (username, password))
    result = connect.cursor.fetchall()
      
    if result: # FTIAKSE TON EMPLOYEE XWRIS TASKS, MEETINGS, LEAVES
        userID = result[0][1]
        globals()[username] = Employee(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], [], [], [])

        # PSAKSE GIA tasks TOY EMPLOYEE 
        query2 = "SELECT TaskName, TaskDescription, TaskDeadline, TaskStatus FROM tasks WHERE UserID = %s"
        connect.cursor.execute(query2, (userID, ))
        result2 = connect.cursor.fetchall()

        if result2: # AMA YPARXOYN TASKS, FTIAKSE TA OBJECTS KAI VALTA STON EMPLOYEE.ASSIGNEDTASKS
            for task in result2:
                taskname = task[0]
                description = task[1]
                deadline = task[2]
                iscompleted = task[3]
                globals()[taskname] = Task(taskname, description, deadline, iscompleted) # DHMIOURGIA TOY OBJECT TASK
                globals()[username].assignedTasks.append(globals()[taskname])

        # VRES SE POIA OMADA ANHKEI AUTOS O EMPLOYEE
        quer = "SELECT Team FROM users WHERE UserID = %s"
        connect.cursor.execute(quer, (userID, ))
        resul = connect.cursor.fetchall()
        histeam = resul[0][0]

        # FERE TA MEETINGS POY ANHKOUN STHN OMADA TOY 
        query3 = "SELECT MeetingName, MeetingDateTime, MeetingAgenda FROM meetings WHERE TeamID = %s"
        connect.cursor.execute(query3, (histeam, ))
        result3 = connect.cursor.fetchall()

        if result3: # AN YPARXOUN MEETINGS
            for meeting in result3:
                meetingname = meeting[0]
                meetingdate = meeting[1]
                globals()[meetingname] = Meeting(meetingname, meetingdate) # DHMIOURGIA TOY OBJECT MEETING
                globals()[username].meetingSchedule.append(globals()[meetingname]) # PROSTHIKI STO meeting.schedule

        # FERE TA LEAVES
        query4 = "SELECT LeaveName, LeaveStartDate, LeaveEndDate FROM leaverequests WHERE UserID = %s"
        connect.cursor.execute(query4, (userID, ))
        result4 = connect.cursor.fetchall()

        if result4:
            for leave in result4:
                leavename = leave[0]
                start = leave[1]
                end = leave[2]
                globals()[leavename] = Leave(leavename, start, end) # DHMIOURGIA TOY OBJECT LEAVE
                globals()[username].leaveRequests.append(globals()[leavename])

        if histeam != None: # AN ANHKEI SE MIA OMADA => REDIRECT TO employeeInterface
            window.destroy()
            employeeInterface(globals()[username], histeam)

        else:
            window.destroy()
            
            global teamNone
            teamNone = Tk()
            teamNone.geometry('600x550')
            teamNone.title('User Interface')

            label = Label(teamNone, text='You are not working for a team.', font=('Arial', 15)).pack(pady=(0,20))
            checkinv = Button(teamNone, text='Check for Invitation', cursor='hand2', command= globals()[username].check_team_invitation).pack()

            logout = Button(teamNone,
                text='Logout',
                font=('Arial', 12, 'bold'),
                fg='white',
                bg='tomato',
                cursor='hand2',
                padx=10,
                pady=5,
                command=lambda: (teamNone.destroy(), createWindow()))

            logout.place(x=520, y=25)


    else:
        messagebox.showerror("Invalid Credentials", "Invalid Username or Password, please try again")
        window.destroy()
        createWindow()

  
def employeeInterface(name, team):
    global if1

    if1 = Tk()
    if1.attributes('-fullscreen', True)
    if1.title('User Interface')

    limg= Label(if1, bg='lightblue')
    limg.place(relheight=1, relwidth=1)

    logout = Button(if1,
                    text='Logout',
                    font=('Arial', 10),
                    fg='white',
                    bg='red',
                    cursor='hand2',
                    command= lambda: (if1.destroy(), createWindow())
                    )
    logout.place(x=1470, y=15)

    welcome = Label(if1, 
                text=f'Welcome, {name.name}', 
                font=('Helvetica', 18, 'bold italic'), 
                border=5, 
                relief="groove", 
                bg='lightblue', 
                padx=10, 
                pady=5)
    welcome.place(x=20, y=20)

    # VRES TO ONOMA TOU TEAM POU ANHKEI
    teamName = "SELECT TeamName FROM teams WHERE TeamID = %s"
    connect.cursor.execute(teamName, (team, ))
    resul = connect.cursor.fetchall()
    teamName_res = resul[0][0]

    teamlabel = Label(if1, 
                 text=f'Current Team: {teamName_res}', 
                 font=('Arial', 12), 
                 fg='grey', 
                 bg='lightblue',
                 border=3,
                 padx=5, 
                 pady=3)
    teamlabel.place(x=20, y=80)

    settings = Button(if1,
                    text='Ρυθμίσεις Λογαριασμού',
                    font=('Arial', 10),
                    fg='black',
                    bg='white',
                    cursor='hand2',
                    command= name.profileSettings
                    )
    settings.place(x=1300, y=15)

    # TASKS
    task_label = Label(if1, 
                   text='my Tasks', 
                   font=('Helvetica', 15, 'bold italic'), 
                   bg='lightsteelblue', 
                   padx=10, 
                   pady=5)

    task_label.place(x=348, y=90)
    main_taskframe = Frame(if1, bg="lightgrey", bd=4)
    main_taskframe.place(x=345, y=130)

    assignedTasks = name.getAssignedTasks()
    if all(assignedTask.completed == 'Completed' for assignedTask in assignedTasks) or len(assignedTasks) == 0:
        notasks = Label(main_taskframe, text='You have not active tasks')
        notasks.pack()
    for assignedTask in assignedTasks:
        if assignedTask.completed == 'Uncompleted':
            task = Button(main_taskframe, text=assignedTask.title, height=5, width=15, cursor='hand2',  command= lambda assignedTask=assignedTask: name.view_assigned_task(assignedTask))  # Adjust height and width as needed
            task.pack()


    # MEETINGS
    meet_label = Label(if1, 
                   text='my Meetings', 
                   font=('Helvetica', 15, 'bold italic'), 
                   bg='lightsteelblue', 
                   padx=10, 
                   pady=5)

    meet_label.place(x=618, y=90)
    meetframe = Frame(if1, bg="lightgrey", bd=4)
    meetframe.place(x=630, y=130)

    meetings = name.getMeetings()
    if len(meetings) == 0:
        nomeets = Label(meetframe, text='You have not active meetings')
        nomeets.pack()
    for meeting in meetings:
        task = Button(meetframe, text=meeting.meetingName, height=5, width=15, cursor='hand2', command= lambda meeting=meeting:name.view_meeting_schedule(meeting))  # Adjust height and width as needed
        task.pack()

    # CHAT
    chatLabel = Label(if1, 
                   text='Chat:', 
                   font=('Helvetica', 15, 'bold italic'), 
                   bg='lightsteelblue', 
                   padx=10, 
                   pady=5)
    chatLabel.place(x=990, y=90)
    chat = Text(if1, height=20, width=30)
    chat.place(x=990, y=130)

    # Completed Tasks
    # Create a button to show completed tasks
    comTasks = Button(if1, 
                  text='Show Completed Tasks', 
                  fg='white', 
                  bg='green', 
                  cursor='hand2', 
                  font=('Arial', 12), 
                  command=name.show_completed_tasks)

    comTasks.place(x=5, y=690)

    # Make Leave Request
    newLeave = Button(if1, text='Make Leave Request', fg='white', bg='blue', cursor='hand2', font=('Arial', 12), command= name.request_leave)
    newLeave.place(x=5, y=730)

    # SEE THE LEAVE REQUEST STATUS
    leavereqButton = Button(if1, text='See Leave Status', cursor='hand2', font=('Arial', 10), bg='grey', fg='white', command= name.show_request_status)
    leavereqButton.place(x=5, y=770)

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
        query = "INSERT INTO users VALUES (null, %s, %s, %s, %s, null)"
        connect.cursor.execute(query, (username, password, 'employee', f'{fname} {lname}', ))
        connect.conn.commit()
        messagebox.showinfo("Success", f"Your account has been created, {fname}!")
        window.destroy()
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
                         cursor='hand2',
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



