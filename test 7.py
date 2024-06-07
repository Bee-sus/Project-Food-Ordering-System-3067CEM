import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import random
from datetime import date, datetime
import sqlite3


# Database setup
def setup_database():
    global conn_menu, cursor_menu, conn_order, cursor_order, conn_order_details, cursor_order_details, conn_review, cursor_review

    # Menu Database
    conn_menu = sqlite3.connect("Menu.db")
    cursor_menu = conn_menu.cursor()
    cursor_menu.execute(
        "CREATE TABLE IF NOT EXISTS `MENU` "
        "(FOOD_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "FOOD_NAME TEXT (75) NOT NULL, "
        "FOOD_DESCRIPTION TEXT (75) NOT NULL, "
        "FOOD_CATEGORY TEXT (50) NOT NULL, "
        "FOOD_QUANTITY TEXT (50) NOT NULL, "
        "FOOD_PRICE REAL (50) NOT NULL) "
    )
    conn_menu.commit()

    # Order Database
    conn_order = sqlite3.connect("Order.db")
    cursor_order = conn_order.cursor()
    cursor_order.execute(
        "CREATE TABLE IF NOT EXISTS `ORDERS` "
        "(ORDER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "CUSTOMER_ID INTEGER NOT NULL, "
        "ORDER_STATUS TEXT (25) NOT NULL, "
        "ORDER_REMARKS TEXT (100) NOT NULL, "
        "ORDER_DATE TEXT (50) NOT NULL) "
    )
    conn_order.commit()

    # Order Details Database
    conn_order_details = sqlite3.connect("OrderDetails.db")
    cursor_order_details = conn_order_details.cursor()
    cursor_order_details.execute(
        "CREATE TABLE IF NOT EXISTS `ORDER_DETAILS` "
        "(ORDER_DETAIL_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "ORDER_ID INTEGER NOT NULL, "
        "FOOD_ID INTEGER NOT NULL, "
        "ORDER_QUANTITY TEXT (50) NOT NULL, "
        "TOTAL_ORDER_PRICE REAL (50) NOT NULL, "
        "PAYMENT_STATUS TEXT (25) NOT NULL, "
        "FOREIGN KEY(ORDER_ID) REFERENCES ORDERS(ORDER_ID), "
        "FOREIGN KEY(FOOD_ID) REFERENCES MENU(FOOD_ID)) "
    )
    conn_order_details.commit()

    # Review Database
    conn_review = sqlite3.connect("Review.db")
    cursor_review = conn_review.cursor()
    cursor_review.execute(
        "CREATE TABLE IF NOT EXISTS `REVIEW` "
        "(REVIEW_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "CUSTOMER_ID INTEGER NOT NULL, "
        "REVIEW TEXT (300) NOT NULL, "
        "REVIEW_DATE TEXT (25) NOT NULL, "
        "FOREIGN KEY(CUSTOMER_ID) REFERENCES ORDERS(CUSTOMER_ID)) "
    )
    conn_review.commit()


# Setup the databases
setup_database()

prices = {"Fried Calamari": 10, "Beach Burger": 14, "Salmon Wonder": 23, "Shrimp Tacos": 15, "Sushi Platter": 25,
          "Empanadas": 10}

root = Tk()
root.title("Restaurant")
root.geometry("1920x1080+0+0")
root.state("zoomed")


# ------------------------------------FUNCTIONS--------------------------------------------- #

# region Generating a random Order ID when starting a new order
def ORDER_ID():
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
    order_id = "BIN_"
    random_letters = ""
    random_digits = ""
    for i in range(0, 3):
        random_letters += random.choice(letters)
        random_digits += str(random.choice(numbers))

    order_id += random_letters + random_digits
    return order_id


# region Add to Order Button
def add():
    # updating the transaction label
    current_order = orderTransaction.cget("text")
    added_dish = displayLabel.cget("text") + "...." + str(prices[displayLabel.cget("text")]) + "RM "
    updated_order = current_order + added_dish
    orderTransaction.configure(text=updated_order)

    # updating the order total label
    order_total = orderTotalLabel.cget("text").replace("TOTAL : ", "")
    order_total = order_total.replace("RM", "")
    updated_total = int(order_total) + prices[displayLabel.cget("text")]
    orderTotalLabel.configure(text="TOTAL : " + "RM" + str(updated_total))


