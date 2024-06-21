import tkinter as tk
from tkinter import messagebox
import sqlite3


class CustomerProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.conn = sqlite3.connect('customer_profile.db')
        self.create_table()

        self.create_label_entry("First Name", 0)
        self.create_label_entry("Last Name", 1)
        self.create_label_entry("Date of Birth (YYYY-MM-DD)", 2)
        self.create_label_entry("Password", 3, show="*")
        self.create_label_entry("Username", 4)
        self.create_label_entry("Email Address", 5)

        self.edit_button = tk.Button(self, text="Edit", command=self.edit_profile)
        self.edit_button.grid(row=6, column=0, pady=10)

        self.save_button = tk.Button(self, text="Save", command=self.save_profile, state=tk.DISABLED)
        self.save_button.grid(row=6, column=1, pady=10)

        self.home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        self.home_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.load_profile()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CUSTOMER (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                password TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                email_address TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def create_label_entry(self, text, row, show=None):
        label = tk.Label(self, text=text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(self, show=show)
        entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f"{text.lower().replace(' ', '_')}_entry", entry)

    def edit_profile(self):
        for entry in self.get_entries().values():
            entry.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.edit_button.config(state=tk.DISABLED)

    def save_profile(self):
        profile_data = {entry_name: entry.get() for entry_name, entry in self.get_entries().items()}

        if not all(profile_data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM CUSTOMER")
        if cursor.fetchone():
            cursor.execute("""
                UPDATE CUSTOMER SET
                first_name = ?,
                last_name = ?,
                date_of_birth = ?,
                password = ?,
                username = ?,
                email_address = ?
            """, (profile_data["First Name"], profile_data["Last Name"], profile_data["Date of Birth (YYYY-MM-DD)"],
                  profile_data["Password"], profile_data["Username"], profile_data["Email Address"]))
        else:
            cursor.execute("""
                INSERT INTO CUSTOMER (first_name, last_name, date_of_birth, password, username, email_address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (profile_data["First Name"], profile_data["Last Name"], profile_data["Date of Birth (YYYY-MM-DD)"],
                  profile_data["Password"], profile_data["Username"], profile_data["Email Address"]))

        self.conn.commit()
        messagebox.showinfo("Profile Saved", "Customer profile has been saved successfully!")

        for entry in self.get_entries().values():
            entry.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.edit_button.config(state=tk.NORMAL)

    def get_entries(self):
        return {
            "First Name": self.first_name_entry,
            "Last Name": self.last_name_entry,
            "Date of Birth (YYYY-MM-DD)": self.date_of_birth_entry,
            "Password": self.password_entry,
            "Username": self.username_entry,
            "Email Address": self.email_address_entry
        }

    def load_profile(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM CUSTOMER")
        customer = cursor.fetchone()
        if customer:
            self.first_name_entry.insert(0, customer[1])
            self.last_name_entry.insert(0, customer[2])
            self.date_of_birth_entry.insert(0, customer[3])
            self.password_entry.insert(0, customer[4])
            self.username_entry.insert(0, customer[5])
            self.email_address_entry.insert(0, customer[6])

            for entry in self.get_entries().values():
                entry.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            self.edit_button.config(state=tk.NORMAL)
        else:
            self.edit_profile()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Home Page")
        label.pack(pady=10, padx=10)

        profile_button = tk.Button(self, text="Go to Profile Page",
                                   command=lambda: controller.show_frame(CustomerProfilePage))
        profile_button.pack()

        menu_button = tk.Button(self, text="Go to Menu Page", command=lambda: controller.show_frame(MenuPage))
        menu_button.pack()


class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Menu Page")
        label.pack(pady=10, padx=10)

        home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        home_button.pack()


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Customer Profile Management System")
        self.geometry("400x300")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, CustomerProfilePage, MenuPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, context):
        frame = self.frames[context.__name__]
        frame.tkraise()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
