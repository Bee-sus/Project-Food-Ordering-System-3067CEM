import sqlite3
import tkinter.messagebox as messagebox
from tkinter import Tk, StringVar, Toplevel, Frame, Label, Entry, Button, Menu

root = Tk()
root.title("Register and Login System")
root.geometry("1920x1080+0+0") #window size and position
root.config() #used to customize the window (bg colour, title)
root.state("zoomed")#maximize the root window to fill the entire screen
# Constants
WIDTH = 800
HEIGHT = 700

#create variables
USERNAME_LOGIN = StringVar()
PASSWORD_LOGIN = StringVar()
USERNAME_REGISTER = StringVar()
PASSWORD_REGISTER = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()
EMAIL_ADDRESS = StringVar()
PHONE_NUMBER = StringVar()
DOB = StringVar()

def Database(): #creating connection to database and creating table
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, "
        "password TEXT, firstname TEXT, lastname TEXT)")

def Exit():
    result = messagebox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()


def Home():
    global HomeFrame
    RegisterFrame = Frame(root)
    root.withdraw()  # Hide the main login window
    HomeFrame = Toplevel()  # Create a new window
    HomeFrame.title("Home")

    # Set the size of HomeFrame to match the login or register frame
    HomeFrame.geometry("%dx%d+%d+%d" % (
    WIDTH, HEIGHT, (root.winfo_screenwidth() - WIDTH) / 2, (root.winfo_screenheight() - HEIGHT) / 2))

    lbl_home = Label(HomeFrame, text="Welcome to the Home Page", font=('times new roman', 20, 'bold'))
    lbl_home.pack(pady=50)

    btn_logout = Button(HomeFrame, text="Logout", font=('times new roman', 16), width=20, command=Logout, bg='blue',
                        fg='white',
                        relief='raised')
    btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="lightblue"))
    btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="blue"))
    btn_logout.pack(pady=20)


def Logout():
    global root
    root.deiconify()  # Show the main login window again
    HomeFrame.destroy()  # Close the home window
    # Clear the username and password fields
    USERNAME_LOGIN.set("")
    PASSWORD_LOGIN.set("")


def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side='top', pady=80)

    lbl_title = Label(LoginFrame, text="Login:", font=('times new roman', 20, 'bold'), bd=18)
    lbl_title.grid(row=0, columnspan=1)

    lbl_username = Label(LoginFrame, text="Username:", font=('times new roman', 16), bd=18)
    lbl_username.grid(row=1, column=0)

    lbl_password = Label(LoginFrame, text="Password:", font=('times new roman', 16), bd=18)
    lbl_password.grid(row=2, column=0)

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
    lbl_text.grid(row=5, columnspan=2)

    lbl_register = Label(LoginFrame, text="Register Now", fg="Blue", font=('arial', 12))
    lbl_register.bind('<Enter>', lambda event, label=lbl_register: label.config(font=('arial', 12, 'underline')))
    lbl_register.bind('<Leave>', lambda event, label=lbl_register: label.config(font=('arial', 12)))
    lbl_register.bind('<Button-1>', ToggleToRegister)
    lbl_register.grid(row=6, columnspan=2)