# region Remove Button Function
def remove():
    dish_to_remove = displayLabel.cget("text") + "...." + str(prices[displayLabel.cget("text")])
    transaction_list = orderTransaction.cget("text").split("RM ")
    transaction_list.pop(len(transaction_list) - 1)

    if dish_to_remove in transaction_list:
        # update transaction label
        transaction_list.remove(dish_to_remove)
        updated_order = ""
        for item in transaction_list:
            updated_order += item + "RM "

        orderTransaction.configure(text=updated_order)

        # update transaction total
        order_total = orderTotalLabel.cget("text").replace("TOTAL : ", "")
        order_total = order_total.replace("RM", "")
        updated_total = int(order_total) - prices[displayLabel.cget("text")]
        orderTotalLabel.configure(text="TOTAL : " + "RM" + str(updated_total))


def order():
    # Retrieve and clean the order ID
    new_receipt = orderIDLabel.cget("text").replace("ORDER ID : ", "")

    # Get the transaction list and clean it
    transaction_list = orderTransaction.cget("text").split("RM ")
    transaction_list.pop(len(transaction_list) - 1)

    # Get the current date and time
    order_day = date.today()
    order_time = datetime.now()

    # Fix the transaction list items
    transaction_list = [item + "RM " for item in transaction_list]

    # Create a new window for the receipt
    global receipt_window
    receipt_window = Toplevel(root)
    receipt_window.title(f"Receipt - {new_receipt}")

    # Create and place the receipt content in the new window
    receipt_text = Text(receipt_window, wrap='word', bg='white', fg='black', font=('Helvetica', 12))
    receipt_text.pack(expand=True, fill='both')

    receipt_text.insert('end', "The Binary\n")
    receipt_text.insert('end', "________________________________________________________\n")
    receipt_text.insert('end', order_day.strftime("%d-%m-%y") + "\n")
    receipt_text.insert('end', order_time.strftime("%X") + "\n\n")
    for item in transaction_list:
        receipt_text.insert('end', item + "\n")
    receipt_text.insert('end', "\n\n")
    receipt_text.insert('end', orderTotalLabel.cget("text") + "\n")

    # Disable the text widget to make it read-only
    receipt_text.config(state='disabled')

    # Store order details in the database
    cursor_order.execute(
        "INSERT INTO ORDERS (CUSTOMER_ID, ORDER_STATUS, ORDER_REMARKS, ORDER_DATE) VALUES (?, ?, ?, ?)",
        (1, 'Completed', '', order_time.strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn_order.commit()
    order_id = cursor_order.lastrowid

    for item in transaction_list:
        food_name = item.split("....")[0]
        cursor_menu.execute("SELECT FOOD_ID FROM MENU WHERE FOOD_NAME=?", (food_name,))
        food_id = cursor_menu.fetchone()[0]
        food_quantity = 1  # Assuming 1 for simplicity; you can modify as needed
        total_price = prices[food_name]
        cursor_order_details.execute(
            "INSERT INTO ORDER_DETAILS (ORDER_ID, FOOD_ID, ORDER_QUANTITY, TOTAL_ORDER_PRICE, PAYMENT_STATUS) VALUES (?, ?, ?, ?, ?)",
            (order_id, food_id, food_quantity, total_price, 'Paid')
        )
    conn_order_details.commit()

    # Reset the UI elements for the next order
    orderTotalLabel.configure(text="TOTAL : RM0")
    orderIDLabel.configure(text="ORDER ID : " + ORDER_ID(), font=("Helvetica", 20, "bold"))
    orderTransaction.configure(text="")

    # Button for payment
    payment_button = tk.Button(receipt_window, text="Payment", command=payment)
    payment_button.pack(pady=10)


# Button and window for transaction
def payment():
    global payment_window
    payment_window = tk.Toplevel(receipt_window)
    payment_window.title("Transaction")

    # Frame for transaction ID entry
    transaction_frame = tk.Frame(payment_window)
    transaction_frame.pack(pady=10)

    transaction_id_label = tk.Label(transaction_frame, text="Transaction ID:")
    transaction_id_label.pack(side="left")

    global transaction_id_entry
    transaction_id_entry = tk.Entry(transaction_frame)
    transaction_id_entry.pack(side="left")

    # Button to submit transaction ID
    transaction_button = tk.Button(payment_window, text="Submit", command=submit_transaction)
    transaction_button.pack(pady=10)


# Payment processing function
def submit_transaction():
    transaction_id = transaction_id_entry.get()
    if not transaction_id:
        messagebox.showerror("Error", "Please enter a transaction ID.")
        return

    # Save the transaction ID and close the window
    with open("transaction.txt", "a") as file:
        file.write(f"{transaction_id}\n")

    payment_window.destroy()
    receipt_window.destroy()
    messagebox.showinfo("Success", "Transaction completed successfully!")


# Review Button Function
def review():
    global review_window
    review_window = tk.Toplevel(root)
    review_window.title("Review")

    review_text = tk.Text(review_window, wrap='word', bg='white', fg='black', font=('Helvetica', 12))
    review_text.pack(expand=True, fill='both')

    submit_button = tk.Button(review_window, text="Submit",
                              command=lambda: submit_review(review_text.get("1.0", 'end-1c')))
    submit_button.pack(pady=10)


def submit_review(review_content):
    if not review_content.strip():
        messagebox.showerror("Error", "Review cannot be empty.")
        return

    review_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor_review.execute(
        "INSERT INTO REVIEW (CUSTOMER_ID, REVIEW, REVIEW_DATE) VALUES (?, ?, ?)",
        (1, review_content, review_date)
    )
    conn_review.commit()

    review_window.destroy()
    messagebox.showinfo("Success", "Review submitted successfully!")


# ------------------------------------UI Setup--------------------------------------------- #
s = ttk.Style()
s.configure('MainFrame.TFrame', background="#E6D8AD")
s.configure('MenuFrame.TFrame', background="#E6D8AD")
s.configure('DisplayFrame.TFrame', background="#E6D8AD", highlightbackground="black")
s.configure('OrderFrame.TFrame', background="#E6D8AD")
s.configure('MenuLabel.TLabel', background="#E6D8AD", font=("Arial", 13, "italic"), foreground="brown",
            padding=(5, 5, 5, 5), width=21)
s.configure('orderTotalLabel.TLabel', background="#E6D8AD", font=("Arial", 10, "bold"), foreground="black",
            padding=(2, 2, 2, 2), anchor="w")
s.configure('orderTransaction.TLabel', background="#E6D8AD", font=('Helvetica', 12), foreground="black", wraplength=170,
            anchor="nw", padding=(3, 3, 3, 3))
s.configure('orderIDLabel.TLabel', background="#E6D8AD", font=("Helvetica", 20, "bold"), foreground="black",
            anchor="center")

# Menu images
displayDefaultImageObject = Image.open("Binary/display - Default.png").resize((300, 300))
displayDefaultImage = ImageTk.PhotoImage(displayDefaultImageObject)

calamariImageObject = Image.open("Binary/fried calamari.png").resize((300, 300))
calamariImage = ImageTk.PhotoImage(calamariImageObject)

burgerImageObject = Image.open("Binary/beach burger.png").resize((300, 300))
burgerImage = ImageTk.PhotoImage(burgerImageObject)

salmonImageObject = Image.open("Binary/salmon wild rice.png").resize((300, 300))
salmonImage = ImageTk.PhotoImage(salmonImageObject)

shrimpImageObject = Image.open("Binary/shrimp tacos.png").resize((300, 300))
shrimpImage = ImageTk.PhotoImage(shrimpImageObject)

sushiImageObject = Image.open("Binary/sushi platter.png").resize((300, 300))
sushiImage = ImageTk.PhotoImage(sushiImageObject)

empanadasImageObject = Image.open("Binary/empanadas.png").resize((300, 300))
empanadasImage = ImageTk.PhotoImage(empanadasImageObject)

# Section Frames
mainFrame = ttk.Frame(root, style='MainFrame.TFrame')
mainFrame.pack(fill="both", expand=True)

menuFrame = ttk.Frame(mainFrame, style='MenuFrame.TFrame')
menuFrame.grid(row=0, column=0, rowspan=2, sticky="NSEW", padx=(20, 20), pady=(20, 20))

displayFrame = ttk.Frame(menuFrame, style='DisplayFrame.TFrame')
displayFrame.grid(row=1, column=0, sticky="NSEW", padx=(20, 20), pady=(20, 20))

orderFrame = ttk.Frame(mainFrame, style='OrderFrame.TFrame')
orderFrame.grid(row=0, column=1, rowspan=2, sticky="NSEW", padx=(20, 20), pady=(20, 20))

mainFrame.columnconfigure(0, weight=1)
mainFrame.columnconfigure(1, weight=1)
mainFrame.rowconfigure(0, weight=1)
mainFrame.rowconfigure(1, weight=1)

# Display widgets
displayLabel = Label(displayFrame, text="", font=("Arial", 30, "bold"), background="#E6D8AD", foreground="brown",
                     width=24, height=1, anchor="center")
displayLabel.grid(row=0, column=0, pady=(20, 20))

displayMenuLabel = Label(displayFrame, image=displayDefaultImage, width=300, height=300)
displayMenuLabel.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))

