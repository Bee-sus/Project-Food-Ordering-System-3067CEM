import sqlite3
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
from tkinter import ttk, Menu
from tkinter import Tk, StringVar, Toplevel, Frame, Label, Entry, Button
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from fpdf import FPDF  #generating pdf documents
from tkinter import filedialog
import os
import datetime
from datetime import datetime as dt

root = Tk()
root.title("Register and Login System")
root.geometry("1920x1080+0+0")  # window size and position
root.config()  # used to customize the window (bg colour, title)
root.configure(bg="#E6D8AD")

# Constants
WIDTH = 800
HEIGHT = 700

# Create variables
USERNAME_LOGIN = StringVar()
PASSWORD_LOGIN = StringVar()
USERNAME_REGISTER = StringVar()
PASSWORD_REGISTER = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()
ADDRESS = StringVar()
PHONE_NUMBER = StringVar()
EMAIL_ADDRESS = StringVar()
DATE_OF_BIRTH = StringVar()

conn = None  # connection to database
cursor = None  # use to execute the sql queries and fetch results from db


def Database():
    global conn, cursor
    conn = sqlite3.connect("db_FOOD_ORDERING_SYSTEM.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `USER` "
        "(USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "FIRST_NAME TEXT (100) NOT NULL, "
        "LAST_NAME TEXT (100) NOT NULL, "
        "USERNAME TEXT (100) NOT NULL, "
        "ADDRESS TEXT (150) NOT NULL, "
        "PHONE_NUMBER TEXT (50) NOT NULL UNIQUE, "
        "EMAIL_ADDRESS TEXT (50) NOT NULL UNIQUE, "
        "DATE_OF_BIRTH TEXT (25) NOT NULL,  "
        "PASSWORD TEXT (50) NOT NULL) ")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `MENU` "
        "(FOOD_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "FOOD_NAME TEXT (75) NOT NULL, "
        "FOOD_DESCRIPTION TEXT (75) NOT NULL, "
        "FOOD_CATEGORY TEXT (50) NOT NULL, "
        "FOOD_QUANTITY TEXT (50) NOT NULL, "
        "FOOD_PRICE REAL (50) NOT NULL, "
        "IMAGE_PATH TEXT (150) NOT NULL)")

def LoginForm():
    global LoginFrame, lbl_result, loginframe
    loginframe = Toplevel()
    loginframe.geometry("1920x1080")
    loginframe.configure(bg="#E6D8AD")
    loginframe.title("Login")
    LoginFrame = Frame(loginframe)
    LoginFrame.configure(bg="#E6D8AD")
    LoginFrame.pack(side='top', pady=80)
    LoginFrame.columnconfigure(0,weight=1)
    LoginFrame.columnconfigure(1, weight=1)
    LoginFrame.columnconfigure(2, weight=1)
    LoginFrame.columnconfigure(3, weight=1)
    LoginFrame.rowconfigure(0,weight=1)
    LoginFrame.rowconfigure(1, weight=1)
    LoginFrame.rowconfigure(2, weight=1)
    LoginFrame.rowconfigure(3, weight=1)
    LoginFrame.rowconfigure(4, weight=1)
    LoginFrame.rowconfigure(5, weight=1)

    background = Image.open(r"C:\Users\tanho\PycharmProjects\ALL project\image\Screenshot_20240630-203500_Chrome.jpg")
    width, height = 500, 500
    resized_background = background.resize((width, height), Image.LANCZOS)
    restaurant_photo = ImageTk.PhotoImage(resized_background)
    photo_label = tk.Label(LoginFrame, image=restaurant_photo)
    photo_label.image = restaurant_photo
    photo_label.grid(column=0, row=0, columnspan=2, rowspan=6, sticky='W')

    lbl_title = Label(LoginFrame, text="Login:", font=('Arial', 20, 'bold'), bd=18)
    lbl_title.configure(bg="#E6D8AD")
    lbl_title.grid(column=2,row=0, columnspan=2)

    lbl_username = Label(LoginFrame, text="Username:", font=('Arial', 16), bd=18)
    lbl_username.configure(bg="#E6D8AD")
    lbl_username.grid(column=2,row=1)

    lbl_password = Label(LoginFrame, text="Password:", font=('Arial', 16), bd=18)
    lbl_password.configure(bg="#E6D8AD")
    lbl_password.grid (column=2, row=2)

    username = Entry(LoginFrame, font=('Arial', 16), textvariable=USERNAME_LOGIN, width=15)
    username.grid(column=3, row=1)

    password = Entry(LoginFrame, font=('Arial', 16), textvariable=PASSWORD_LOGIN, width=15, show="*")
    password.grid(column=3, row=2)

    btn_login = Button(LoginFrame, text="Login", font=('Arial', 16), width=20, command=Login, bg='#dbac1a', fg='white',
                       relief='raised')
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#E6D8AD"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#dbac1a"))
    btn_login.grid(column=2, row=4, columnspan=2, pady=5)

    lbl_text = Label(LoginFrame, text="Not a member?", font=('Arial', 14))
    lbl_text.configure(bg="#E6D8AD")
    lbl_text.grid(column=2, row=5, columnspan=2)

    lbl_register = Label(LoginFrame, text="Register Now", fg="#96750e", font=('Arial', 12))
    lbl_register.configure(bg="#E6D8AD")
    lbl_register.bind('<Enter>', lambda event, label=lbl_register: label.config(font=('Arial', 12, 'underline')))
    lbl_register.bind('<Leave>', lambda event, label=lbl_register: label.config(font=('Arial', 12)))
    lbl_register.bind('<Button-1>', ToggleToRegister)
    lbl_register.grid(column=2, row=6, columnspan=2)

