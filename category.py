from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
from helper_functions import createLabel, createEntry, createTableWithScrollbars, configureTableColumns, createButton

class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ variables -------------
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #--------------- title ---------------------
        #this uses pack so cant use helper function
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        createLabel(self.root,"Enter Category Name", 50, 100, font_size=30)
        createEntry(self.root, self.var_name, 50, 170, width=300, font_size=18)

        createButton(self.root, "ADD", self.add, "#4caf50", 360, 170, 150, 30)
        createButton(self.root, "Delete", self.delete, "red", 520, 170, 150, 30)

        #------------ category details -------------
        columns_config = [
            ("cid", "C ID", 90),
            ("name", "Name", 100)
        ]
        
        cat_frame, self.CategoryTable = createTableWithScrollbars(self.root, ("cid", "name"), 700, 100, width=380, height=100)
        
        configureTableColumns(self.CategoryTable, columns_config, self.get_data)
        self.show()

        #----------------- images ---------------------
        self.im1=Image.open("Inventory-Management-System/images/cat.jpg")
        self.im1=self.im1.resize((500,250))
        self.im1=ImageTk.PhotoImage(self.im1)
        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)

        self.im2=Image.open("Inventory-Management-System/images/category.jpg")
        self.im2=self.im2.resize((500,250))
        self.im2=ImageTk.PhotoImage(self.im2)
        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=580,y=220)
#----------------------------------------------------------------------------------
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category Name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already present",parent=self.root)
                else:
                    cur.execute("insert into category(name) values(?)",(
                        self.var_name.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    
    def clear(self):
        self.var_name.set("")
        self.show()

    def get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])
    
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Category name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Category Name",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.clear()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")



if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()