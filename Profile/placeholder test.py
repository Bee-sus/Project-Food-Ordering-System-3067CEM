import sqlite3
from tkinter import *
from tkinter import messagebox


# Function to connect to the database and create the CUSTOMER table if it doesn't exist
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
        "PASSWORD TEXT (50) NOT NULL)"
    )
    conn.commit()


# Initialize the database
Database()

# Create the main application window
root = Tk()
root.title("Customer Profile Management")
root.geometry("400x200")  # Set the size of the main window


# Function to open the edit profile window
def open_edit_profile_window():
    edit_window = Toplevel(root)
    edit_window.title("Edit Profile")
    edit_window.geometry("400x400")  # Set the size of the new window

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
    Label(edit_window, text="Customer ID").place(x=10, y=10)
    id_entry = Entry(edit_window, textvariable=myid)
    id_entry.place(x=150, y=10)

    Label(edit_window, text="First Name").place(x=10, y=40)
    first_name_entry = Entry(edit_window, textvariable=first_name)
    first_name_entry.place(x=150, y=40)

    Label(edit_window, text="Last Name").place(x=10, y=70)
    last_name_entry = Entry(edit_window, textvariable=last_name)
    last_name_entry.place(x=150, y=70)

    Label(edit_window, text="Username").place(x=10, y=100)
    username_entry = Entry(edit_window, textvariable=username)
    username_entry.place(x=150, y=100)

    Label(edit_window, text="Address").place(x=10, y=130)
    address_entry = Entry(edit_window, textvariable=address)
    address_entry.place(x=150, y=130)

    Label(edit_window, text="Phone Number").place(x=10, y=160)
    phone_number_entry = Entry(edit_window, textvariable=phone_number)
    phone_number_entry.place(x=150, y=160)

    Label(edit_window, text="Email Address").place(x=10, y=190)
    email_address_entry = Entry(edit_window, textvariable=email_address)
    email_address_entry.place(x=150, y=190)

    Label(edit_window, text="Date of Birth").place(x=10, y=220)
    date_of_birth_entry = Entry(edit_window, textvariable=date_of_birth)
    date_of_birth_entry.place(x=150, y=220)

    Label(edit_window, text="Password").place(x=10, y=250)
    password_entry = Entry(edit_window, textvariable=password, show="*")
    password_entry.place(x=150, y=250)

    # Function to retrieve and display profile information
    def search():
        conn = sqlite3.connect("db_FOOD ORDERING SYSTEM.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CUSTOMER WHERE CUSTOMER_ID=?", (myid.get(),))
        theuser = cursor.fetchone()

        if theuser:
            first_name.set(theuser[1])
            last_name.set(theuser[2])
            username.set(theuser[3])
            address.set(theuser[4])
            phone_number.set(theuser[5])
            email_address.set(theuser[6])
            date_of_birth.set(theuser[7])
            password.set(theuser[8])
            messagebox.showinfo(title='ID Found', message='User found')
        else:
            messagebox.showerror(title='Error', message='Wrong ID')

        conn.close()

    # Function to save the updated profile information
    def save():
        conn = sqlite3.connect("db_FOOD ORDERING SYSTEM.db")
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE CUSTOMER 
            SET FIRST_NAME=?, LAST_NAME=?, USERNAME=?, ADDRESS=?, PHONE_NUMBER=?, EMAIL_ADDRESS=?, DATE_OF_BIRTH=?, PASSWORD=?
            WHERE CUSTOMER_ID=?""",
            (
                first_name.get(), last_name.get(), username.get(), address.get(),
                phone_number.get(), email_address.get(), date_of_birth.get(), password.get(), myid.get()
            )
        )
        conn.commit()
        conn.close()
        messagebox.showinfo(title='Profile Updated', message='Profile information updated successfully')

    # Create buttons for search and save actions
    btn_search = Button(edit_window, text='SEARCH', command=search)
    btn_search.place(x=50, y=300, width=80, height=30)

    btn_save = Button(edit_window, text='SAVE', command=save)
    btn_save.place(x=150, y=300, width=80, height=30)


# Add a button to the main window to open the edit profile window
btn_open_edit_profile_window = Button(root, text='Edit Profile', command=open_edit_profile_window)
btn_open_edit_profile_window.pack(pady=20)

# Run the application
root.mainloop()