def RegisterForm():
    global RegisterFrame, lbl_result2, confirm_password_entry, registerframe
    registerframe = Toplevel()
    registerframe.geometry("1920x1080")
    registerframe.configure(bg="#E6D8AD")
    registerframe.title('Register')
    image = (Image.open(
        r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1) - Copy.png"))
    resized_bgimage = image.resize((1920, 1080), Image.LANCZOS)
    backgroundimage = ImageTk.PhotoImage(resized_bgimage)
    backgroundimage.image = backgroundimage
    canvas3 = Canvas(registerframe)
    canvas3.pack(fill="both", expand=True)
    canvas3.create_image(0, 0, image=backgroundimage,
                         anchor="nw")
    RegisterFrame = Frame(canvas3)
    RegisterFrame.configure(bg="#E6D8AD")
    RegisterFrame.pack(side='top', pady=60)
    RegisterFrame.columnconfigure(0, weight=1)
    RegisterFrame.columnconfigure(1, weight=1)
    RegisterFrame.columnconfigure(2, weight=1)
    RegisterFrame.columnconfigure(3, weight=1)

    lbl_login = Label(RegisterFrame, text="Click to Login",  bg= "#E6D8AD", fg="#96750e", font=('arial', 12))
    lbl_login.bind('<Enter>', lambda event, label=lbl_login: label.config(font=('arial', 12, 'underline')))
    lbl_login.bind('<Leave>', lambda event, label=lbl_login: label.config(font=('arial', 12)))
    lbl_login.grid(row=13, column=2, columnspan=2)
    lbl_login.bind('<Button-1>', ToggleToLogin)

    lbl_result2 = Label(RegisterFrame, text="Registration Form:", bg= "#E6D8AD", font=('Arial', 20, 'bold'), bd=18)
    lbl_result2.grid(row=1, column=2, columnspan=2)


    lbl_firstname = Label(RegisterFrame, text="First Name:",  bg= "#E6D8AD", font=('Arial', 14), bd=18)
    lbl_firstname.grid(row=2, column=1)

    lbl_lastname = Label(RegisterFrame, text="Last Name:",  bg= "#E6D8AD", font=('Arial', 14), bd=18)
    lbl_lastname.grid(row=3, column=1)

    lbl_username = Label(RegisterFrame, text="Username:",  bg= "#E6D8AD", font=('Arial', 14), bd=18)
    lbl_username.grid(row=4, column=1)

    lbl_address = Label(RegisterFrame, text="Address:",  bg= "#E6D8AD", font=('Arial', 14), bd=18)
    lbl_address.grid(row=5,column=1)

    lbl_phone_number = Label(RegisterFrame, text="Phone Number:",  bg= "#E6D8AD", font=('Arial', 14), bd=18)
    lbl_phone_number.grid(row=6,column=1)

    lbl_email_address = Label(RegisterFrame, text="Email Address:",  bg= "#E6D8AD", font=('Arial', 14), bd=18)
    lbl_email_address.grid(row=2,column=3)

    lbl_date_of_birth = Label(RegisterFrame, text="Date of Birth:",  bg= "#E6D8AD", font=('Arial', 14), bd=18)
    lbl_date_of_birth.grid(row=3,column=3)

    lbl_password = Label(RegisterFrame, text="Password:",  bg= "#E6D8AD", font=('Arial', 14), bd=18)
    lbl_password.grid(row=4,column=3)

    lbl_confirm_password = Label(RegisterFrame, text="Confirm Password:",  bg= "#E6D8AD", font=('Arial', 14), bd=18)
    lbl_confirm_password.grid(row=5,column=3)

    #Entry frames

    firstname = Entry(RegisterFrame, font=('Arial', 14), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=2, column=2)

    lastname = Entry(RegisterFrame, font=('Arial', 14), textvariable=LASTNAME, width=15)
    lastname.grid(row=3, column=2)

    username = Entry(RegisterFrame, font=('Arial', 14), textvariable=USERNAME_REGISTER, width=15)
    username.grid(row=4, column=2)

    address = Entry(RegisterFrame, font=('Arial', 14), textvariable=ADDRESS, width=15)
    address.grid(row=5, column=2)

    phone_number = Entry(RegisterFrame, font=('Arial', 14), textvariable=PHONE_NUMBER, width=15)
    phone_number.grid(row=6, column=2)

    email_address = Entry(RegisterFrame, font=('Arial', 14), textvariable=EMAIL_ADDRESS, width=15)
    email_address.grid(row=2, column=4)

    date_of_birth = Entry(RegisterFrame, font=('Arial', 14), textvariable=DATE_OF_BIRTH, width=15)
    date_of_birth.grid(row=3, column=4)

    password = Entry(RegisterFrame, font=('Arial', 14), textvariable=PASSWORD_REGISTER, width=15, show="*")
    password.grid(row=4, column=4)

    confirm_password_entry = Entry(RegisterFrame, font=('Arial', 14), width=15, show="*")
    confirm_password_entry.grid(row=5, column=4)

    btn_login = Button(RegisterFrame, text="Register", font=('arial', 15), width=20, command=Register, bg='#dbac1a',fg='white', relief='raised')
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#E6D8AD"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#dbac1a"))
    btn_login.grid(row=11,  column=2, columnspan=2, pady=20)
    btn_login.config(anchor='center')

def ToggleToLogin(event=None):    #switching from register to login page.
    if registerframe is not None:
        registerframe.destroy()
    LoginForm()
    root.withdraw()

def ToggleToRegister(event=None): #switching the interface from login to register after user click the register link
    if loginframe is not None:     #if login form is display, then need to deleted and switch to registration form
        loginframe.destroy()
    RegisterForm()

def edit_profile():
    def Database():
        global conn, cursor
        conn = sqlite3.connect("db_FOOD_ORDERING_SYSTEM.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `USER` "
            "(USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            "FIRST_NAME TEXT (100) NOT NULL, "
            "LAST_NAME TEXT (100) NOT NULL, "
            "USERNAME TEXT (100) NOT NULL, "
            "ADDRESS TEXT (150) NOT NULL, "
            "PHONE_NUMBER TEXT (50) NOT NULL UNIQUE, "
            "EMAIL_ADDRESS TEXT (50) NOT NULL UNIQUE, "
            "DATE_OF_BIRTH TEXT (25) NOT NULL,  "
            "PASSWORD TEXT (50) NOT NULL)"
        )
        conn.commit()

    # Initialize the database
    Database()


    # Function to open the edit profile window
    def open_edit_profile_window():
        edit_window = Toplevel()
        edit_window.title("Edit Profile")
        edit_window.geometry("1920x1080")  # Set the size of the new window
        edit_window.configure(bg='#e6d8ad')
        image = (Image.open(
            r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1) - Copy.png"))
        resized_bgimage1 = image.resize((1920, 1080), Image.LANCZOS)
        backgroundimage1 = ImageTk.PhotoImage(resized_bgimage1)
        backgroundimage1.image = backgroundimage1
        canvas6 = Canvas(edit_window)
        canvas6.pack(fill="both", expand=True)
        canvas6.create_image(0, 0, image=backgroundimage1,
                             anchor="nw")


        # Define StringVar variables for profile fields
        myid = StringVar()
        first_name = StringVar()
        last_name = StringVar()
        username = StringVar()
        address = StringVar()
        phone_number = StringVar()
        email_address = StringVar()
        date_of_birth = StringVar()
        password = StringVar()

        # Create Entry widgets for the profile fields
        Label(canvas6, text="Edit Profile", font=('Arial',16), bg='#e6d8ad').place(x=920, y=10)

        Label(canvas6, text="First Name", font=('Arial',16), bg='#e6d8ad').place(x=740, y=60)
        first_name_entry = Entry(canvas6, textvariable=first_name, font=('Arial',16))
        first_name_entry.place(x=940, y=60)

        Label(canvas6, text="Last Name", font=('Arial',16), bg='#e6d8ad').place(x=740, y=110)
        last_name_entry = Entry(canvas6, textvariable=last_name, font=('Arial',16))
        last_name_entry.place(x=940, y=110)

        Label(canvas6, text="Username",font=('Arial',16), bg='#e6d8ad').place(x=740, y=160)
        username_entry = Entry(canvas6, textvariable=username,font=('Arial',16))
        username_entry.place(x=940, y=160)

        Label(canvas6, text="Address",font=('Arial',16), bg='#e6d8ad').place(x=740, y=210)
        address_entry = Entry(canvas6, textvariable=address,font=('Arial',16))
        address_entry.place(x=940, y=210)

        Label(canvas6, text="Phone Number",font=('Arial',16), bg='#e6d8ad').place(x=740, y=260)
        phone_number_entry = Entry(canvas6, textvariable=phone_number,font=('Arial',16))
        phone_number_entry.place(x=940, y=260)

        Label(canvas6, text="Email Address",font=('Arial',16), bg='#e6d8ad').place(x=740, y=310)
        email_address_entry = Entry(canvas6, textvariable=email_address,font=('Arial',16))
        email_address_entry.place(x=940, y=310)

        Label(canvas6, text="Date of Birth",font=('Arial',16), bg='#e6d8ad').place(x=740, y=360)
        date_of_birth_entry = Entry(canvas6, textvariable=date_of_birth,font=('Arial',16))
        date_of_birth_entry.place(x=940, y=360)

        Label(canvas6, text="Password",font=('Arial',16), bg='#e6d8ad').place(x=740, y=410)
        password_entry = Entry(canvas6, textvariable=password, show="*",font=('Arial',16))
        password_entry.place(x=940, y=410)

        # Function to retrieve and display profile information
        def retrive_customer_info():
            conn = sqlite3.connect("db_FOOD_ORDERING_SYSTEM.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USER WHERE USERNAME=?", (USERNAME_LOGIN.get(),))
            theuser = cursor.fetchone()


            first_name.set(theuser[1])
            last_name.set(theuser[2])
            username.set(theuser[3])
            address.set(theuser[4])
            phone_number.set(theuser[5])
            email_address.set(theuser[6])
            date_of_birth.set(theuser[7])
            password.set(theuser[8])

            conn.close()

        retrive_customer_info()

        # Function to save the updated profile information
        def save():
            conn = sqlite3.connect("db_FOOD_ORDERING_SYSTEM.db")
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE USER 
                SET FIRST_NAME=?, LAST_NAME=?, USERNAME=?, ADDRESS=?, PHONE_NUMBER=?, EMAIL_ADDRESS=?, DATE_OF_BIRTH=?, PASSWORD=?
                WHERE USER_ID=?""",
                (
                    first_name.get(), last_name.get(), username.get(), address.get(),
                    phone_number.get(), email_address.get(), date_of_birth.get(), password.get(), myid.get()
                )
            )
            conn.commit()
            conn.close()
            messagebox.showinfo(title='Profile Updated', message='Profile information updated successfully')
            edit_window.withdraw()
            customer_window()

        # Create buttons for search and save actions

        btn_save = Button(edit_window, text='Save' ,font=('Arial',16), command=save, bg='#dbac1a', fg='white')
        btn_save.place(x=920, y=460, width=160, height=40)
        btn_save.bind("<Enter>", lambda e: btn_save.config(bg="#e6d8ad"))
        btn_save.bind("<Leave>", lambda e: btn_save.config(bg="#dbac1a"))

        btn_back= Button(edit_window, text='Back', font=('Arial', 16), command=lambda: [customer_window(), edit_window.withdraw()], bg='#dbac1a', fg='white')
        btn_back.place(x=920, y=510, width=160, height=40)
        btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#e6d8ad"))
        btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#dbac1a"))

    open_edit_profile_window()
    customer_home_window.withdraw()
    # Run the application

def customer_window():
    global customer_home_window
    customer_home_window = Toplevel()
    customer_home_window.title("Home Page")
    customer_home_window.geometry("1920x1080+0+0")  # window size and position
    customer_home_window.config()  # used to customize the window (bg colour, title)
    customer_home_window.state("zoomed")  # maximize the root window to fill the entire screen
    # Constants
    WIDTH = 800
    HEIGHT = 700

    image = (Image.open(
        r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1).jpg"))
    resized_bgimage = image.resize((1920, 1080), Image.LANCZOS)
    backgroundimage = ImageTk.PhotoImage(resized_bgimage)
    backgroundimage.image = backgroundimage
    canvas1 = Canvas(customer_home_window)
    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0, 0, image=backgroundimage,
                         anchor="nw")

    lbl_home = Label(canvas1, text=f"Welcome to the Home Page, {USERNAME_LOGIN.get()}", font=('Arial', 20, 'bold'), bg='white')
    lbl_home.pack(pady=50)

    btn_menu = Button(canvas1, text="Menu", font=('Arial', 16), width=20, bg='#dbac1a', command=lambda:[customer_menu(), customer_home_window.withdraw()],
                           fg='white', relief='raised')
    btn_menu.bind("<Enter>", lambda e: btn_menu.config(bg="#e6d8ad"))
    btn_menu.bind("<Leave>", lambda e: btn_menu.config( bg='#dbac1a'))
    btn_menu.pack(pady=20)

    btn_profile = Button(canvas1, text="Profile", font=('Arial', 16), width=20,  bg='#dbac1a', fg='white',command=edit_profile,
                         relief='raised')
    btn_profile.bind("<Enter>", lambda e: btn_profile.config(bg="#e6d8ad"))
    btn_profile.bind("<Leave>", lambda e: btn_profile.config( bg='#dbac1a'))
    btn_profile.pack(pady=20)

    btn_logout = Button(canvas1, text="Logout", font=('Arial', 16), width=20, bg='#dbac1a', fg='white', command= lambda :[LoginForm(),customer_home_window.withdraw()],
                        relief='raised')
    btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#e6d8ad"))
    btn_logout.bind("<Leave>", lambda e: btn_logout.config( bg='#dbac1a'))
    btn_logout.pack(pady=20)

def customer_menu():
    # Establish connection to sqlite database
    connection = sqlite3.connect('db_FOOD_ORDERING_SYSTEM.db')
    cursor = connection.cursor()

    # create the ordered table if it dosen't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ordered (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment_info (
        cardholder_name TEXT NOT NULL,
        card_number TEXT NOT NULL,
        expiry_date REAL NOT NULL,
        cvv INTEGER NOT NULL,
        total_cost RAL NOT NULL
    )
    """)
    connection.commit()

    def fetch_products():
        cursor.execute("SELECT FOOD_ID, FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_PRICE FROM MENU")
        return cursor.fetchall()

    # function to handle placing an order
    def place_order():
        selected_item = products_tree.focus()
        if not selected_item:
            messagebox.showwarning('Place Order', 'Please select a product to order.')
            return

        quantity_str = quantity_entry.get()
        if not quantity_str.isdigit() or int(quantity_str) <= 0:
            messagebox.showwarning('Place Order', 'PLease enter a valid quantity (greater than zero).')
            return

        quantity = int(quantity_str)
        product = products_tree.item(selected_item)['values']
        food_name = product[1]
        price = float(product[4])
        total_cost = price * quantity

        # insert order into the ordered table
        cursor.execute("INSERT INTO ordered (food_name, price, quantity) VALUES (?, ?, ?)",
                       (food_name, price, quantity))
        connection.commit()

        # update order summary
        update_order_summary()

        # clear quantity entry
        quantity_entry.delete(0, tk.END)

        # refresh products list
        update_products_list()

    # function to remove order
    def remove_order():
        selected_order = products_tree.focus()
        if not selected_order:
            messagebox.showwarning('Remove Order', 'Please select an order to remove.')
            return

        product = products_tree.item(selected_order)['values']
        food_name = product[1]  # Assuming the order ID is the first value in the row

        # Remove order from the ordered table
        cursor.execute("DELETE FROM ordered WHERE food_name = ?", (food_name,))
        connection.commit()

        # Update order summary
        update_order_summary()

    # function to retrive the image path of food image
    def retrive_image():
        global image_path, new_food_image
        selected_item = products_tree.focus()

        product = products_tree.item(selected_item)['values']
        food_name = product[1]

        # Retrieve the image path from the database
        cursor.execute("SELECT IMAGE_PATH FROM MENU WHERE FOOD_NAME = ?", (food_name,))
        image_path_tuple = cursor.fetchone()  # fetchone() because you expect one result
        if image_path_tuple:
            image_path = image_path_tuple[0]  # Extract the path string from the tuple

            try:
                food_image = Image.open(image_path)
                resized_food_image = food_image.resize((300, 300), Image.LANCZOS)
                new_food_image = ImageTk.PhotoImage(resized_food_image)

            except Exception as e:
                print(f"Error opening image: {e}")
        else:
            print("No image path found for selected food item.")

    # function to update products list
    def update_products_list():
        products = fetch_products()
        # clear existing products in treeview
        for item in products_tree.get_children():
            products_tree.delete(item)

        # insert fetched products into treeview
        for product in products:
            products_tree.insert('', tk.END, values=product)

    # function to update order summary text
    def update_order_summary():
        total_price = 0.0
        order_summary_text.config(state=tk.NORMAL)
        order_summary_text.delete(1.0, tk.END)  # clear existing content

        cursor.execute("SELECT food_name, quantity, price FROM ordered")
        orders = cursor.fetchall()

        for order in orders:
            food_name, quantity, price = order
            subtotal = price * quantity
            total_price += subtotal
            order_summary_text.insert(tk.END, f"{food_name} x {quantity} = RM{subtotal:.2f}\n")

        tax_amount = total_price * 0.06
        total_cost = total_price + tax_amount
        order_summary_text.insert(tk.END, f"\nTax (6%): RM{tax_amount:.2f}\n")
        order_summary_text.insert(tk.END, f"Total Cost: RM{total_cost:.2f}\n\n")

        # disabling the text widget prevents further editing by user and ensures the displayed information is read only
        order_summary_text.config(state=tk.DISABLED)

    # function to clear order summary
    def clear_order_summary():
        cursor.execute("DELETE FROM ordered")
        connection.commit()
        update_order_summary()

    # function to open checkout window
    def open_checkout_window():
        checkout_window = tk.Toplevel(root)
        checkout_window.title("Checkout")
        checkout_window.geometry("1920x1080")
        image = (Image.open(
            r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1).jpg"))
        resized_bgimage = image.resize((1920, 1080), Image.LANCZOS)
        backgroundimage = ImageTk.PhotoImage(resized_bgimage)
        backgroundimage.image = backgroundimage


        # frame for order summary in checkout window

        canvas2 = Canvas(checkout_window)
        canvas2.pack(fill="both", expand=True)
        canvas2.create_image(0, 0, image=backgroundimage,
                             anchor="nw")

        label_summary = tk.Label(canvas2, text="Order Summary", font=('Arial', 18),bg="white")
        label_summary.pack()

        text_summary = tk.Text(canvas2, height=15, width=60, bg='#e8dbb1')
        text_summary.pack(pady=10)
        text_summary.config(state=tk.NORMAL)

        # fetch and display order summary
        cursor.execute("SELECT food_name, quantity, price FROM ordered")
        orders = cursor.fetchall()

        total_price = 0.0
        for order in orders:
            food_name, quantity, price = order
            subtotal = price * quantity
            total_price += subtotal
            text_summary.insert(tk.END, f"{food_name} x {quantity} = RM{subtotal:.2f}\n")

        tax_amount = total_price * 0.06
        total_cost = total_price + tax_amount
        text_summary.insert(tk.END, f"\nTax (6%): RM{tax_amount:.2f}\n")
        text_summary.insert(tk.END, f"Total Cost: RM{total_cost:.2f}\n\n")

        text_summary.config(state=tk.DISABLED)

        # button to pay by card
        button_pay_card = tk.Button(canvas2, text="Pay by Debit/Credit Card",
                                    command=lambda: [open_payment_details_window(total_cost), checkout_window.withdraw()],
                                    bg='#dbac1a', fg='white')  # set background and foreground colors
        button_pay_card.pack(pady=10)

    # function to open payment details window
    def open_payment_details_window(total_cost):
        payment_window = tk.Toplevel(root)
        payment_window.title("Payment Details")
        payment_window.geometry("1920x1080")
        image = (Image.open(
            r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1).jpg"))
        resized_bgimage = image.resize((1920, 1080), Image.LANCZOS)
        backgroundimage = ImageTk.PhotoImage(resized_bgimage)
        backgroundimage.image = backgroundimage

        canvas2 = Canvas(payment_window)
        canvas2.pack(fill="both", expand=True)
        canvas2.create_image(0, 0, image=backgroundimage,
                             anchor="nw")

        label_payment = tk.Label(canvas2, text="Enter Payment Details", font=('Arial', 18), bg='white')
        label_payment.pack()

        # card holder name
        label_name = tk.Label(canvas2, text="Cardholder Name:",bg='white',font=('Arial', 12))
        label_name.pack(pady=5)
        entry_name = tk.Entry(canvas2, width=30,bg='#e8dbb1',font=('Arial', 12))
        entry_name.pack()

        # card number
        label_card_number = tk.Label(canvas2, text="Card Number:",bg='white',font=('Arial', 12))
        label_card_number.pack(pady=5)
        entry_card_number = tk.Entry(canvas2, width=30,bg='#e8dbb1',font=('Arial', 12))
        entry_card_number.pack()

        # expiry date
        label_expiry = tk.Label(canvas2, text="Expiry:",bg='white',font=('Arial', 12))
        label_expiry.pack(pady=5)
        entry_expiry = tk.Entry(canvas2, width=30,bg='#e8dbb1',font=('Arial', 12))
        entry_expiry.pack()

        # CVV number
        label_cvv = tk.Label(canvas2, text="CVV Number:",bg='white',font=('Arial', 12))
        label_cvv.pack(pady=5)
        entry_cvv = tk.Entry(canvas2, width=5,bg='#e8dbb1',font=('Arial', 12))
        entry_cvv.pack()

        # Total cost
        label_total_cost = tk.Label(canvas2, text=f"Total Cost: ${total_cost:.2f}", font=('Arial', 14),bg='white')
        label_total_cost.pack(pady=10)

        # Button to process payment
        button_process_payment = tk.Button(canvas2, text="Process Payment",
                                           command=lambda: [process_payment(entry_name.get(), entry_card_number.get(),
                                                                           entry_expiry.get(), entry_cvv.get(),
                                                                           total_cost), payment_window.withdraw()],
                                           bg='#dbac1a', fg='white')  # Set background and foreground colors
        button_process_payment.pack(pady=10)

    # fuction to open review window
    def open_review_window():
        global review_window
        review_window = tk.Toplevel(root)
        review_window.title("review window")
        review_window.geometry("1920x1080")
        image = (Image.open(
            r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1).jpg"))
        resized_bgimage = image.resize((1920, 1080), Image.LANCZOS)
        backgroundimage = ImageTk.PhotoImage(resized_bgimage)
        backgroundimage.image = backgroundimage

        canvas2 = Canvas(review_window)
        canvas2.pack(fill="both", expand=True)
        canvas2.create_image(0, 0, image=backgroundimage,
                             anchor="nw")

        tk.Label(canvas2, text=f"Write a review", bg='white').pack(pady=10)
        review_entry = tk.Text(canvas2, width=50, height=10,bg='#e8dbb1')
        review_entry.pack(padx=10, pady=10)

        submit_button = tk.Button(canvas2, text="Submit",bg='#dbac1a', fg='white', font=("arial", 16),
                                  command=lambda: [submit_review(review_entry.get("1.0", 'end-1c'))])
        submit_button.pack(pady=10)

        close_button = tk.Button(canvas2, text="I Would Rather Not", bg='#dbac1a', fg='white',  font=("arial", 16),
                                  command=lambda: [review_window.withdraw()])
        close_button.pack(pady=10)

    def submit_review(review_content):
        if not review_content.strip():
            messagebox.showerror("Error", "Review cannot be empty.")
            return

        review_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO REVIEW (CUSTOMER_ID, REVIEW, REVIEW_DATE) VALUES (?, ?, ?)",
            (1, review_content, review_date)
        )
        connection.commit()

        review_window.withdraw()
        messagebox.showinfo("Success", "Review submitted successfully!")

    # function to process payment
    def process_payment(cardholder_name, card_number, expiry_date, cvv, total_cost):
        # insert payment details into the payment_info table
        cursor.execute(
            "INSERT INTO payment_info (cardholder_name, card_number, expiry_date, cvv, total_cost) VALUES (?, ?, ?, ?, ?)",
            (cardholder_name, card_number, expiry_date, cvv, total_cost))
        connection.commit()

        # show payment success message and update order status
        messagebox.showinfo("Payment Processed",
                            f"Payment of ${total_cost:.2f} processed successfully for {cardholder_name}.")

        # update order status
        update_order_status("Preparing")

        # open the review window
        open_review_window()

    def download_receipt():
        conn = sqlite3.connect('db_FOOD_ORDERING_SYSTEM.db')
        cursor = conn.cursor()
        cursor.execute("SELECT food_name, price, quantity FROM ordered")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showwarning("No Data", "No products to generate report")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        pdf = FPDF()
        pdf.add_page()

        # Add header title
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Receipt", ln=True, align="C")

        # Add space between the header and the table
        pdf.cell(200, 80, ln=True)  # Empty cell with height 10

        pdf.set_font("Arial", size=12)

        pdf.image(r"C:\Users\tanho\PycharmProjects\ALL project\image\Screenshot_20240630-203500_Chrome.jpg", 75, 20,
                  70, 70, '', '')

        # Set table header background color
        pdf.set_fill_color(230, 216, 173)

        # Add table headers with shading
        pdf.set_font("Arial", style="B")  # Bold font
        pdf.cell(70, 10, "Food Name", 1, 0, 'C', fill=True)
        pdf.cell(35, 10, "Price", 1, 0, 'C', fill=True)
        pdf.cell(35, 10, "Quantity", 1, 0, 'C', fill=True)
        pdf.cell(50, 10, "Total Price", 1, 1, 'C', fill=True)  # Move to next line after last cell
        pdf.set_font("Arial", size=12)  # Reset font

        # Reset fill color for table body
        pdf.set_fill_color(230, 216, 173)

        # Add table rows
        for row in rows:
            total_price = row[1] * row[2]  # Calculate total price for each row
            pdf.cell(70, 10, row[0], 1, 0, 'C')  # row[0] is food_name, should be a string
            pdf.cell(35, 10, f"RM{row[1]:.2f}", 1, 0, 'C')  # row[1] is price, format as string
            pdf.cell(35, 10, str(row[2]), 1, 0, 'C')  # row[2] is quantity, convert to string
            pdf.cell(50, 10, f"{total_price:.2f}", 1, 1, 'C')  # Move to next line after last cell

        # Add total price and total quantity at the end of the table
        total_price = sum(row[1] * row[2] for row in rows)
        tax = total_price * 0.06
        total_price_all = total_price + tax

        pdf.set_font("Arial", style="B")  # Bold font
        pdf.cell(140, 10, "Tax(6%) :", 1, 0, 'C', fill=True)
        pdf.cell(50, 10, f"RM{tax:.2f}", 1, 1, 'C', fill=True)  # Move to next line after last cell
        pdf.cell(140, 10, "Total Price:", 1, 0, 'C', fill=True)
        pdf.cell(50, 10, f"RM{total_price_all:.2f}", 1, 1, 'C', fill=True)  # Move to next line after last cell



        pdf.output(file_path)
        messagebox.showinfo("Success", "Receipt downloaded successfully!")
        os.startfile(file_path)  # Open the PDF file after creation

    # Function to update order status
    def update_order_status(status):
        order_status_label.config(text=f"Order Status: {status}")

    def search_data_customer():
        global result_text

        # Connect to the database
        conn = sqlite3.connect('db_FOOD_ORDERING_SYSTEM.db')
        c = conn.cursor()

        for i in products_tree.get_children():
            products_tree.delete(i)

        # Get the search term from the entry widget
        search_term = search_entry.get()

        # Execute the query
        if search_term == "":
            c.execute(
                "SELECT FOOD_ID, FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_PRICE FROM MENU")
            rows = c.fetchall()
        else:
            c.execute(
                "SELECT FOOD_ID, FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_PRICE FROM MENU WHERE FOOD_NAME LIKE ?",
                ('%' + search_term + '%',))
            rows = c.fetchall()

        for row in rows:
            products_tree.insert("", 'end', values=row)

    # main application window
    root = tk.Toplevel()
    root.title("Menu")
    root.geometry("1920x1080")
    root.configure(bg='#e6d8ad')

    # frame for restaurant banner
    frame_banner = tk.Frame(root)
    frame_banner.configure(bg='#e6d8ad')
    frame_banner.grid(row=0, column=0, columnspan=2)

    # frame for displaying products
    frame_products = tk.Frame(root)
    frame_products.configure(bg='#e6d8ad')
    frame_products.grid(row=1, column=0)

    search_entry = Entry(frame_products, width=50, font=('Arial', 16))
    search_entry.grid(row=0, column=0)

    search_btn = Button(frame_products, text="search", font=('Arial', 12), command=search_data_customer, bg='#dbac1a')
    search_btn.grid(row=0, column=0, sticky='e')

    # label and treeview for products
    label_products = tk.Label(frame_products, text="List of Foods Menu", font=('Arial', 18, 'bold'))
    label_products.grid(row=1, column=0, columnspan=4)

    products_tree = ttk.Treeview(frame_products, columns=('ID', 'Name', 'Description', 'Category', 'Price'),
                                 show='headings', height=10)
    style = ttk.Style()

    # Configure the Treeview heading font to be bold
    style.configure('Treeview.Heading', font=('Arial', 16) )
    products_tree.heading('ID', text='Food ID')
    products_tree.heading('Name', text='Food Name')
    products_tree.heading('Description', text='Description')
    products_tree.heading('Category', text='Category')
    products_tree.heading('Price', text='Price (RM)')

    # Center-align the text in each column
    style.configure('Treeview', font=('Arial', 12),foreground='grey')
    products_tree.column('ID', width=100, anchor='center')
    products_tree.column('Name', width=200, anchor='center')
    products_tree.column('Description', width=400, anchor='center')
    products_tree.column('Category', width=300, anchor='center')
    products_tree.column('Price', width=150, anchor='center')

    # Populate products Treeview
    update_products_list()
    products_tree.grid(row=1, column=0, padx=5, pady=5)

    # Frame for order summary and operations
    frame_order_summary = tk.Frame(root)
    frame_order_summary.configure(bg='#e6d8ad')
    frame_order_summary.grid(row=1, column=1, padx=5, pady=5, sticky='n')

    # Label and Text for order summary label_order_summary
    label_order_summary = tk.Label(frame_order_summary, text="List of Order", font=('Arial', 16, 'bold'), bg='#e6d8ad')
    label_order_summary.grid(row=0, column=0, sticky='ew')

    order_summary_text = tk.Text(frame_order_summary, height=10, width=40)
    order_summary_text.grid(row=1, column=0, padx=10, pady=10)
    order_summary_text.config(state=tk.DISABLED)

    # Button to clear order summary
    button_clear_summary = tk.Button(frame_order_summary, text="Clear Order Summary", command=clear_order_summary,font=('Arial', 12,),
                                     bg='#dbac1a', fg='black')
    button_clear_summary.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    # Frame for placing order and payment
    frame_order = tk.Frame(root, width=100, height=100)
    frame_order.grid(row=2, column=0, padx=100, pady=5, sticky='ew')
    frame_order.configure(bg='#e6d8ad')

    # Label and Entry for quantity
    label_quantity = tk.Label(frame_order, text="Quantity:",bg='#e6d8ad',font=('Arial', 12, 'bold'))
    label_quantity.grid(row=1, column=0, padx=10, pady=10)

    quantity_entry = tk.Entry(frame_order, width=10,font=('Arial', 12))
    quantity_entry.grid(row=1, column=1, padx=10, pady=10)

    # Buttons for placing order and checkout button_place_order
    button_place_order = tk.Button(frame_order, text="Place Order", font=('Arial', 12), command=place_order, bg='#a17b05',
                                   fg='white')  # Set background and foreground colors
    button_place_order.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    button_checkout = tk.Button(frame_order, text="Checkout", font=('Arial', 12), command=open_checkout_window, bg='#dbac1a',
                                fg='white')  # Set background and foreground colors
    button_checkout.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    button_remove_order = tk.Button(frame_order, text="Remove Order", font=('Arial', 12), command=remove_order, bg='#d6bf76',
                                    fg='white')  # Set background and foreground colors
    button_remove_order.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    button_download_receipt = tk.Button(frame_order, text="Download Receipt", font=('Arial', 12), command=download_receipt, bg='#b8a469',
                                    fg='white')  # Set background and foreground colors
    button_download_receipt.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # frame for displaying the food images
    frame_image = tk.Frame(root)
    frame_image.grid(row=2, column=0, padx=5, pady=5)

    displayDefaultImageObject = Image.open(
        r"C:\Users\tanho\PycharmProjects\ALL project\image\display - Default.jpg").resize((300, 300))
    displayDefaultImage = ImageTk.PhotoImage(displayDefaultImageObject)
    displayDefaultImage.image = displayDefaultImage

    def on_treeview_select(event):
        retrive_image()
        selected_item = products_tree.selection()
        if selected_item:
            food_image_label.config(image=new_food_image)

    products_tree.bind("<<TreeviewSelect>>", on_treeview_select)

    # label for restaurant banner and to show the restaurant banner
    image = Image.open(r'C:\Users\tanho\PycharmProjects\ALL project\image\Screenshot 2024-07-04 115424.jpg')
    resized_image = image.resize((1920, 260), Image.LANCZOS)
    new_image = ImageTk.PhotoImage(resized_image)


    food_image_label = tk.Label(frame_image, image=displayDefaultImage)
    food_image_label.pack()

    image_label = tk.Label(frame_banner, image=new_image, borderwidth=0, highlightthickness=0)
    image_label.image = new_image
    image_label.pack()

    # Label for order status
    order_status_label = tk.Label(root, text="Order Status: ", font=("Calibri", 12, 'bold'),bg='#e6d8ad')
    order_status_label.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky='w')

    btn_back = Button(root, text="Back to Home", font=('Arial', 14), bg='#dbac1a', fg='white',
                      command=lambda: [customer_window(), root.withdraw()])
    btn_back.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

    # close database connection when application is closed
    def on_closing():
        connection.close()
        root.destroy()

def Register():
    Database()
    if (USERNAME_REGISTER.get() == "" or PASSWORD_REGISTER.get() == "" or
        FIRSTNAME.get() == "" or LASTNAME.get() == "" or
        confirm_password_entry.get() == ""):
        messagebox.showerror("Error", "Please complete all the required fields!")
    elif PASSWORD_REGISTER.get() != confirm_password_entry.get():
        messagebox.showerror("Error", "Password and Confirm Password do not match!")
    else:
        try:
            cursor.execute("SELECT * FROM `USER` WHERE `USERNAME` = ?", (USERNAME_REGISTER.get(),))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "Username is already taken!")
            else:
                cursor.execute(
                    "INSERT INTO `USER` (FIRST_NAME, LAST_NAME, USERNAME, ADDRESS, PHONE_NUMBER, EMAIL_ADDRESS, DATE_OF_BIRTH, PASSWORD) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                    (str(FIRSTNAME.get()),str(LASTNAME.get()),str(USERNAME_REGISTER.get()), str(ADDRESS.get()),str(PHONE_NUMBER.get()), str(EMAIL_ADDRESS.get()), str(DATE_OF_BIRTH.get()), str(PASSWORD_REGISTER.get())))
                conn.commit()  #save current data to database
                FIRSTNAME.set("")
                LASTNAME.set("")
                USERNAME_REGISTER.set("")
                ADDRESS.set("")
                PHONE_NUMBER.set("")
                EMAIL_ADDRESS.set("")
                DATE_OF_BIRTH.set("")
                PASSWORD_REGISTER.set("")
                confirm_password_entry.delete(0, 'end')  # Clear confirm password field
                messagebox.showinfo("Success", "You Successfully Registered. Click to Login")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))

