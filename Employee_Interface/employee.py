from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import connect
from classes import *

class User:
    def __init__(self, name, id, username, password, role):
        self.name = name
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def profileSettings(self):
        profSettIf = Tk()
        profSettIf.geometry('350x200')
        profSettIf.title('Profile Settings')

        def closeSettWindow():
            profSettIf.destroy()

        def setName():
            name.forget()
            pwrd.forget()
            leave.forget()

            def submitName():
                if self.name == nameEntry.get():
                    messagebox.showwarning('Wrong Name', 'You entered your existing name.')
                    nameEntry.delete(0, END)
                    nameEntry.delete(0, END)
                else:
                    self.name = nameEntry.get()
                    query = "UPDATE users SET name = %s WHERE UserID = %s"
                    connect.cursor.execute(query, (self.name, self.id))
                    connect.conn.commit()
                    messagebox.showinfo('Success', f'New Name = {self.name}')
                    profSettIf.destroy()

            nameLabel = Label(profSettIf, text='Enter Your New name:')
            nameLabel.pack()
            nameEntry =  Entry(profSettIf)
            nameEntry.pack()
            submit = Button(profSettIf, text='Submit', cursor='hand2',  command=submitName)
            submit.pack()


        def setPassword():
            name.forget()
            pwrd.forget()
            leave.forget()

            def submitPassword():
                if self.password != oldEntry.get():
                    messagebox.showerror('Wrong Password', 'The Old password you entered is wrong')
                    oldEntry.delete(0, END)
                    newEntry.delete(0, END)
                else:
                    self.password = newEntry.get()
                    query = "UPDATE users SET password = %s WHERE name = %s"
                    connect.cursor.execute(query, (self.password, self.name))
                    connect.conn.commit()
                    messagebox.showinfo('Success', 'Your Password has been changed')
                    profSettIf.destroy()


            oldLabel = Label(profSettIf, text='Enter Your Old password:')
            oldLabel.pack()
            oldEntry =  Entry(profSettIf, show='*')
            oldEntry.pack()
            newLabel = Label(profSettIf, text='Enter Your New password:')
            newLabel.pack()
            newEntry =  Entry(profSettIf, show='*')
            newEntry.pack()
            submit = Button(profSettIf, text='Submit', cursor='hand2',  command=submitPassword)
            submit.pack()

        name = Button(profSettIf, text='Change Your Name', cursor='hand2', command= setName)
        name.pack()
        pwrd = Button(profSettIf, text='Change Your Password', cursor='hand2', command= setPassword)
        pwrd.pack()
        leave = Button(profSettIf, text='Aποχώρηση', cursor='hand2', command= closeSettWindow)
        leave.pack()

        profSettIf.mainloop()


