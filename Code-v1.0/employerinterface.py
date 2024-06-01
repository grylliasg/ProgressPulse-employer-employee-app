from employer import Employer
from employee import *
from tkinter import *
import tkinter as tk
from tkcalendar import DateEntry
from employeeinterface_main import createWindow



def on_create_project(employer):
    description = description_entry.get()
    name = name_entry1.get()
    team_id =team_entry.get()
    employer.create_project(name, description,team_id)
    messagebox.showinfo("Success", "Project created successfully!")
   


def on_create_meeting(employer):
    meeting_name =  name_entry.get()
    meeting_datetime = datetime_entry.get()
    meeting_agenda = agenda_entry.get()
    team_id = team_id_meeting_entry.get()
    employer.create_meeting(meeting_datetime, meeting_agenda, team_id,meeting_name)
    messagebox.showinfo("Success", "Meeting created successfully!")
    



def on_view_leave_requests(employer):

        leave_requests = employer.view_leave_requests()
        if leave_requests:
            leave_requests_str = "\n".join([
                f"Request ID: {request[0]}\nUser ID: {request[1]}\nStart Date: {request[2]}\nEnd Date: {request[3]}\nStatus: {request[4]}\n"
                for request in leave_requests
            ])
            
            # Create a new window to display leave requests
            leave_window = tk.Toplevel(if2)
            leave_window.title("Leave Requests")

            for i, request in enumerate(leave_requests):
                request_str = f"Request ID: {request[0]}\nStart Date: {request[1]}\nEnd Date: {request[2]}\nStatus: {request[3]}\nUser ID: {request[4]}\n"
                tk.Label(leave_window, text=request_str, anchor='w', justify='left').grid(row=i, column=0, sticky='w')

                accept_button = tk.Button(leave_window, text="Accept", command=lambda req_id=request[0]: on_accept_leave(req_id,employer))
                accept_button.grid(row=i, column=1)

                deny_button = tk.Button(leave_window, text="Deny", command=lambda req_id=request[0]: on_deny_leave(req_id,employer))
                deny_button.grid(row=i, column=2)

        else:
            messagebox.showinfo("Leave Requests", "No leave requests found.")
    


def on_accept_leave(leave_request_id,employer):
   
        employer.accept_leave_request(leave_request_id)
        messagebox.showinfo("Success", f"Leave request {leave_request_id} accepted.")
        on_view_leave_requests()  # Refresh the list
    

def on_deny_leave(leave_request_id,employer):
    
        employer.deny_leave_request(leave_request_id)
        messagebox.showinfo("Success", f"Leave request {leave_request_id} denied.")
        on_view_leave_requests()  # Refresh the list
   





def on_view_progress(employer):
    
        progress_data = employer.view_progress()
        progress_str = "Project Progress:\n\n"
        for row in progress_data:
            progress_str += f"Project ID: {row[0]}\n"
            progress_str += f"Project Name: {row[1]}\n"
            progress_str += f"Total Tasks: {row[2]}\n"
            progress_str += f"Completed Tasks: {row[3]}\n\n"
        messagebox.showinfo("Progress", progress_str)
   





def on_view_team_settings(employer):
    
        # Create a new window to display team settings
        team_window = tk.Toplevel(if2)
        team_window.title("Team Settings")

        # Team name update
        tk.Label(team_window, text="New Team Name:", anchor='w', justify='left').grid(row=0, column=0, sticky='w')
        team_name_entry = tk.Entry(team_window)
        team_name_entry.grid(row=0, column=1)

        update_team_name_button = tk.Button(team_window, text="Update Team Name", command=lambda: on_update_team_name(team_name_entry.get(),employer))
        update_team_name_button.grid(row=0, column=2)

        # Team description update
        tk.Label(team_window, text="New Team Description:", anchor='w', justify='left').grid(row=1, column=0, sticky='w')
        team_description_entry = tk.Entry(team_window)
        team_description_entry.grid(row=1, column=1)

        update_team_description_button = tk.Button(team_window, text="Update Team Description", command=lambda: on_update_team_description(team_description_entry.get(),employer))
        update_team_description_button.grid(row=1, column=2)

    

def on_update_team_name(new_team_name,employer):
    
        employer.change_team_name(new_team_name)
        messagebox.showinfo("Success", "Team name updated successfully.")
   

def on_update_team_description(new_team_description,employer):
    
        employer.change_team_description(new_team_description)
        messagebox.showinfo("Success", "Team description updated successfully.")
    



