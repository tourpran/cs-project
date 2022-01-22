#!/usr/bin/python3
from tkinter import *
from tkinter.font import names
import tkinter.messagebox as tkMessageBox
import mysql.connector
from PIL import ImageTk, Image
from functools import partial

'''
query statements used:
* SELECT
* UPDATE
* INSERT
* CREATE
'''


global id
id= 0

# Tkinter functions:
def login():
    global screen1
    screen1 = Toplevel(root)
    screen1.title("login")
    screen1.geometry("900x900")

    global username 
    username = StringVar()
    global passwd
    passwd = StringVar()

    Label(screen1, text="").pack()
    Label(screen1, text="LOGIN", font= ('Helvetica 18 bold')).pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Username").pack()
    Entry(screen1, textvariable=username).pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Password").pack()
    Entry(screen1, textvariable=passwd, show="*").pack()
    Label(screen1, text="").pack()
    Button(screen1, text="login", command=login_user).pack()

def login_failed():
    screen1 = Toplevel(root)
    screen1.title("login failed")
    screen1.geometry("800x200")
    Label(screen1, text="").pack()
    Label(screen1, text="Your username and password is wrong check again.").pack()

def fake_user():
    screen1.destroy()
    global screen
    screen = Toplevel(root)
    screen.title("fake user")
    screen.geometry("900x200")

    Label(screen, text="Username already found in Database.").pack()

def register():
    global screen1
    screen1 = Toplevel(root)
    screen1.title("register")
    screen1.geometry("900x900")

    global username 
    username = StringVar()
    global passwd
    passwd = StringVar()
    global address
    address = StringVar()

    Label(screen1, text="REGISTER").pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Username").pack()
    Entry(screen1, textvariable=username).pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Password").pack()
    Entry(screen1, textvariable=passwd, show="*").pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Address").pack()
    Entry(screen1, textvariable=address).pack()
    Label(screen1, text="").pack()
    Button(screen1, text="register", command=register_user).pack()
    
def shop():
    for widgets in root.winfo_children():
      widgets.destroy()
    
    Label(root, text="").pack()
    Label(root, text="Shop Items", font=('Helvetica', 18, 'bold')).pack()
    Label(root, text="").pack()
    items = get_items()
    mycursor = db.cursor()
    print(items)
    for product in items:
        print(product)
        mycursor.execute(f"select * from {username_info} where name='{product[1]}'")
        qty = mycursor.fetchall()
        print(qty)
        if(qty == []):
            qty = []
            qty.append([0,0,0,0])
        Label(root, text=f"{product[1]}({product[3]}) - {qty[0][2]}").pack()
        img = Image.open(f"/home/tourpran/cs-project/images/{product[1]}.png")
        img = img.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        label = Label(root, image = img)
        label.image = img
        label.pack()

        Button(root, text="add", width=10, command=partial(add_product, f"{product[1]}", f"{product[3]}")).pack()
        Button(root, text="remove", width=10, command=partial(remove_product, f"{product[1]}", f"{product[3]}")).pack()    
        Label(text="").pack()
    
    Button(root, text="Total", command=bill).pack()

def bill():
    global total 
    total = 0

    for widgets in root.winfo_children():
        widgets.destroy()

    Label(root, text="").pack()
    Label(root, text="Totaling your items:", font=('Helvetica', 18, 'bold')).pack()
    Label(root, text="").pack()
    
    mycursor = db.cursor()
    mycursor.execute(f"select * from {username_info}")
    items = mycursor.fetchall()

    Label(root, text="Product name"+" "*(8)+"Quantity"+" "*(12)+"Price").pack()
    Label(root, text="").pack()
    for product in items:
        Label(root, text=f"{product[1]}"+" "*(25-len(product[1]))+f"{product[2]}"+" "*(20-len(str(product[2])))+f"{product[3]}").pack()
        Label(root, text="").pack()
        total += product[2]*product[3]

    Label(root, text="--------------").pack()
    Label(root, text=f"Grand total: {total}").pack()
    Label(root, text="--------------").pack()
    Button(root, text="shop", command=shop).pack()

def main_screen():
    global root 
    root = Tk()
    root.geometry("900x900")
    root.title("Retail Application")
    
    Label(text="").pack()
    img = Image.open("login.png")
    img = img.resize((100, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    label = Label(root, image = img)
    label.pack()

    Label(text="").pack()
    Button(root, text="Login", command=login).pack()
    Label(text="").pack()
    Button(root, text="Signup", command=register).pack()

    root.mainloop()

# Sql functions:
def add_product(name, price):
    global id
    mycursor = db.cursor()
    mycursor.execute(f"select * from {username_info} where name='{name}'")
    mycursor.fetchall()
    if mycursor.rowcount == 0:
        id += 1
        mycursor.execute(f"insert into {username_info} values ({id}, '{name}', 1, {price})")
        db.commit() 
    else:
        mycursor.execute(f"update {username_info} set qty=qty+1 where name='{name}'")
        db.commit()
    shop()
    
def remove_product(name, price):
    mycursor = db.cursor()
    mycursor.execute(f"select * from {username_info} where name='{name}' and qty!=0")
    mycursor.fetchall()
    if mycursor.rowcount == 0:
        return 0
    else:
        mycursor.execute(f"update {username_info} set qty=qty-1 where name='{name}'")
        db.commit()
    shop()

def mysqlconnect():
    global db
    db = mysql.connector.connect(user = 'tourpran', host = 'localhost', password= "password", database = 'retailapp')
    print("Connected")

def get_items():
    mycursor = db.cursor()
    mycursor.execute("select * from products")
    record = mycursor.fetchall()
    return record

def initialise():
    mycursor = db.cursor()
    try:
        mycursor.execute("create table users (name varchar(255), password varchar(255), address varchar(255))")
        mycursor.execute("create table products(id int, name varchar(100), description varchar(100), price int)")

        db.commit()
    except:
        pass

def register_user():
    username_info = username.get()
    password_info = passwd.get()
    address_info = address.get()
    mycursor = db.cursor()
    mycursor.execute(f"SELECT * FROM users where name='{username_info}'")
    mycursor.fetchall()
    if mycursor.rowcount != 0:
        fake_user()
        return 0
        
    mycursor.execute(f"INSERT INTO users (name, password, address) VALUES ('{username_info}', '{password_info}', '{address_info}')")
    db.commit()
    screen1.destroy()

def login_user():
    global username_info
    username_info = username.get()
    password_info = passwd.get()
    mycursor = db.cursor()
    mycursor.execute(f"SELECT * FROM users WHERE name='{username_info}' and password='{password_info}'")
    mycursor.fetchall()
    if mycursor.rowcount == 0:
        screen1.destroy()
        login_failed()
    else:
        try:
            mycursor = db.cursor()
            mycursor.execute(f"create table {username_info} (id int, name varchar(100), qty int, price int)")
        except:
            pass
        shop()

# Initialisation
mysqlconnect()
# initialise()
main_screen()
    
