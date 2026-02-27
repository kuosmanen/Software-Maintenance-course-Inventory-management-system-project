from tkinter import Label, Entry, Button, Frame, Scrollbar, VERTICAL, HORIZONTAL, BOTTOM, RIGHT, X, Y, RIDGE, BOTH
from tkinter import ttk


#Helper functions for creating UI elements with the same styling
#also helps eliminate code repetition


#Create a styled label
def createLabel(root, text, x, y, font_size=15):
    Label(root, text=text, font=("goudy old style",font_size), bg="white").place(x=x, y=y)

#Create a styled entry
def createEntry(root, textvariable, x, y):
    Entry(root, textvariable=textvariable, font=("goudy old style",15), bg="lightyellow").place(x=x, y=y, width=180)

#Create a styled button
def createButton(root, text, command, bg, x, y, width, height):
    Button(root, text=text, command=command, font=("goudy old style",15), bg=bg, fg="white", cursor="hand2").place(x=x, y=y, width=width, height=height)


#Create a table with scrollbars
def createTableWithScrollbars(root, columns, x, y, width=None, height=None, relwidth=None):
    #frame
    frame = Frame(root, bd=3, relief=RIDGE)
    frame.place(x=x, y=y, width=width, height=height, relwidth=relwidth)
    
    #scrollbars
    scrolly = Scrollbar(frame, orient=VERTICAL)
    scrollx = Scrollbar(frame, orient=HORIZONTAL)
    
    #Treeview
    table = ttk.Treeview(frame, columns=columns,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill= Y)
    scrollx.config(command=table.xview)
    scrolly.config(command=table.yview)
    
    return frame, table

#Configure table columns
def configureTableColumns(table, columns_config, bind):
    for col_id, col_text, col_width in columns_config:
        table.heading(col_id, text=col_text)
        table.column(col_id, width=col_width)
    
    table["show"]="headings"

    table.pack(fill=BOTH,expand=1)
    table.bind("<ButtonRelease-1>",bind)