# Order frame
orderIDLabel = ttk.Label(orderFrame, text="ORDER ID : " + ORDER_ID(), style="orderIDLabel.TLabel")
orderIDLabel.grid(row=0, column=0, pady=(20, 20))

orderTransaction = ttk.Label(orderFrame, text="", style="orderTransaction.TLabel")
orderTransaction.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nw", columnspan=2)

orderTotalLabel = ttk.Label(orderFrame, text="TOTAL : RM0", style="orderTotalLabel.TLabel")
orderTotalLabel.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nw")

# Order Frame Buttons
orderButton = Button(orderFrame, text="Order", font=("Helvetica", 12, "bold"), command=order, background="green",
                     foreground="white")
orderButton.grid(row=3, column=0, pady=(10, 10), padx=(20, 20), sticky="nsew")

addButton = Button(orderFrame, text="Add to Order", font=("Helvetica", 12, "bold"), command=add, background="blue",
                   foreground="white")
addButton.grid(row=4, column=0, pady=(10, 10), padx=(20, 20), sticky="nsew")

removeButton = Button(orderFrame, text="Remove", font=("Helvetica", 12, "bold"), command=remove, background="red",
                      foreground="white")
removeButton.grid(row=5, column=0, pady=(10, 10), padx=(20, 20), sticky="nsew")

