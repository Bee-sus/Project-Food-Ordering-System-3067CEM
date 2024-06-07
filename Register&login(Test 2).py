import sqlite3
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
from tkinter import ttk, Menu
from tkinter import Tk, StringVar, Toplevel, Frame, Label, Entry, Button
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk

root = Tk()
root.title("Register and Login System")
root.geometry("1920x1080+0+0")  # window size and position
root.config()  # used to customize the window (bg colour, title)
root.state("zoomed")# maximize the root window to fill the entire screen
root.configure(bg="light blue")

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
    conn = sqlite3.connect("db_FOOD ORDERING SYSTEM.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `CUSTOMER` "
        "(CUSTOMER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
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
        "FOOD_PRICE REAL (50) NOT NULL) ")


def Exit():
    result = messagebox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()


def Home():
    global HomeFrame
    HomeFrame = Frame(root)
    HomeFrame.pack(side='top', pady=60)
    root.withdraw()  # Hide the main login window
    HomeFrame = Toplevel()  # Create a new window
    HomeFrame.title("Home")
    HomeFrame.attributes('-fullscreen', True)

    lbl_home = Label(HomeFrame, text="Welcome to the Home Page", font=('times new roman', 20, 'bold'))
    lbl_home.pack(pady=50)

    btn_dashboard = Button(HomeFrame, text="Food Dashboard", font=('times new roman', 16), width=20, command=FoodDashboard,bg='blue',
                           fg='white', relief='raised')
    btn_dashboard.bind("<Enter>", lambda e: btn_dashboard.config(bg="lightblue"))
    btn_dashboard.bind("<Leave>", lambda e: btn_dashboard.config(bg="blue"))
    btn_dashboard.pack(pady=20)

    btn_logout = Button(HomeFrame, text="Logout", font=('times new roman', 16), width=20, command=Logout, bg='blue',fg='white',
                        relief='raised')
    btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="lightblue"))
    btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="blue"))
    btn_logout.pack(pady=20)


def add_food_window():
    # Create a new window for adding food
    add_food_window = Toplevel()
    add_food_window.title("Add Food")
    add_food_window.geometry("1920x1080+0+0")  # window size and position
    add_food_window.state("zoomed")
    add_food_window.columnconfigure(0,weight=1)
    add_food_window.columnconfigure(1,weight=1)

    # Define the layout of the window
    label_food_name = Label(add_food_window, text="Food Name:", font=('times new roman', 16))
    label_food_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_food_name = Entry(add_food_window, font=('times new roman', 16))
    entry_food_name.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    label_description = Label(add_food_window, text="Description:", font=('times new roman', 16))
    label_description.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_description = Entry(add_food_window, font=('times new roman', 16))
    entry_description.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    label_category = Label(add_food_window, text="Category:", font=('times new roman', 16))
    label_category.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_category = Entry(add_food_window, font=('times new roman', 16))
    entry_category.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    label_quantity = Label(add_food_window, text="Quantity:", font=('times new roman', 16))
    label_quantity.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_quantity = Entry(add_food_window, font=('times new roman', 16))
    entry_quantity.grid(row=3, column=1, padx=10, pady=10, sticky='w')

    label_price = Label(add_food_window, text="Price:", font=('times new roman', 16))
    label_price.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_price = Entry(add_food_window, font=('times new roman', 16))
    entry_price.grid(row=4, column=1, padx=10, pady=10, sticky='w')

    # Create a button to add the food
    btn_add_food = Button(add_food_window, text="Add Food", font=('times new roman', 16), bg='green',fg='white',
                          command=lambda: add_food(entry_food_name, entry_description, entry_price))
    btn_add_food.grid(row=3, columnspan=2, pady=20)
    btn_back = Button(add_food_window, text="Back to Dashboard", font=('times new roman', 16), bg='brown', fg='white',
                          command=lambda: [FoodDashboard(), add_food_window.destroy()])
    btn_back.grid(row=4, columnspan=2, pady=20)