def on_view_team_members(employer):
    
        team_members = employer.view_team_members()  
        team_window = tk.Toplevel(if2)
        team_window.title("Team Members")
        if team_members:
            # Create a new window to display team members
          

            for i, member in enumerate(team_members):
                member_str = f"User ID: {member[0]}\nUsernmame: {member[1]}\nName: {member[4]}\n"
                tk.Label(team_window, text=member_str, anchor='w', justify='left').grid(row=i, column=0, sticky='w')

                remove_button = tk.Button(team_window, text="Remove Member", command=lambda user_id=member[0]: on_remove_member(user_id,employer))
                remove_button.grid(row=i, column=1)
        
             # Invite Member section
            invite_label = tk.Label(team_window, text="Invite Member (User ID):", anchor='w', justify='left')
            invite_label.grid(row=len(team_members), column=0, sticky='w')

            invite_entry = tk.Entry(team_window)
            invite_entry.grid(row=len(team_members), column=1)

            invite_button = tk.Button(team_window, text="Invite Member", command=lambda: on_invite_member(invite_entry.get(),employer))
            invite_button.grid(row=len(team_members), column=2)

        else:
            no_members_label = tk.Label(team_window, text="No team members found", anchor='w', justify='left')
            no_members_label.grid(row=len(team_members), column=0, sticky='w')
            invite_button = tk.Button(team_window, text="Invite Member", command=lambda: on_invite_member(invite_entry.get(),employer))
            invite_button.grid(row=len(team_members), column=2)
    

def on_remove_member(user_id,employer):
    
        employer.remove_member_from_team(user_id)
        messagebox.showinfo("Success", f"Member {user_id} removed from team.")
        
    


def on_invite_member(user_id,employer):
    try:
        employer.invite_member_to_team(user_id)
        messagebox.showinfo("Success", f"Member {user_id} invited to team.")
       
    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_open_create_task_window(employer):
    # Create a new window for task creation
    global create_task_window
    create_task_window = tk.Toplevel(if2)
    create_task_window.title("Create Task")

    # Task Name
    name_label = tk.Label(create_task_window, text="Task Name:")
    name_label.grid(row=0, column=0, sticky='w')
    name_entry = tk.Entry(create_task_window)
    name_entry.grid(row=0, column=1)

    # Task description
    description_label = tk.Label(create_task_window, text="Task Description:")
    description_label.grid(row=1, column=0, sticky='w')
    description_entry = tk.Entry(create_task_window)
    description_entry.grid(row=1, column=1)

    # Task deadline
    deadline_label = tk.Label(create_task_window, text="Task Deadline:")
    deadline_label.grid(row=2, column=0, sticky='w')
    deadline_entry = DateEntry(create_task_window, date_pattern='yyyy-mm-dd')
    deadline_entry.grid(row=2, column=1)

    # User ID
    user_id_label = tk.Label(create_task_window, text="User ID:")
    user_id_label.grid(row=3, column=0, sticky='w')
    user_id_entry = tk.Entry(create_task_window)
    user_id_entry.grid(row=3, column=1)

    # Project ID
    project_id_label = tk.Label(create_task_window, text="Project ID:")
    project_id_label.grid(row=4, column=0, sticky='w')
    project_id_entry = tk.Entry(create_task_window)
    project_id_entry.grid(row=4, column=1)

    # Create task button
    create_button = tk.Button(create_task_window, text="Create Task", command=lambda: on_create_task(employer,name_entry.get(),description_entry.get(), deadline_entry.get(), user_id_entry.get(), project_id_entry.get()))
    create_button.grid(row=5, column=0, columnspan=2)



def on_create_task(employer,name,description, deadline, user_id, project_id):
    try:
        employer.create_task(name,description, deadline, user_id, project_id)
        messagebox.showinfo("Success", "Task created successfully!")
        create_task_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))



def on_control_withdrawals(employer):
    withdrawal_requests = employer.view_withdrawal_requests()
    
    if withdrawal_requests:
        withdrawal_window = tk.Toplevel(if2)
        withdrawal_window.title("Withdrawal Requests")
        withdrawal_window.geometry("400x300")
        
        for idx, request in enumerate(withdrawal_requests):
            request_str = f"UserID: {request[0]}, Status: {request[1]}"  # Assuming request is a tuple (UserID, Status)
            tk.Label(withdrawal_window, text=request_str).grid(row=idx, column=0, padx=10, pady=5)
            
            accept_button = tk.Button(withdrawal_window, text="Accept", command=lambda user_id=request[0]: handle_accept_withdrawal(user_id,employer))
            accept_button.grid(row=idx, column=1, padx=5, pady=5)
            
            deny_button = tk.Button(withdrawal_window, text="Deny", command=lambda user_id=request[0]: handle_deny_withdrawal(user_id,employer))
            deny_button.grid(row=idx, column=2, padx=5, pady=5)
    else:
        messagebox.showinfo("No Withdrawals", "No withdrawal requests found.")