def Login():
    Database()
    if USERNAME_LOGIN.get() == "" or PASSWORD_LOGIN.get() == "":
        messagebox.showerror("Error", "Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM `USER` WHERE `USERNAME` = ? and `PASSWORD` = ?",
                        (USERNAME_LOGIN.get(), PASSWORD_LOGIN.get()))
        if  cursor.fetchone() is not None:
            messagebox.showinfo("Success", "You Successfully Login")
            if USERNAME_LOGIN.get() == "admin":
                Home()
                loginframe.withdraw()
            else:
                customer_window()
                loginframe.withdraw()
        else:
            messagebox.showerror("Error", "Invalid Username or password")


def Exit():
    result = messagebox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()

def update_profile_treeview():
    # Clear existing data in the treeview
    for item in profile_treeview.get_children():
        profile_treeview.delete(item)

    try:
        # Fetch data from the database
        cursor.execute("SELECT FIRST_NAME, LAST_NAME, USERNAME, ADDRESS, PHONE_NUMBER, EMAIL_ADDRESS FROM USER")
        rows = cursor.fetchall()

        # Populate the treeview with fetched data
        for row in rows:
            profile_treeview.insert("", "end", values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

def View_User_Info():
    global profile_treeview
    ProfileFrame = Toplevel()
    ProfileFrame.title("View Profile")
    ProfileFrame.geometry("1920x1080+0+0")  # window size and position
    ProfileFrame.state("zoomed")
    ProfileFrame.configure(bg='#e6d8ad')
    image = (Image.open(
        r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1).jpg"))
    resized_bgimage2 = image.resize((1920, 1080), Image.LANCZOS)
    backgroundimage2 = ImageTk.PhotoImage(resized_bgimage2)
    backgroundimage2.image = backgroundimage2
    canvas7 = Canvas(ProfileFrame)
    canvas7.pack(fill="both", expand=True)

    canvas7.create_image(0, 0, image=backgroundimage2,
                         anchor="nw")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial', 14), foreground="grey")

    profile_treeview = ttk.Treeview(canvas7,
                                 columns=("First Name", "Last Name", "Username", "Address", "Phone Number", "Email Address"),
                                 show='headings', height=20, style="Treeview")

    profile_treeview = ttk.Treeview(canvas7,
                                 columns=("First Name", "Last Name", "Username", "Address", "Phone Number", "Email Address"),
                                 show='headings', height=20)
    profile_treeview.heading("First Name", text="First Name")
    profile_treeview.heading("Last Name", text="Last Name")
    profile_treeview.heading('Username', text="Username")
    profile_treeview.heading('Address', text="Address")
    profile_treeview.heading("Phone Number", text="Phone Number")
    profile_treeview.heading("Email Address", text="Email Address")

    profile_treeview.column("First Name", width=200, anchor="center")
    profile_treeview.column("Last Name", width=200, anchor="center")
    profile_treeview.column('Username', width=200, anchor="center")
    profile_treeview.column('Address', width=300, anchor="center")
    profile_treeview.column("Phone Number", width=200, anchor="center")
    profile_treeview.column("Email Address", width=200, anchor="center")
    profile_treeview.pack(pady=20)

    btn_back = Button(canvas7, text="Back to Home", font=('Arial', 16), bg='#dbac1a', fg='white',
                      command=lambda: [Home(), ProfileFrame.withdraw()])
    btn_back.pack(pady=20)

    update_profile_treeview()

    HomeFrame.destroy

def Home():
    global HomeFrame
    HomeFrame = Frame(root)
    HomeFrame.pack(side='top', pady=60)
    root.withdraw()  # Hide the main login window
    HomeFrame = Toplevel()  # Create a new window
    HomeFrame.title("Home")
    HomeFrame.attributes('-fullscreen', True)
    image = (Image.open(r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1).jpg"))
    resized_bgimage = image.resize((1920, 1080), Image.LANCZOS)
    bgimage = ImageTk.PhotoImage(resized_bgimage)
    bgimage.image = bgimage
    canvas1 = Canvas(HomeFrame)
    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0, 0, image=bgimage,
                         anchor="nw")
    lbl_home = Label(canvas1, text="Welcome to the Home Page", font=('Arial', 20, 'bold'), bg='white')
    lbl_home.pack(pady=50)

    btn_dashboard = Button(canvas1, text="Food Dashboard", font=('Arial', 16), width=20, command=lambda:[FoodDashboard(),HomeFrame.withdraw()], bg='#dbac1a',
                           fg='white', relief='raised')
    btn_dashboard.bind("<Enter>", lambda e: btn_dashboard.config(bg="#E6D8AD"))
    btn_dashboard.bind("<Leave>", lambda e: btn_dashboard.config(bg="#dbac1a"))
    btn_dashboard.pack(pady=20)

    btn_view_profile = Button(canvas1, text="View User Profile", font=('Arial', 16), width=20, command=lambda:[View_User_Info(),HomeFrame.withdraw()], bg='#dbac1a',
                           fg='white', relief='raised')
    btn_view_profile.bind("<Enter>", lambda e: btn_view_profile.config(bg="#E6D8AD"))
    btn_view_profile.bind("<Leave>", lambda e: btn_view_profile.config(bg="#dbac1a"))
    btn_view_profile.pack(pady=20)

    btn_logout = Button(canvas1, text="Logout", font=('Arial', 16), width=20, command=lambda:[LoginForm(), HomeFrame.withdraw()], bg='#dbac1a',fg='white',
                        relief='raised')
    btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#E6D8AD"))
    btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="#dbac1a"))
    btn_logout.pack(pady=20)