def add_food(entry_food_name, entry_description, entry_price):
    # Get the values entered by the user
    food_name = entry_food_name.get()
    description = entry_description.get()
    price = entry_price.get()
    category = entry_category.get()
    quantity = entry_quantity.get()

    # Check if all fields are filled
    if food_name and description and price and category and quantity:
        try:
            # Insert the food details into the database
            cursor.execute("INSERT INTO MENU (FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_QUANTITY, FOOD_PRICE) VALUES (?, ?, ?, ?, ?, ?)",
                           (food_name, description, price, category ,quantity))
            conn.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Food successfully added!")

            # Fetch data from the database and update the food_treeview
            update_food_treeview()

            # Destroy the add_food_window
            add_food_window.destroy()
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
        cursor.execute("SELECT FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_QUANTITY, FOOD_PRICE FROM MENU")
        rows = cursor.fetchall()

        # Populate the treeview with fetched data
        for row in rows:
            food_treeview.insert("", "end", values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching food data: {e}")

def search_data():
    global result_text

    # Connect to the database
    conn = sqlite3.connect('db_FOOD ORDERING SYSTEM.db')
    c = conn.cursor()

    for i in food_treeview.get_children():
        food_treeview.delete(i)

    # Get the search term from the entry widget
    search_term = search_entry.get()

    # Execute the query
    c.execute("SELECT FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_QUANTITY, FOOD_PRICE FROM MENU WHERE FOOD_NAME LIKE ?", ('%' + search_term + '%',))
    rows = c.fetchall()

    for row in rows:
        food_treeview.insert("", 'end', values=row)

def FoodDashboard():
    global HomeFrame, food_treeview, FoodFrame, search_entry

    HomeFrame.withdraw()  # Hide the home window
    FoodFrame = Toplevel()
    FoodFrame.title("Food Dashboard")
    FoodFrame.geometry("1920x1080+0+0")  # window size and position
    FoodFrame.state("zoomed")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), foreground="grey")

    food_treeview = ttk.Treeview(FoodFrame, columns=("Food Name", "Description", "Category", "Quantity" "Price"),
                                 show='headings', height=20, style="Treeview")

    # Create a frame to contain the food options buttons
    food_options_frame = Frame(FoodFrame)
    food_options_frame.pack(side="top", pady=20)

    search_frame = Frame(FoodFrame)
    search_frame.pack(side="top", pady=10)

    logout_frame = Frame(FoodFrame)
    logout_frame.pack(side="bottom", pady=80)
    # Create the food options buttons
    btn_add_food = Button(food_options_frame, text="Add Food", font=('times new roman', 16), width=15,
                          command=lambda: [add_food_window(), FoodFrame.destroy()], bg='blue',fg='white', relief='raised')
    btn_add_food.bind("<Enter>", lambda e: btn_add_food.config(bg="lightblue"))
    btn_add_food.bind("<Leave>", lambda e: btn_add_food.config(bg="blue"))
    btn_add_food.pack(side="left", padx=10)

    btn_delete_food = Button(food_options_frame, text="Delete Food", font=('times new roman', 16), width=15,
                             command=delete_food,bg='green', fg='white', relief='raised')
    btn_delete_food.bind("<Enter>", lambda e: btn_delete_food.config(bg="lightblue"))
    btn_delete_food.bind("<Leave>", lambda e: btn_delete_food.config(bg="green"))
    btn_delete_food.pack(side="left", padx=10)

    btn_update_food = Button(food_options_frame, text="Update Food", font=('times new roman', 16), width=15,
                             command=lambda : [update_food_window()], bg='yellow', fg='black')
    btn_update_food.pack(side="left", padx=10)

    btn_logout = Button(logout_frame, text="Logout", font=('times new roman', 16), width=20, command=Logout, bg='blue',
                        fg='white',
                        relief='raised')

    search_entry = Entry(search_frame, width=50, font=('times new roman', 16))
    search_entry.pack(side="left", padx=10)

    search_btn = Button(search_frame, text="search", font=('times new roman', 16), command=search_data)
    search_btn.pack(side="left", padx=10)

    btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="lightblue"))
    btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="blue"))
    btn_logout.pack(side="top", pady=50)

    # Create a Treeview widget to display food items
    food_treeview = ttk.Treeview(FoodFrame, columns=("Food Name", "Description","Category", "Quantity", "Price"),show='headings', height=20)
    food_treeview.heading("Food Name", text="food name")
    food_treeview.heading("Description", text="description")
    food_treeview.heading('Category', text="Category")
    food_treeview.heading('Quantity', text="Quantity")
    food_treeview.heading("Price", text="price")

    food_treeview.column("Food Name", width=200, anchor="center")
    food_treeview.column("Description", width=400, anchor="center")
    food_treeview.column('Category', width=300, anchor="center")
    food_treeview.column('Quantity', width=75, anchor="center")
    food_treeview.column("Price", width=150, anchor="center")
    food_treeview.pack(pady=20)

    # Populate the treeview with food data from the database
    update_food_treeview()

