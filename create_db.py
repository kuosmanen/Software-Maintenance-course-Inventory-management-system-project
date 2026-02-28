import sqlite3

def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
    con.commit()

    #adding a default admin user
    #passwords are in plain text because they are also so in the original employee table
    cur.execute("SELECT * FROM employee WHERE email=?",( "admin@admin.com",))
    if not cur.fetchall():
        cur.execute("INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES(?,?,?,?,?,?,?,?,?,?)",(
            "Admin",
            "admin@admin.com",
            "Other",
            "+358999999999",
            "01/01/2000",
            "28/02/2026",
            "123456", #this is the password
            "Admin",
            "My house",
            "999999"
        ))
        con.commit()

    #adding an employee user for testing
    cur.execute("SELECT * FROM employee WHERE email=?",( "employee@employee.com",))
    if not cur.fetchall():
        cur.execute("INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES(?,?,?,?,?,?,?,?,?,?)",(
            "Employee",
            "employee@employee.com",
            "Other",
            "+358888888888",
            "01/01/2010",
            "28/02/2026",
            "123456", #same password
            "Employee",
            "Their house",
            "5000"
        ))
        con.commit()


    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text, Supplier text,name text,price text,qty text,status text)")
    con.commit()


create_db()