reviewButton = Button(orderFrame, text="Review", font=("Helvetica", 12, "bold"), command=review, background="orange",
                      foreground="white")
reviewButton.grid(row=6, column=0, pady=(10, 10), padx=(20, 20), sticky="nsew")

# Treeview to display menu items
treeview = ttk.Treeview(menuFrame, columns=("Item", "Price", "Description", "Category", "Quantity"), show='headings')
treeview.heading('Item', text='Item')
treeview.heading('Price', text='Price')
treeview.heading('Description', text='Description')
treeview.heading('Category', text='Category')
treeview.heading('Quantity', text='Qty')
treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

for item, price in prices.items():
    treeview.insert('', 'end', values=(item, f"RM {price}"))


# Event handling for Treeview selection
def on_treeview_select(event):
    selected_item = treeview.selection()
    if selected_item:
        item = treeview.item(selected_item)["values"][0]
        displayLabel.config(text=item)
        displayMenuLabel.config(image=menuImages[item])


treeview.bind("<<TreeviewSelect>>", on_treeview_select)

# Images dictionary for menu items
menuImages = {"Fried Calamari": calamariImage, "Beach Burger": burgerImage, "Salmon Wonder": salmonImage,
              "Shrimp Tacos": shrimpImage, "Sushi Platter": sushiImage, "Empanadas": empanadasImage}

root.mainloop()