def update_food_window():
    # Get the selected food_id
    food_id = get_selected_food_id()

    if food_id:
        try:
            # Fetch the selected food details from the database
            cursor.execute("SELECT FOOD_NAME, FOOD_DESCRIPTION, FOOD_CATEGORY, FOOD_QUANTITY, FOOD_PRICE FROM MENU WHERE FOOD_ID=?", (food_id,))
            food_details = cursor.fetchone()
            if food_details:
                # Create a new window for updating food
                update_food_window = Toplevel()
                update_food_window.title("Update Food")
                update_food_window.geometry("1920x1080+0+0")  # window size and position
                update_food_window.state("zoomed")
                update_food_window.columnconfigure(0,weight=1)
                update_food_window.columnconfigure(1,weight=1)

                # Define the layout of the window
                label_food_name = Label(update_food_window, text="Food Name:", font=('times new roman', 16))
                label_food_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
                entry_food_name = Entry(update_food_window, font=('times new roman', 16))
                entry_food_name.grid(row=0, column=1, padx=10, pady=10,sticky="w")
                entry_food_name.insert(0, food_details[0])  # Food name

                label_description = Label(update_food_window, text="Description:", font=('times new roman', 16))
                label_description.grid(row=1, column=0, padx=10, pady=10, sticky="e")
                entry_description = Entry(update_food_window, font=('times new roman', 16))
                entry_description.grid(row=1, column=1, padx=10, pady=10,sticky="w")
                entry_description.insert(0, food_details[1])  # Description

                label_category = Label(update_food_window, text="Category:", font=('times new roman', 16))
                label_category.grid(row=2, column=0, padx=10, pady=10, sticky="e")
                entry_category = Entry(update_food_window, font=('times new roman', 16))
                entry_category.grid(row=2, column=1, padx=10, pady=10, sticky="w")
                entry_category.insert(0, food_details[2])

                label_quantity = Label(update_food_window, text="Quantity:", font=('times new roman', 16))
                label_quantity.grid(row=3, column=0, padx=10, pady=10, sticky="e")
                entry_quantity = Entry(update_food_window, font=('times new roman', 16))
                entry_quantity.grid(row=3, column=1, padx=10, pady=10, sticky="w")
                entry_quantity.insert(0, food_details[3])

                label_price = Label(update_food_window, text="Price:", font=('times new roman', 16))
                label_price.grid(row=4, column=0, padx=10, pady=10, sticky="e")
                entry_price = Entry(update_food_window, font=('times new roman', 16))
                entry_price.grid(row=4, column=1, padx=10, pady=10,sticky="w")
                entry_price.insert(0, food_details[4])  # Price

                # Create a button to update the food
                btn_update_food = Button(update_food_window, text="Update Food", font=('times new roman', 16), bg='green', fg='white',
                                          command=lambda: update_food(food_id, entry_food_name.get(),entry_description.get(), entry_category.get(), entry_quantity.get(), entry_price.get()))
                btn_update_food.grid(row=3, columnspan=2, pady=20)
                btn_back = Button(update_food_window, text="Back to Dashboard", font=('times new roman', 16), bg='brown',
                                  fg='white',
                                  command=lambda : [FoodDashboard(), update_food_window.destroy()])
                btn_back.grid(row=4, columnspan=2, pady=20)
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
        update_food_window.destroy()
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
            cursor.execute("DELETE FROM food WHERE food_name=?", (food_name,))
            conn.commit()  # Commit the transaction

            # Delete the selected item from the Treeview
            food_treeview.delete(selected_item)
            messagebox.showinfo("Success", f"'{food_name}' deleted successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting food: {e}")





