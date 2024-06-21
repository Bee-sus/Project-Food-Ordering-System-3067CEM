import tkinter as tk
from tkinter import messagebox


class CustomerProfilePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Profile Page")

        # Labels and Entry Widgets
        self.create_label_entry("First Name", 0)
        self.create_label_entry("Last Name", 1)
        self.create_label_entry("Date of Birth (YYYY-MM-DD)", 2)
        self.create_label_entry("Password", 3, show="*")
        self.create_label_entry("Username", 4)
        self.create_label_entry("Email Address", 5)

        # Edit and Save Buttons
        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_profile)
        self.edit_button.grid(row=6, column=0, pady=10)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_profile, state=tk.DISABLED)
        self.save_button.grid(row=6, column=1, pady=10)

    def create_label_entry(self, text, row, show=None):
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(self.root, show=show)
        entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f"{text.lower().replace(' ', '_')}_entry", entry)

    def edit_profile(self):
        for entry in self.get_entries():
            entry.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.edit_button.config(state=tk.DISABLED)

    def save_profile(self):
        profile_data = {entry_name: entry.get() for entry_name, entry in self.get_entries().items()}

        # Simple validation
        if not all(profile_data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        messagebox.showinfo("Profile Saved", "Customer profile has been saved successfully!")

        for entry in self.get_entries():
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


# Create the main window
root = tk.Tk()
app = CustomerProfilePage(root)
root.mainloop()