def handle_accept_withdrawal(user_id,employer):
        employer.accept_withdrawal(user_id)
        messagebox.showinfo("Success", "Withdrawal accepted successfully!")
  

def handle_deny_withdrawal(user_id,employer):
    
        employer.deny_withdrawal(user_id)
        messagebox.showinfo("Success", "Withdrawal denied successfully!")
    
def on_view_meetings(employer):
    meetings = employer.view_meetings()
    if not meetings:
        messagebox.showinfo("My Meetings", "No meetings found.")
    else:
        meetings_str = "My Meetings:\n\n"
        for meeting in meetings:
            meetings_str += f"ID: {meeting[0]}, DateTime: {meeting[1]}, Agenda: {meeting[2]}\n"
        messagebox.showinfo("My Meetings", meetings_str)

def on_delete_meeting(meeting_id,employer):
    try:
        employer.delete_meeting(meeting_id)
        messagebox.showinfo("Success", "Meeting deleted successfully!")
        on_view_meetings()  # Refresh the meetings list
    except Exception as e:
        messagebox.showerror("Error", str(e))



def employerInterface(employer,name):
    global if2, name_entry,name_entry1, description_entry, team_entry,meetings_frame  # Declare the entry variables as global
    global datetime_entry, agenda_entry, team_id_meeting_entry  # Declare the meeting entry variables as global

    if2 = tk.Tk()
    if2.attributes('-fullscreen', True)
    if2.title('User Interface')

    limg = tk.Label(if2, bg='lightblue')
    limg.place(relheight=1, relwidth=1)

    logout = tk.Button(if2,
                       text='Logout',
                       font=('Arial', 10),
                       fg='white',
                       bg='red',
                       cursor='hand2',
                       command=lambda: (if2.destroy(), createWindow())
                       )
    logout.place(x=1470, y=15)

    welcome = tk.Label(if2, 
                       text=f'Welcome, {name} ', 
                       font=('Helvetica', 18, 'bold italic'), 
                       border=5, 
                       relief="groove", 
                       bg='lightblue', 
                       padx=10, 
                       pady=5)
    welcome.place(x=20, y=20)

    settings = tk.Button(if2,
                         text='Ρυθμίσεις Λογαριασμού',
                         font=('Arial', 10),
                         fg='black',
                         bg='white',
                         cursor='hand2',
                         #command= name.profileSettings
                         )
    settings.place(x=1300, y=15)

    # CREATE PROJECT
    task_label = tk.Label(if2, 
                          text='Create Project', 
                          font=('Helvetica', 15, 'bold italic'), 
                          bg='lightsteelblue', 
                          padx=10, 
                          pady=5)
    task_label.place(x=248, y=90)

    main_taskframe = tk.Frame(if2, bg="lightgrey", height=200, width=300, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    main_taskframe.place(x=145, y=130)

    # Entry for project name
    name_label = tk.Label(main_taskframe, text="Project Name", bg="lightgrey")
    name_label.place(x=10, y=10)
    name_entry1 = tk.Entry(main_taskframe)
    name_entry1.place(x=150, y=10)

    # Entry for project description
    description_label = tk.Label(main_taskframe, text="Project Description", bg="lightgrey")
    description_label.place(x=10, y=50)
    description_entry = tk.Entry(main_taskframe)
    description_entry.place(x=150, y=50)


    team_id_label = tk.Label(main_taskframe, text="Team ID", bg="lightgrey")
    team_id_label.place(x=10, y=90)  # Αλλαγή y τιμής
    team_entry = tk.Entry(main_taskframe)
    team_entry.place(x=150, y=90)
    


    # Create project button
    create_button = tk.Button(main_taskframe, text="Create Project", command=lambda:on_create_project(employer))
    create_button.place(x=100, y=130)


    # CREATE MEETING
    meet_label = tk.Label(if2, 
                          text='Create Meeting', 
                          font=('Helvetica', 15, 'bold italic'), 
                          bg='lightsteelblue', 
                          padx=10, 
                          pady=5)
    meet_label.place(x=518, y=90)

    meetframe = tk.Frame(if2, bg="lightgrey", height=300, width=300, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    meetframe.place(x=480, y=130)


        # Entry για το όνομα της συνάντησης
    name_label = tk.Label(meetframe, text="Meeting Name", bg="lightgrey")
    name_label.place(x=10, y=10)  # Αλλαγή y τιμής
    name_entry = tk.Entry(meetframe)
    name_entry.place(x=150, y=10)

    # Entry για την ημερομηνία και την ώρα της συνάντησης
    datetime_label = tk.Label(meetframe, text="Meeting DateTime", bg="lightgrey")
    datetime_label.place(x=10, y=50)  # Αλλαγή y τιμής
    datetime_entry = DateEntry(meetframe, date_pattern='yyyy-mm-dd')
    datetime_entry.place(x=150, y=50)

    # Entry για την ατζέντα της συνάντησης
    agenda_label = tk.Label(meetframe, text="Meeting Agenda", bg="lightgrey")
    agenda_label.place(x=10, y=90)  # Αλλαγή y τιμής
    agenda_entry = tk.Entry(meetframe)
    agenda_entry.place(x=150, y=90)

    # Entry για το Team ID της συνάντησης
    team_id_meeting_label = tk.Label(meetframe, text="Team ID", bg="lightgrey")
    team_id_meeting_label.place(x=10, y=130)  # Αλλαγή y τιμής
    team_id_meeting_entry = tk.Entry(meetframe)
    team_id_meeting_entry.place(x=150, y=130)

    # Δημιουργία του κουμπιού "Create Meeting"
    create_meeting_button = tk.Button(meetframe, text="Create Meeting", command=lambda: on_create_meeting(employer))
    create_meeting_button.place(x=100, y=170)


    # SHOW PROGRESS
    chat_label = tk.Label(if2, 
                          text='Show Progress', 
                          font=('Helvetica', 15, 'bold italic'), 
                          bg='lightsteelblue', 
                          padx=10, 
                          pady=5)
    chat_label.place(x=790, y=90)

    # Show progress button
    show_progress_button = tk.Button(if2, text="Show Progress",
                                     fg='white', 
                                     bg='red', 
                                     cursor='hand2', 
                                    font=('Arial', 12), command=lambda:on_view_progress(employer))
    show_progress_button.place(x=790, y=130)

    # CHAT
    chatLabel = Label(if2, 
                text='Chat:', 
                font=('Helvetica', 15, 'bold italic'), 
                bg='lightsteelblue', 
                padx=10, 
                pady=5)
    chatLabel.place(x=1090, y=90)
    chat = Text(if2, height=20, width=30)
    chat.place(x=1100, y=130)


# LEAVES
    leaves = Button(if2, 
                    text='Leave Requests', 
                    fg='white', 
                    bg='blue', 
                    cursor='hand2', 
                    font=('Arial', 12),
                    command=lambda:on_view_leave_requests(employer) 
                    )

    leaves.place(x=1000, y=20)

#TEAMMEBERS
    
    teammembers = Button(if2, 
                     text='Team Members', 
                     fg='white', 
                     bg='green', 
                     cursor='hand2', 
                     font=('Arial', 12), 
                     command=lambda:on_view_team_members(employer)
                     )
    teammembers.place(x=810, y=20)

    withdrawals = tk.Button(if2, 
                       text='Control Withdrawals', 
                        fg='white', 
                        bg='red', 
                       cursor='hand2', 
                      font=('Arial', 12), 
                       command=lambda:on_control_withdrawals(employer))

    withdrawals.place(x=632, y=20)

    members = Button(if2, 
                 text='Team Settings', 
                 fg='white', 
                 bg='orange', 
                 cursor='hand2', 
                 font=('Arial', 12), 
                 command=lambda:on_view_team_settings(employer)
                 )
    members.place(x=350, y=20)


    create_task_button = Button(if2, 
                            text='Create Task', 
                            fg='white', 
                            bg='purple', 
                            cursor='hand2', 
                            font=('Arial', 12), 
                            command=lambda:on_open_create_task_window(employer)
                            )
    create_task_button.place(x=1150, y=20)



     # MY MEETINGS
    meetings_button = tk.Button(if2, 
                                text='My Meetings', 
                                fg='white', 
                                bg='blue', 
                                cursor='hand2', 
                                font=('Arial', 12), 
                                command=lambda:on_view_meetings(employer))
    meetings_button.place(x=491, y=20)

   
    if2.mainloop()


