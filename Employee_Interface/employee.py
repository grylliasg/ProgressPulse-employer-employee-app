from tkinter import *
from tkinter import Tk, Label, Button, messagebox
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
        profSettIf.geometry('400x200')
        profSettIf.title('Profile Settings')
        profSettIf.config(bg="#bdc1b2")

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

            nameLabel = Label(profSettIf, text='Enter Your New Name:', font=('Verdana', 12))
            nameLabel.pack(pady=(40, 5),anchor='center')
            
            nameEntry =  Entry(profSettIf, font=('Verdana', 12), width=25, bd=2)
            nameEntry.pack(pady=(0, 10),anchor='center')
            
            
            submit = Button(profSettIf, text='Submit', font=('Verdana', 12), bg='olive', cursor='hand2', command=submitName, bd=2)
            submit.pack()
            
            
        #Password Settings

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

            
            oldLabel = Label(profSettIf, text='Enter Your Old Password:', font=('Verdana', 12))
            oldLabel.pack(pady=(20, 5))
            
            oldEntry = Entry(profSettIf, show='*', font=('Verdana', 12), width=25, bd=2)
            oldEntry.pack(pady=(0, 10))
            
            newLabel = Label(profSettIf, text='Enter Your New Password:', font=('Verdana', 12))
            newLabel.pack(pady=(0, 5))

            newEntry = Entry(profSettIf, show='*', font=('Verdana', 12), width=25, bd=2)
            newEntry.pack(pady=(0, 10))
            
            submit = Button(profSettIf, text='Submit', font=('Verdana', 12), bg='olive', cursor='hand2', command=submitPassword, bd=2)
            submit.pack()
            
            
        #Account Settings Main

        name = Button(profSettIf, text='Change Your Name', font=('Verdana', 12), cursor='hand2', command=setName, bd=2)
        name.pack(pady=15)
        
        pwrd = Button(profSettIf, text='Change Your Password', font=('Verdana', 12), cursor='hand2', command=setPassword, bd=2)
        pwrd.pack(pady=15)
        
        leave = Button(profSettIf, text='Exit Settings', font=('Verdana', 12), cursor='hand2', command=closeSettWindow, bd=2)
        leave.pack(pady=15)

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
        confirm = messagebox.askyesno("Confirm Withdrawal", "Are you sure you want to request a withdrawal?")
        if confirm:
            query = 'INSERT INTO withdrawals VALUES (%s, %s)'
            connect.cursor.execute(query, (self.id, 'Υπο εξέταση'))
            connect.conn.commit()
            messagebox.showinfo('Success!', 'Your request has been sent to your Employee')
        else:
            pass
    
    
    def view_assigned_task(self, task):
        taskwin = Tk()
        taskwin.geometry('400x400')
        taskwin.title("Task Details")
        taskwin.config(bg="#bdc1b2")

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
            

        task_details = Label(taskwin, text=f'Task Title: {task.title}\n\nDescription: {task.description}\n\nDeadline: {task.deadline}\n', font=('Verdana', 15))
        task_details.pack(anchor='center', pady=40)

        if task.completed == 'Uncompleted':
            complete = Button(taskwin, text='Complete this Task', bg='green', fg='white', font=('Verdana', 15), border=2, cursor='hand2', command=mark_task_complete)
            complete.pack(anchor='center',pady=20)
        else:
           completed = Label(taskwin, text='This Task is Completed!', font=('Verdana', 15), fg='green')
           completed.pack(anchor='center', pady=10)
           unmark = Button(taskwin, text='Unmark Completed Task', font=('Verdana', 13), cursor='hand2', fg='orange', command=unmark_completed_task)
           unmark.pack(anchor='center',pady=20)
           

           taskwin.mainloop()

    def view_meeting_schedule(self, meeting):
        meetwin = Tk()
        meetwin.geometry('400x400')
        meetwin.title('Meeting Details')
        meetwin.config(bg="#bdc1b2")

        def attend_meeting(meeting):
            self.meetingSchedule.append(meeting)
            meetwin.destroy()

        def request_not_attend_meeting(meeting):
            self.meetingSchedule.remove(meeting)
            meetwin.destroy()
            

        meeting_details = Label(meetwin, text=f'Meeting Title: {meeting.meetingName}\n\nDescription: {meeting.date}\n\n', font=('Verdana', 15))
        meeting_details.pack(anchor='center', pady=40)

        if meeting in self.meetingSchedule:
            notattend = Button(meetwin, text='Not Attend', fg='red', font=('Verdana', 12), cursor='hand2', command=lambda:request_not_attend_meeting(meeting)).pack()
            notattend.pack(anchor='center',pady=20)
        else:
            notattendlabel = Label(meetwin, text="You're not attending this meeting.", font=('Verdana', 14), fg='red').pack(pady=15)
            unmark = Button(meetwin, text='Click to Attend', font=('Verdana, 13'), cursor='hand2', fg='orange', command= lambda:attend_meeting(meeting)).pack()
            unmark.pack(anchor='center',pady=20)
    
    def request_leave(self):
        leavewin = Tk()
        leavewin.geometry('400x400')
        leavewin.title('Leave Request')
        leavewin.config(bg="#bdc1b2")

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
                
                if len(apprdates_res) == 0:
                    submitleave = 'INSERT INTO leaverequests VALUES (null, %s, %s, %s, %s, %s)'
                    connect.cursor.execute(submitleave, (start, end, 'Υπο εξέταση', self.id, name))
                    connect.conn.commit()
                    messagebox.showinfo('Submitted', f"Your leave request ({start} - {end}) has been submitted!")
                    leavewin.destroy()
                    
                else:
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
            

        label = Label(leavewin, text="Submit Your Leave Request", font=('Verdana', 15)).pack(pady=(20,10))

        namelabel = Label(leavewin, text='Request Name:', font=('Verdana', 12))
        namelabel.pack(pady=(10,5))
        name = Entry(leavewin, font=('Verdana', 12), width=30, bd=2)
        name.pack(pady=(0,15), padx=10)

        sdatelabel = Label(leavewin, text='Start Date:', font=('Verdana', 12))
        sdatelabel.pack(pady=(10,5))
        start = DateEntry(leavewin, width=17, background="#008080", foreground="white", borderwidth=2)
        start.pack(pady=(0,15), padx=10)

        edatelabel = Label(leavewin, text='End Date:', font=('Verdana', 12))
        edatelabel.pack(pady=(10,5))
        end = DateEntry(leavewin, width=17, background="#008080", foreground="white", borderwidth=2)
        end.pack(pady=(0,30), padx=10)

        submit = Button(leavewin, text='Submit', font=('Verdana', 12), fg='white',bg='#008080', cursor='hand2', border=2, command=lambda: submit_leave_request(start.get_date(), end.get_date(), name.get()))
        submit.pack(pady=(0, 10))
        
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