def browse_pic():
    filename = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                          filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
    entry_picture.insert (END, filename)
    img = Image.open (filename)
    img. thumbnail ((150, 150))
    img = ImageTk. PhotoImage (img)
    display_pic_label.config (image=img)
    display_pic_label.image = img

def add_food_window1():
    global entry_picture, display_pic_label
    # Create a new window for adding food
    add_food_window = Toplevel()
    add_food_window.title("Add Food")
    add_food_window.geometry("1920x1080+0+0")  # window size and position
    add_food_window.state("zoomed")
    add_food_window.configure(bg='#E6D8AD')
    image = (Image.open(
        r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1) - Copy.png"))
    resized_bgimage = image.resize((1920, 1080), Image.LANCZOS)
    backgroundimage = ImageTk.PhotoImage(resized_bgimage)
    backgroundimage.image = backgroundimage
    canvas5 = Canvas(add_food_window)
    canvas5.pack(fill="both", expand=True)
    canvas5.create_image(0, 0, image=backgroundimage,
                         anchor="nw")
    canvas5.columnconfigure(0,weight=1)
    canvas5.columnconfigure(1,weight=1)

    # Define the layout of the window
    label_food_name = Label(canvas5, text="Food Name:", font=('Arial', 16), bg='#E6D8AD')
    label_food_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_food_name = Entry(canvas5, font=('Arial', 16))
    entry_food_name.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    label_description = Label(canvas5, text="Description:", font=('Arial', 16),bg='#E6D8AD')
    label_description.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_description = Entry(canvas5, font=('Arial', 16))
    entry_description.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    categories = ['Chinese Cuisine', 'Malay Cuisine', 'Indian Cuisine']
    selected = StringVar(canvas5)

    category_label = tk.Label(canvas5, text="Food Category:", font=('Arial', 16),bg='#E6D8AD')
    category_combobox = ttk.Combobox(canvas5, font=('Arial', 16), textvariable=selected,
                                     values=categories)
    category_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    category_combobox.grid(row=3, column=1, padx=10, pady=10, sticky='w')

    label_quantity = Label(canvas5, text="Quantity:", font=('Arial', 16),bg='#E6D8AD')
    label_quantity.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_quantity = Entry(canvas5, font=('Arial', 16))
    entry_quantity.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    label_price = Label(canvas5, text="Price:", font=('Arial', 16),bg='#E6D8AD')
    label_price.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_price = Entry(canvas5, font=('Arial', 16))
    entry_price.grid(row=4, column=1, padx=10, pady=10, sticky='w')

    label_picture = Label(canvas5, text="Add Picture:", font=('Arial', 16),bg='#E6D8AD')
    label_picture.grid(row=5, column=0, padx=10, pady=10, sticky="e")
    entry_picture = Entry(canvas5, font=('Arial', 16))
    entry_picture.grid(row=5, column=1, padx=10, pady=10, sticky='w')

    display_pic_label = tk.Label(canvas5)
    display_pic_label.grid(row=6, column=0, columnspan=2)

    button_browse_pic = Button(canvas5, text="Select Image", font=('Arial', 12), bg='#dbac1a', fg='black', command=lambda: [browse_pic()])
    button_browse_pic.grid(row=7, column=0, columnspan=2)

    # Create a button to add the food
    btn_add_food = Button(canvas5, text="Add Food", font=('Arial', 16), bg='#d6bf76',fg='white',
                          command=lambda: add_food(entry_food_name, entry_description, category_combobox, entry_quantity, entry_price, entry_picture))
    btn_add_food.grid(row=8, columnspan=2, pady=20)
    btn_back = Button(canvas5, text="Back to Dashboard", font=('Arial', 16), bg='#8a5e0c', fg='white',
                          command=lambda: [FoodDashboard(), add_food_window.withdraw()])
    btn_back.grid(row=9, columnspan=2, pady=20)

def add_food(entry_food_name, entry_description,category_combobox,entry_quantity, entry_price, entry_picture):
    # Get the values entered by the user
    food_name = entry_food_name.get()
    description = entry_description.get()
    price = entry_price.get()
    category = category_combobox.get()
    quantity = entry_quantity.get()
    picture = entry_picture.get()

    # Check if all fields are filled
    if food_name and description and price and category and quantity:
        try:
            # Insert the food details into the database
            cursor.execute("INSERT INTO MENU (FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_QUANTITY, FOOD_PRICE, IMAGE_PATH) VALUES (?, ?, ?, ?, ?, ?)",
                           (food_name, description, category, quantity, price, picture))
            conn.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Food successfully added!")

            # Fetch data from the database and update the food_treeview
            update_food_treeview()


        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding food: {e}")
    else:
        messagebox.showerror("Error", "Please fill in all fields!")

def update_food_treeview():
    # Clear existing data in the treeview
    for item in food_treeview.get_children():
        food_treeview.delete(item)

    try:
        # Fetch data from the database
        cursor.execute("SELECT FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_QUANTITY, FOOD_PRICE, IMAGE_PATH FROM MENU")
        rows = cursor.fetchall()

        # Populate the treeview with fetched data
        for row in rows:
            food_treeview.insert("", "end", values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching food data: {e}")


def search_data():
    global result_text

    # Connect to the database
    conn = sqlite3.connect('db_FOOD_ORDERING_SYSTEM.db')
    c = conn.cursor()

    for i in food_treeview.get_children():
        food_treeview.delete(i)

    # Get the search term from the entry widget
    search_term = search_entry.get()

    # Execute the query
    if search_term =="":
        c.execute("SELECT FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_QUANTITY, FOOD_PRICE , IMAGE_PATH FROM MENU")
        rows = c.fetchall()
    else:
        c.execute("SELECT FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_QUANTITY, FOOD_PRICE , IMAGE_PATH FROM MENU WHERE FOOD_NAME LIKE ?", ('%' + search_term + '%',))
        rows = c.fetchall()

    for row in rows:
        food_treeview.insert("", 'end', values=row)


def FoodDashboard():
    global HomeFrame, food_treeview, FoodFrame, search_entry, category_combobox

    HomeFrame.withdraw()  # Hide the home window
    FoodFrame = Toplevel()
    FoodFrame.title("Food Dashboard")
    FoodFrame.geometry("1920x1080")  # window size and position
    FoodFrame.configure(bg='#E6D8AD')

    image = (Image.open(
        r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1) - Copy.png"))
    resized_bgimage = image.resize((1920, 1080), Image.LANCZOS)
    backgroundimage = ImageTk.PhotoImage(resized_bgimage)
    backgroundimage.image = backgroundimage
    canvas4 = Canvas(FoodFrame)
    canvas4.pack(fill="both", expand=True)
    canvas4.create_image(0, 0, image=backgroundimage,
                         anchor="nw")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial', 14), foreground="grey")

    food_treeview = ttk.Treeview(canvas4, columns=("Food Name", "Description", "Category", "Quantity", "Price", "Image Path"),
                                 show='headings', height=20, style="Treeview")

    # Create a frame to contain the food options buttons


    search_frame = Frame(canvas4)
    search_frame.configure(bg='#E6D8AD')
    search_frame.pack(side="top", pady=10)

    logout_frame = Frame(canvas4)
    logout_frame.configure(bg='#E6D8AD')
    logout_frame.pack(side="bottom", pady=80)
    # Create the food options buttons



    search_entry = Entry(search_frame, width=50, font=('Arial', 16))
    search_entry.pack(side="left", padx=10)

    search_btn = Button(search_frame, text="search", font=('Arial', 16), command=search_data, bg='#dbac1a')
    search_btn.pack(side="left", padx=10)


    # Create a Treeview widget to display food items
    food_treeview = ttk.Treeview(canvas4, columns=("Food Name", "Description", "Category", "Quantity", "Price", "Image Path"),show='headings', height=20)
    food_treeview.heading("Food Name", text="Food Name")
    food_treeview.heading("Description", text="Description")
    food_treeview.heading('Category', text="Category")
    food_treeview.heading('Quantity', text="Quantity")
    food_treeview.heading("Price", text="Price")
    food_treeview.heading("Image Path", text="Image Path")

    food_treeview.column("Food Name", width=200, anchor="center")
    food_treeview.column("Description", width=400, anchor="center")
    food_treeview.column('Quantity', width=75, anchor="center")
    food_treeview.column('Category', width=300, anchor="center")
    food_treeview.column("Price", width=150, anchor="center")
    food_treeview.column("Image Path", width=150, anchor="center")
    food_treeview.pack(pady=20)

    food_options_frame = Frame(canvas4)
    food_options_frame.configure(bg='#E6D8AD')
    food_options_frame.pack(pady=20)

    btn_add_food = Button(food_options_frame, text="Add Food", font=('Arial', 16), width=15,
                          command=lambda: [add_food_window1(), FoodFrame.destroy()], bg='#a17b05', fg='white',
                          relief='raised')
    btn_add_food.bind("<Enter>", lambda e: btn_add_food.config(bg="#E6D8AD"))
    btn_add_food.bind("<Leave>", lambda e: btn_add_food.config(bg="#a17b05"))
    btn_add_food.pack(side="left", pady=10, padx=10)

    btn_delete_food = Button(food_options_frame, text="Delete Food", font=('Arial', 16), width=15,
                             command=delete_food, bg='#dbac1a', fg='white', relief='raised')
    btn_delete_food.bind("<Enter>", lambda e: btn_delete_food.config(bg="#E6D8AD"))
    btn_delete_food.bind("<Leave>", lambda e: btn_delete_food.config(bg="#dbac1a"))
    btn_delete_food.pack(side="left", pady=10, padx=10)

    btn_update_food = Button(food_options_frame, text="Update Food", font=('Arial', 16), width=15,
                             command=lambda: [update_food_window()], bg='#d6bf76', fg='white')
    btn_update_food.bind("<Enter>", lambda e: btn_update_food.config(bg="#E6D8AD"))
    btn_update_food.bind("<Leave>", lambda e: btn_update_food.config(bg="#d6bf76"))
    btn_update_food.pack(side="left", pady=10, padx=10)

    btn_back = Button(food_options_frame, text="Back to Home", font=('Arial', 16), width=15, bg='#dbac1a', fg='white',
                      command=lambda: [Home(), FoodFrame.withdraw()])
    btn_back.pack(side='left', pady=10, padx=10)
    btn_logout = Button(food_options_frame, text="Logout", font=('Arial', 16), width=15,
                        command=lambda: [LoginForm(), FoodFrame.withdraw()], bg='#8a5e0c',
                        fg='white',
                        relief='raised')
    btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#E6D8AD"))
    btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="#8a5e0c"))
    btn_logout.pack(side="left", pady=10, padx=10)

    # Populate the treeview with food data from the database
    update_food_treeview()

def update_food_window():
    # Get the selected food_id
    food_id = get_selected_food_id()

    if food_id:
        try:
            # Fetch the selected food details from the database
            cursor.execute("SELECT FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_QUANTITY, FOOD_PRICE, IMAGE_PATH FROM MENU WHERE FOOD_ID=?", (food_id,))
            food_details = cursor.fetchone()
            if food_details:
                # Create a new window for updating food
                update_food_window = Toplevel()
                update_food_window.title("Update Food")
                update_food_window.geometry("1920x1080+0+0")  # window size and position
                update_food_window.state("zoomed")
                update_food_window.configure(bg='#E6D8AD')
                image = (Image.open(
                    r"C:\Users\tanho\PycharmProjects\ALL project\image\360_F_269622083_VdHDLDkJ6ZKc8tmEN3M4LR995skrg6R2 (1) - Copy.png"))
                resized_bgimage = image.resize((1920, 1080), Image.LANCZOS)
                backgroundimage = ImageTk.PhotoImage(resized_bgimage)
                backgroundimage.image = backgroundimage
                canvas6 = Canvas(update_food_window)
                canvas6.pack(fill="both", expand=True)
                canvas6.create_image(0, 0, image=backgroundimage,
                                     anchor="nw")
                canvas6.columnconfigure(0,weight=1)
                canvas6.columnconfigure(1,weight=1)

                # Define the layout of the window
                label_food_name = Label(canvas6, text="Food Name:", font=('Arial', 16),bg='#E6D8AD')
                label_food_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
                entry_food_name = Entry(canvas6, font=('Arial', 16))
                entry_food_name.grid(row=0, column=1, padx=10, pady=10,sticky="w")
                entry_food_name.insert(0, food_details[0])  # Food name

                label_description = Label(canvas6, text="Description:", font=('Arial', 16),bg='#E6D8AD')
                label_description.grid(row=1, column=0, padx=10, pady=10, sticky="e")
                entry_description = Entry(canvas6, font=('Arial', 16))
                entry_description.grid(row=1, column=1, padx=10, pady=10,sticky="w")
                entry_description.insert(0, food_details[1])  # Description

                categories = ['Chinese Cuisine', 'Malay Cuisine', 'Indian Cuisine']
                selected = StringVar(canvas6)

                category_label = tk.Label(canvas6, text="Food Category:", font=('Arial', 16),bg='#E6D8AD')
                category_combobox = ttk.Combobox(canvas6, font=('Arial', 16), textvariable=selected,
                                                 values=categories)
                category_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
                category_combobox.grid(row=2, column=1, padx=10, pady=10, sticky='w')


                label_quantity = Label(canvas6, text="Quantity:", font=('Arial', 16),bg='#E6D8AD')
                label_quantity.grid(row=3, column=0, padx=10, pady=10, sticky="e")
                entry_quantity = Entry(canvas6, font=('Arial', 16))
                entry_quantity.grid(row=3, column=1, padx=10, pady=10, sticky="w")
                entry_quantity.insert(0, food_details[3])

                label_price = Label(canvas6, text="Price:", font=('Arial', 16),bg='#E6D8AD')
                label_price.grid(row=4, column=0, padx=10, pady=10, sticky="e")
                entry_price = Entry(canvas6, font=('Arial', 16))
                entry_price.grid(row=4, column=1, padx=10, pady=10,sticky="w")
                entry_price.insert(0, food_details[4])  # Price

                label_picture = Label(canvas6, text="Picture", font=('Arial', 16),bg='#E6D8AD')
                label_picture.grid(row=5, column=0, padx=10, pady=10, sticky="e")
                entry_picture = Entry(canvas6, font=('Arial', 16))
                entry_picture.grid(row=5, column=1, padx=10, pady=10,sticky="w")
                entry_picture.insert(0, food_details[5])

                button_browse_pic = Button(canvas6, text="Select Image", font=('Arial', 12),
                                           bg='#dbac1a', fg='white', command=lambda: [browse_pic()])
                button_browse_pic.grid(row=6, column=0, columnspan=2)

                # Create a button to update the food
                btn_update_food = Button(canvas6, text="Update Food", font=('Arial', 16), bg='#d6bf76', fg='white',
                                          command=lambda: update_food(food_id, entry_food_name.get(),entry_description.get(), category_combobox.get(), entry_quantity.get(), entry_price.get()))
                btn_update_food.grid(row=7, columnspan=2, pady=20)
                btn_back = Button(canvas6, text="Back to Dashboard", font=('Arial', 16), bg='#8a5e0c',
                                  fg='white',
                                  command=lambda : [FoodDashboard(), update_food_window.destroy()])
                btn_back.grid(row=8, columnspan=2, pady=20)
            else:
                messagebox.showerror("Error", "Selected food details not found.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food details: {e}")


def get_selected_food_id():
    selected_item = food_treeview.selection()
    if selected_item:
        item_values = food_treeview.item(selected_item, 'values')
        cursor.execute("SELECT FOOD_ID FROM MENU WHERE FOOD_NAME=?", (item_values[0],))
        food_id = cursor.fetchone()
        if food_id:
            return food_id[0]  # Return the food id
        else:
            messagebox.showerror("Error", "Selected food id not found.")
    else:
        messagebox.showerror("Error", "Please select a food item.")


def update_food(food_id, food_name, description, category, quantity, price):
    try:
        cursor.execute("UPDATE MENU SET FOOD_NAME=?, FOOD_DESCRIPTION=?, FOOD_CATEGORY=?, FOOD_QUANTITY=?, FOOD_PRICE=? WHERE FOOD_ID=?",
                       (food_name, description, category, quantity, price, food_id))
        conn.commit()  # Commit the transaction
        messagebox.showinfo("Success", "Food details updated successfully!")

        # Fetch the updated data from the database and update the food treeview
        update_food_treeview()


        # Show the food dashboard
        # Destroy the update window after the user clicks "OK" on the message box
        update_food_window.destroy
        FoodDashboard()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating food details: {e}")

def delete_food():
    # Get the selected item from the Treeview
    selected_item = food_treeview.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a food item to delete.")
        return

    # Get the item's values
    item_values = food_treeview.item(selected_item, 'values')
    food_name = item_values[0]

    # Prompt the user for confirmation
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{food_name}'?")

    if confirm:
        try:
            # Delete the selected item from the database table
            cursor.execute("DELETE FROM MENU WHERE food_name=?", (food_name,))
            conn.commit()  # Commit the transaction

            # Delete the selected item from the Treeview
            food_treeview.delete(selected_item)
            messagebox.showinfo("Success", f"'{food_name}' deleted successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting food: {e}")


LoginForm()
root.withdraw()
if __name__ == '__main__':
    root.mainloop()