def Logout():
    global root
    root.deiconify()  # Show the main login window again
    HomeFrame.destroy()  # Close the home window
    FoodFrame.destroy()
    # Clear the username and password fields
    USERNAME_LOGIN.set("")
    PASSWORD_LOGIN.set("")

def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.configure(bg="light blue")
    LoginFrame.pack(side='top', pady=80)

    lbl_title = Label(LoginFrame, text="Login:", font=('times new roman', 20, 'bold'), bd=18)
    lbl_title.configure(bg="light blue")
    lbl_title.grid(row=0, columnspan=1)

    lbl_username = Label(LoginFrame, text="Username:", font=('times new roman', 16), bd=18)
    lbl_username.configure(bg="light blue")
    lbl_username.grid(row=1, column=0)

    lbl_password = Label(LoginFrame, text="Password:", font=('times new roman', 16), bd=18)
    lbl_password.configure(bg="light blue")
    lbl_password.grid (row=2, column=0)

    username = Entry(LoginFrame, font=('times new roman', 16), textvariable=USERNAME_LOGIN, width=15)
    username.grid(row=1, column=1)

    password = Entry(LoginFrame, font=('times new roman', 16), textvariable=PASSWORD_LOGIN, width=15, show="*")
    password.grid(row=2, column=1)

    btn_login = Button(LoginFrame, text="Login", font=('times new roman', 16), width=20, command=Login, bg='blue', fg='white',
                       relief='raised')
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="lightblue"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="blue"))
    btn_login.grid(row=4, columnspan=2, pady=30)

    lbl_text = Label(LoginFrame, text="Not a member?", font=('times new roman', 14))
    lbl_text.configure(bg="light blue")
    lbl_text.grid(row=5, columnspan=2)

    lbl_register = Label(LoginFrame, text="Register Now", fg="Blue", font=('arial', 12))
    lbl_register.configure(bg="light blue")
    lbl_register.bind('<Enter>', lambda event, label=lbl_register: label.config(font=('arial', 12, 'underline')))
    lbl_register.bind('<Leave>', lambda event, label=lbl_register: label.config(font=('arial', 12)))
    lbl_register.bind('<Button-1>', ToggleToRegister)
    lbl_register.grid(row=6, columnspan=2)