def RegisterForm():
    global RegisterFrame, lbl_result2, confirm_password_entry
    RegisterFrame = Frame(root)
    RegisterFrame.pack(side='top', pady=60)

    lbl_login = Label(RegisterFrame, text="Click to Login", fg="Blue", font=('arial', 12))
    lbl_login.grid(row=11, columnspan=2)
    lbl_login.bind('<Button-1>', ToggleToLogin)

    lbl_result2 = Label(RegisterFrame, text="Registration Form:", font=('times new roman', 20, 'bold'), bd=18)
    lbl_result2.grid(row=1, columnspan=2)

    lbl_username = Label(RegisterFrame, text="Username:", font=('times new roman', 16), bd=18)
    lbl_username.grid(row=2)

    lbl_password = Label(RegisterFrame, text="Password:", font=('times new roman', 16), bd=18)
    lbl_password.grid(row=3)

    lbl_confirm_password = Label(RegisterFrame, text="Confirm Password:", font=('times new roman', 16), bd=18)
    lbl_confirm_password.grid(row=4)

    lbl_firstname = Label(RegisterFrame, text="Firstname:", font=('times new roman', 16), bd=18)
    lbl_firstname.grid(row=5)

    lbl_lastname = Label(RegisterFrame, text="Lastname:", font=('times new roman', 16), bd=18)
    lbl_lastname.grid(row=6)

    lbl_email_address = Label(RegisterFrame, text="Email Address:", font=('times new roman', 16),bd=18)
    lbl_email_address.grid(row=7)

    lbl_phone_number = Label(RegisterFrame, text="Phone Number:", font=('times new roman', 16),bd=18)
    lbl_phone_number.grid(row=8)

    lbl_dob = Label(RegisterFrame,text="DOB:", font=('times new roman', 16),bd=18)
    lbl_dob.grid(row=9)

    username = Entry(RegisterFrame, font=('times new roman', 16), textvariable=USERNAME_REGISTER, width=15)
    username.grid(row=2, column=1)

    password = Entry(RegisterFrame, font=('times new roman', 16), textvariable=PASSWORD_REGISTER, width=15, show="*")
    password.grid(row=3, column=1)

    confirm_password_entry = Entry(RegisterFrame, font=('times new roman', 16), width=15, show="*")
    confirm_password_entry.grid(row=4, column=1)

    firstname = Entry(RegisterFrame, font=('times new roman', 16), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=5, column=1)

    lastname = Entry(RegisterFrame, font=('times new roman', 16), textvariable=LASTNAME, width=15)
    lastname.grid(row=6, column=1)

    email_address = Entry(RegisterFrame, font=('times new roman', 16), textvariable= EMAIL_ADDRESS, width=15)
    email_address.grid(row=7, column=1)

    phone_number = Entry(RegisterFrame, font=('times new roman', 16), textvariable=PHONE_NUMBER, width=15)
    phone_number.grid(row=8, column=1)

    dob = Entry(RegisterFrame, font=("times new roman", 16),textvariable=DOB, width=15)
    dob.grid(row=9, column=1)

    btn_login = Button(RegisterFrame, text="Register", font=('arial', 15), width=20, command=Register, bg='blue',
                       fg='white', relief='raised')
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="lightblue"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="blue"))
    btn_login.grid(row=10, columnspan=2, pady=20)

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
            cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME_REGISTER.get(),))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "Username is already taken!")
            else:
                cursor.execute(
                    "INSERT INTO `member` (username, password, firstname, lastname) VALUES(?, ?, ?, ?)",
                    (str(USERNAME_REGISTER.get()), str(PASSWORD_REGISTER.get()), str(FIRSTNAME.get()),
                     str(LASTNAME.get())))
                conn.commit()  #save current data to database
                USERNAME_REGISTER.set("")
                PASSWORD_REGISTER.set("")
                FIRSTNAME.set("")
                LASTNAME.set("")
                confirm_password_entry.delete(0, 'end')  # Clear confirm password field
                messagebox.showinfo("Success", "You Successfully Registered. Click to Login")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))

def Login():
    Database()
    if USERNAME_LOGIN.get() == "" or PASSWORD_LOGIN.get() == "":
        messagebox.showerror("Error", "Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?",
                        (USERNAME_LOGIN.get(), PASSWORD_LOGIN.get()))
        if cursor.fetchone() is not None:
            messagebox.showinfo("Success", "You Successfully Login")
            Home()  # Call Home function after successful login
        else:
            messagebox.showerror("Error", "Invalid Username or password")


LoginForm()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


if __name__ == '__main__':
    root.mainloop()
