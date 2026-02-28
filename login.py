from tkinter import *
from tkinter import messagebox
import sqlite3
import dashboard
from helper_functions import createLabel, createEntry, createButton

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")
        
        #Variables
        self.var_email = StringVar()
        self.var_password = StringVar()
        
        #Login Frame
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=275, y=150, width=800, height=450)
        
        #Title
        createLabel(login_frame, "Login to the IMS", 250, 30, font_size=30, fg="blue", bold=True)
        
        #Email
        createLabel(login_frame, "Email", 200, 120, bg="white", fg="gray", bold=True)
        createEntry(login_frame, self.var_email, 200, 160, width=400, height=35, font="times new roman", bg="lightgray")
        
        #Password
        createLabel(login_frame, "Password", 200, 210, bg="white", fg="gray", bold=True)
     
        createEntry(login_frame, self.var_password, 200, 250, width=400, height=35, font="times new roman", bg="lightgray")
        
        #Login Button
        createButton(login_frame, "Log In", self.login, "light blue", 310, 320, 180, 40, font="times new roman", fg="white")

    
    #Verifying credentials against employee table
    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            #Querying the employee table for matching credentials
            cur.execute(
                "SELECT * FROM employee WHERE email=? AND pass=?",
                (self.var_email.get(), self.var_password.get())
            )
            row = cur.fetchone()
            
            if row is None:
                messagebox.showerror("Error", "Invalid email or password", parent=self.root)
            else:
                #Success!!
                messagebox.showinfo("Login", "Login successful!")
                #Closing the login window and opening dashboard
                self.root.destroy()
                self.open_dashboard()
                con.close()
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
            con.close()
            
    

    
    #Opening the main dashboard after successful login
    #and setting the dashboard as the new main window
    def open_dashboard(self):
        root = Tk()
        obj = dashboard.IMS(root)
        root.mainloop()


if __name__ == "__main__":
    root = Tk()
    obj = Login_System(root)
    root.mainloop()