def RegisterForm():
    global RegisterFrame, lbl_result2, confirm_password_entry
    RegisterFrame = Frame(root)
    RegisterFrame.configure(bg="light blue")
    RegisterFrame.pack(side='top', pady=60)

    lbl_login = Label(RegisterFrame, text="Click to Login", fg="Blue", font=('arial', 12))
    lbl_login.grid(row=13, columnspan=2)
    lbl_login.bind('<Button-1>', ToggleToLogin)

    lbl_result2 = Label(RegisterFrame, text="Registration Form:", font=('times new roman', 20, 'bold'), bd=18)
    lbl_result2.grid(row=1, columnspan=2)

    lbl_firstname = Label(RegisterFrame, text="First Name:", font=('times new roman', 14), bd=18)
    lbl_firstname.grid(row=2)

    lbl_lastname = Label(RegisterFrame, text="Last Name:", font=('times new roman', 14), bd=18)
    lbl_lastname.grid(row=3)

    lbl_username = Label(RegisterFrame, text="Username:", font=('times new roman', 14), bd=18)
    lbl_username.grid(row=4)

    lbl_address = Label(RegisterFrame, text="Address:", font=('times new roman', 14), bd=18)
    lbl_address.grid(row=5)

    lbl_phone_number = Label(RegisterFrame, text="Phone Number:", font=('times new roman', 14), bd=18)
    lbl_phone_number.grid(row=6)

    lbl_email_address = Label(RegisterFrame, text="Email Address:", font=('times new roman', 14), bd=18)
    lbl_email_address.grid(row=7)

    lbl_date_of_birth = Label(RegisterFrame, text="Date of Birth:", font=('times new roman', 14), bd=18)
    lbl_date_of_birth.grid(row=8)

    lbl_password = Label(RegisterFrame, text="Password:", font=('times new roman', 14), bd=18)
    lbl_password.grid(row=9)

    lbl_confirm_password = Label(RegisterFrame, text="Confirm Password:", font=('times new roman', 14), bd=18)
    lbl_confirm_password.grid(row=10)

    #Entry frames

    firstname = Entry(RegisterFrame, font=('times new roman', 14), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=2, column=1)

    lastname = Entry(RegisterFrame, font=('times new roman', 14), textvariable=LASTNAME, width=15)
    lastname.grid(row=3, column=1)

    username = Entry(RegisterFrame, font=('times new roman', 14), textvariable=USERNAME_REGISTER, width=15)
    username.grid(row=4, column=1)

    address = Entry(RegisterFrame, font=('times new roman', 14), textvariable=ADDRESS, width=15)
    address.grid(row=5, column=1)

    phone_number = Entry(RegisterFrame, font=('times new roman', 14), textvariable=PHONE_NUMBER, width=15)
    phone_number.grid(row=6, column=1)

    email_address = Entry(RegisterFrame, font=('times new roman', 14), textvariable=EMAIL_ADDRESS, width=15)
    email_address.grid(row=7, column=1)

    date_of_birth = Entry(RegisterFrame, font=('times new roman', 14), textvariable=DATE_OF_BIRTH, width=15)
    date_of_birth.grid(row=8, column=1)

    password = Entry(RegisterFrame, font=('times new roman', 14), textvariable=PASSWORD_REGISTER, width=15, show="*")
    password.grid(row=9, column=1)

    confirm_password_entry = Entry(RegisterFrame, font=('times new roman', 14), width=15, show="*")
    confirm_password_entry.grid(row=10, column=1)

    btn_login = Button(RegisterFrame, text="Register", font=('arial', 15), width=20, command=Register, bg='blue',fg='white', relief='raised')
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="lightblue"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="blue"))
    btn_login.grid(row=11, columnspan=2, pady=20)

def ToggleToLogin(event=None):    #switching from register to login page.
    if RegisterFrame is not None:
        RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None): #switching the interface from login to register after user click the register link
    if LoginFrame is not None:     #if login form is display, then need to deleted and switch to registration form
        LoginFrame.destroy()
    RegisterForm()

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
            cursor.execute("SELECT * FROM `CUSTOMER` WHERE `USERNAME` = ?", (USERNAME_REGISTER.get(),))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "Username is already taken!")
            else:
                cursor.execute(
                    "INSERT INTO `CUSTOMER` (FIRST_NAME, LAST_NAME, USERNAME, ADDRESS, PHONE_NUMBER, EMAIL_ADDRESS, DATE_OF_BIRTH, PASSWORD) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
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
        cursor.execute("SELECT * FROM `CUSTOMER` WHERE `USERNAME` = ? and `PASSWORD` = ?",
                        (USERNAME_LOGIN.get(), PASSWORD_LOGIN.get()))
        if  cursor.fetchone() is not None:
            messagebox.showinfo("Success", "You Successfully Login")
            Home()  # Call Home function after successful login
        else:
            messagebox.showerror("Error", "Invalid Username or password")

LoginForm()

if __name__ == '__main__':
    root.mainloop()