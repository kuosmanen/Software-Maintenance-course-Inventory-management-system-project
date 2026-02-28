from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import sqlite3
import os

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass

from helper_functions import logout, createButton

# ------------------ BASE PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
BILL_DIR = os.path.join(BASE_DIR, "bill")

os.makedirs(BILL_DIR, exist_ok=True)
# ---------------------------------------------------

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # ------------- title --------------
        self.icon_title = PhotoImage(file=os.path.join(IMAGE_DIR, "logo1.png"))
        title = Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("times new roman", 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20
        ).place(x=0, y=0, relwidth=1, height=70)

        # ------------ logout button -----------
        createButton(self.root, "Logout", lambda: logout(self.root), "yellow", 1150, 10, 150, 50, font="times new roman", bold=True, fg="black")

        # ------------ clock -----------------
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
            font=("times new roman", 15),
            bg="#4d636d", fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ---------------- left menu ---------------
        self.MenuLogo = Image.open(os.path.join(IMAGE_DIR, "menu_im.png"))
        self.MenuLogo = self.MenuLogo.resize((200, 200))
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        lbl_menu = Label(
            LeftMenu, text="Menu",
            font=("times new roman", 20),
            bg="#009688"
        ).pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file=os.path.join(IMAGE_DIR, "side.png"))

        #All buttons are created with a helper funciton
        self.createDashboardButton(LeftMenu, "Employee", self.employee)
        self.createDashboardButton(LeftMenu, "Supplier", self.supplier)
        self.createDashboardButton(LeftMenu, "Category", self.category)
        self.createDashboardButton(LeftMenu, "Products", self.product)
        self.createDashboardButton(LeftMenu, "Sales", self.sales)
        self.createDashboardButton(LeftMenu, "Exit", self.root.destroy)

        # ----------- content ----------------
        self.lbl_employee = self.createStatLabel("Total Employee\n{ 0 }", "#33bbf9", 300, 120)
        self.lbl_supplier = self.createStatLabel("Total Supplier\n{ 0 }", "#ff5722", 650, 120)
        self.lbl_category = self.createStatLabel("Total Category\n{ 0 }", "#009688", 1000, 120)
        self.lbl_product = self.createStatLabel("Total Product\n{ 0 }", "#607d8b", 300, 300)
        self.lbl_sales = self.createStatLabel("Total Sales\n{ 0 }", "#ffc107", 650, 300)

        # ------------ footer -----------------
        lbl_footer = Label(
            self.root,
            text="IMS-Inventory Management System",
            font=("times new roman", 12),
            bg="#4d636d", fg="white"
        ).pack(side=BOTTOM, fill=X)

        self.update_content()

    # -------------- functions ----------------

    #The helper function to create the buttons
    def createDashboardButton(self, parent, text, command):
        Button(
            parent, text=text, command=command,
            image=self.icon_side, compound=LEFT,
            padx=5, anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white", bd=3, cursor="hand2"
        ).pack(side=TOP, fill=X)

    #function to create the labels for the stats
    def createStatLabel(self, text, bg_color, x, y):
        label = Label(
            self.root, text=text,
            bd=5, relief=RIDGE, bg=bg_color,
            fg="white", font=("goudy old style", 20, "bold")
        )
        label.place(x=x, y=y, height=150, width=300)
        return label

    #another helper function. Opens a new window when a menu button is clicked
    def openWindow(self, window_class):
        self.new_win = Toplevel(self.root)
        self.new_obj = window_class(self.new_win)

    def employee(self):
        self.openWindow(employeeClass)

    def supplier(self):
        self.openWindow(supplierClass)

    def category(self):
        self.openWindow(categoryClass)

    def product(self):
        self.openWindow(productClass)

    def sales(self):
        self.openWindow(salesClass)

    #Function to update the stat counts on the dashboard
    def updateStatCount(self, cur, tableName, label, display_name):
        cur.execute(f"select * from {tableName}")
        count = len(cur.fetchall())
        label.config(text=f"Total {display_name}\n[ {count} ]")

    def update_content(self):
        con = sqlite3.connect(database=os.path.join(BASE_DIR, 'ims.db'))
        cur = con.cursor()

        try:
            self.updateStatCount(cur, "product", self.lbl_product, "Product")
            self.updateStatCount(cur, "category", self.lbl_category, "Category")
            self.updateStatCount(cur, "employee", self.lbl_employee, "Employee")
            self.updateStatCount(cur, "supplier", self.lbl_supplier, "Supplier")

            bill = len(os.listdir(BILL_DIR))
            self.lbl_sales.config(text=f"Total Sales\n[ {bill} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}"
            )

            self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            pass
