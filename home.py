import tkinter as tk
from tkinter import messagebox

# Define functions for navigation
def open_menu():
    messagebox.showinfo("Menu", "Navigating to Menu...")

def open_profile():
    messagebox.showinfo("Profile", "Navigating to Profile...")

def open_orders():
    messagebox.showinfo("Orders", "Navigating to Orders...")

def logout():
    messagebox.showinfo("Logout", "Logging out...")
    root.destroy()

# Main application window
root = tk.Tk()
root.title("Customer Homepage")
root.geometry("400x300")

# Welcome label
welcome_label = tk.Label(root, text="Welcome to the Food Ordering System", font=("Helvetica", 16))
welcome_label.pack(pady=20)

# Menu button
menu_button = tk.Button(root, text="Menu", width=20, command=open_menu)
menu_button.pack(pady=10)

# Profile button
profile_button = tk.Button(root, text="Profile", width=20, command=open_profile)
profile_button.pack(pady=10)

# Orders button
orders_button = tk.Button(root, text="Orders", width=20, command=open_orders)
orders_button.pack(pady=10)

# Logout button
logout_button = tk.Button(root, text="Logout", width=20, command=logout)
logout_button.pack(pady=10)

# Run the application
root.mainloop()
