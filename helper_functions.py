from tkinter import Label, Entry, Button, Frame, Scrollbar, VERTICAL, HORIZONTAL, BOTTOM, RIGHT, X, Y, RIDGE, BOTH
from tkinter import ttk


#Helper functions for creating UI elements with the same styling
#also helps eliminate code repetition


#Create a styled label
def createLabel(root, text, x, y, font_size=15, font="goudy old style", bg="white", fg="black", bold=False):
    if bold:
        final_font = (font, font_size, "bold")
    else:
        final_font = (font, font_size)
    Label(root, text=text, font=final_font, bg=bg, fg=fg).place(x=x, y=y)

#Create a styled entry
def createEntry(root, textvariable, x, y, width=180, height=None, font_size=15, font="goudy old style", bg="lightyellow", fg="black", state="normal"):
    Entry(root, textvariable=textvariable, font=(font, font_size), bg=bg, fg=fg, state=state).place(x=x, y=y, width=width, height=height)

#Create a styled button
def createButton(root, text, command, bg, x, y, width, height, font_size=15, font="goudy old style", bold=False, fg="white"):
    if bold:
        final_font = (font, font_size, "bold")
    else:
        final_font = (font, font_size)
    Button(root, text=text, command=command, font=final_font, bg=bg, fg=fg, cursor="hand2").place(x=x, y=y, width=width, height=height)


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
