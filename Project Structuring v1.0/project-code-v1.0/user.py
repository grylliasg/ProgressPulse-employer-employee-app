from tkinter import *
from tkinter import Tk, Label, Button, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import connect


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