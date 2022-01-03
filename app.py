#!/usr/bin/python3
from tkinter import *
from tkinter.font import names
import tkinter.messagebox as tkMessageBox
import mysql.connector
from PIL import ImageTk, Image

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

    Label(screen1, text="LOGIN").pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Username").pack()
    Entry(screen1, textvariable=username).pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Password").pack()
    Entry(screen1, textvariable=passwd).pack()
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
    Entry(screen1, textvariable=passwd).pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Address").pack()
    Entry(screen1, textvariable=address).pack()
    Label(screen1, text="").pack()
    Button(screen1, text="register", command=register_user).pack()

def shop():
    for widgets in root.winfo_children():
      widgets.destroy()
    Label(root, text="Shop items").pack()

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
def mysqlconnect():
    global db
    db = mysql.connector.connect(user = 'pranav', host = 'localhost', password= "password", database = 'retailapp')
    print("Connected")

def initialise():
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE users (name VARCHAR(255), password VARCHAR(255), address VARCHAR(255))")

def register_user():
    username_info = username.get()
    password_info = passwd.get()
    address_info = address.get()
    mycursor = db.cursor()
    mycursor.execute(f"SELECT * FROM users where name='{username_info}'")
    mycursor.fetchall()
    if mycursor.rowcount != 0:
        fake_user()
    mycursor.execute(f"INSERT INTO users (name, password, address) VALUES ('{username_info}', '{password_info}', '{address_info}')")
    db.commit()
    screen1.destroy()

def login_user():
    username_info = username.get()
    password_info = passwd.get()
    mycursor = db.cursor()
    mycursor.execute(f"SELECT * FROM users WHERE name='{username_info}' and password='{password_info}'")
    mycursor.fetchall()
    if mycursor.rowcount == 0:
        screen1.destroy()
        login_failed()
    else:
        shop()

# Initialisation
mysqlconnect()
main_screen()
    