class Employee(User):
    def __init__(self, name, id, username, password, role, assignedTasks, meetingSchedule, leaveRequests):
        super().__init__(name, id, username, password, role)
        self.assignedTasks = assignedTasks
        self.meetingSchedule = meetingSchedule
        self.leaveRequests = leaveRequests

    def getAssignedTasks(self):
        return self.assignedTasks
    
    def getMeetings(self):
        return self.meetingSchedule
    
    def check_team_invitation(self):
        pass

    def request_withdrawal(self):
        pass
    
    def show_completed_tasks(self):
        global win
        win = Tk()
        win.geometry('350x450')

        task_label = Label(win, text='Completed Tasks:', font=('Arial', 15))
        task_label.place(x=5, y=0)
        main_comtaskframe = Frame(win, bg="lightgrey", bd=4)
        main_comtaskframe.place(x=90, y=90)

        for assignedTask in self.assignedTasks:
            if assignedTask.completed == 'Completed':
                comtasklabel = Button(main_comtaskframe, text=assignedTask.title, height=5, width=15, cursor='hand2',  command= lambda assignedTask=assignedTask: self.view_assigned_task(assignedTask)).pack()
            else:
                pass
    
    def view_assigned_task(self, task):
        taskwin = Tk()
        taskwin.geometry('350x350')

        def mark_task_complete():
            query = 'UPDATE tasks SET TaskStatus = %s WHERE TaskName = %s'
            connect.cursor.execute(query, ('Completed', task.title))
            connect.conn.commit()
            task.completed = 'Completed'
            taskwin.destroy()

        def unmark_completed_task():
            query = 'UPDATE tasks SET TaskStatus = %s WHERE TaskName = %s'
            connect.cursor.execute(query, ('Uncompleted', task.title))
            connect.conn.commit()
            task.completed = 'Uncompleted'
            taskwin.destroy()
            win.destroy()
            

        task_details = Label(taskwin, text=f'Task Title: {task.title}\n\nDescription: {task.description}\n\nDeadline: {task.deadline}\n', font=('Arial', 15))
        task_details.pack()

        if task.completed == 'Uncompleted':
            complete = Button(taskwin, text='Complete this Task', bg='green', fg='white', font=('Arial', 15), border=2, cursor='hand2', command= mark_task_complete)
            complete.pack()
        else:
            completed = Label(taskwin, text='This Task is Completed!', font=('Arial', 15), fg='green').pack()
            unmark = Button(taskwin, text='Unmark Completed Task', font=('Arial, 13'), cursor='hand2', fg='orange', command= unmark_completed_task).pack()

    def view_meeting_schedule(self, meeting):
        meetwin = Tk()
        meetwin.geometry('350x350')
        meetwin.title('Meeting Details')

        def attend_meeting(meeting):
            self.meetingSchedule.append(meeting)
            meetwin.destroy()

        def request_not_attend_meeting(meeting):
            self.meetingSchedule.remove(meeting)
            meetwin.destroy()
            

        meeting_details = Label(meetwin, text=f'Meeting Title: {meeting.meetingName}\n\nDescription: {meeting.date}\n\n', font=('Arial', 15))
        meeting_details.pack()

        if meeting in self.meetingSchedule:
            notattend = Button(meetwin, text='Not Attend', fg='red', font=('Arial', 12), cursor='hand2', command=lambda:request_not_attend_meeting(meeting)).pack()
        else:
            notattendlabel = Label(meetwin, text="You're not attending this meeting.", font=('Arial', 14), fg='red').pack()
            unmark = Button(meetwin, text='Click to Attend', font=('Arial, 13'), cursor='hand2', fg='orange', command= lambda:attend_meeting(meeting)).pack()

    def request_leave(self):
        leavewin = Tk()
        leavewin.geometry('350x350')
        leavewin.title('Leave Request')

        def submit_leave_request(start, end, name):

            # ELEGXOS AN O EMPLOYEE EXEI HDH ENA APODEKTO LEAVE POU TON PERIMENEI
            hasrequest = 'SELECT LeaveRequestID FROM leaverequests WHERE UserID = %s AND LeaveStatus = %s'
            connect.cursor.execute(hasrequest, (self.id, 'Αποδεκτή'))
            hasrequestres = connect.cursor.fetchall()

            if hasrequestres: # APOTELESMA ELEGXOU = TRUE
                messagebox.showwarning('Failure', "You've got already an approved request")
                leavewin.destroy()

            else: # ALLIWS, ELEGXOS AN OI HMEROMINIES POU EVALE PEFTOUN MESA SE ALLO APODEKTO LEAVE
                apprdates = 'SELECT LeaveStartDate, LeaveEndDate FROM leaverequests WHERE LeaveStatus = %s'
                connect.cursor.execute(apprdates, ('Αποδεκτή', ))
                apprdates_res = connect.cursor.fetchall()

                for date in apprdates_res: # GIA KATHE APODEKTO LEAVE REQUEST TSEKARE TIS HMEROMHNIES
                    if date[0] <= start <= date[1] or date[0] <= end <= date[1]:
                        messagebox.showwarning('Failure', "There is another approved request between these dates")
                        leavewin.destroy()
                    else:
                        submitleave = 'INSERT INTO leaverequests VALUES (null, %s, %s, %s, %s, %s)'
                        connect.cursor.execute(submitleave, (start, end, 'Υπο εξέταση', self.id, name))
                        connect.conn.commit()
                        messagebox.showinfo('Submitted', f"Your leave request ({start} - {end}) has been submitted!")
                        leavewin.destroy()
            

        label = Label(leavewin, text="Submit Your Leave Request", font=('Arial', 15)).pack()

        namelabel = Label(leavewin, text='Request Name:', font=('Arial', 12)).pack(pady=(10,0))
        name = Entry(leavewin)
        name.pack(pady=(0,15))

        sdatelabel = Label(leavewin, text='Start Date:', font=('Arial', 12))
        sdatelabel.pack(pady=(15,0))
        start = DateEntry(leavewin, width=17, background="darkblue", foreground="white", borderwidth=2)
        start.pack(pady=(0,15))

        edatelabel = Label(leavewin, text='End Date:', font=('Arial', 12))
        edatelabel.pack()
        end = DateEntry(leavewin, width=17, background="darkblue", foreground="white", borderwidth=2)
        end.pack(pady=(0,50))

        submit = Button(leavewin, text='Submit', font=('Arial', 12), bg='lightblue', cursor='hand2', border=3, command=lambda: submit_leave_request(start.get_date(), end.get_date(), name.get()))
        submit.pack()

        leavewin.mainloop()

    def show_request_status(self):
        statuswin = Tk()
        statuswin.geometry('450x450')
        statuswin.title('Leave Request Status')

        status = 'SELECT LeaveStatus, LeaveRequestID, LeaveStartDate, LeaveEndDate, LeaveName FROM leaverequests WHERE UserID = %s'
        connect.cursor.execute(status, (self.id, ))
        res = connect.cursor.fetchall()

        scrollbar = Scrollbar(statuswin, orient=VERTICAL)
        scrollbar.pack(side="right", fill="y")

        text = Text(statuswin, wrap="word", yscrollcommand=scrollbar.set)
        text.pack(expand=True, fill="both")
        scrollbar.config(command=text.yview)

        for r in res:
            status_res = r[0]
            id = r[1]
            start = r[2]
            end = r[3]
            name = r[4]

            text.insert(END, f'The Status of your request is: {status_res}\n\n')
            text.insert(END, f'Leave Request Id: {id}\nLeave Start: {start}\nLeave End: {end}\nLeave Name: {name}\n\n')

        statuswin.mainloop()

