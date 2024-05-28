import sqlite3

#For Customer Registration and Login

conn = None
cursor = None
def Database():
    global conn, cursor
    conn = sqlite3.connect("Customer.db")
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

Database()

#Admin Login
def Database():
    global conn, cursor
    conn = sqlite3.connect("Admin.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `ADMIN` "
        "(USERNAME TEXT (50) PRIMARY KEY AUTOINCREMENT NOT NULL"
        "PASSWORD TEXT (50) NOT NULL) ")

#Menu
def Database():
    global conn, cursor
    conn = sqlite3.connect("Menu.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `MENU` "
        "(FOOD_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "FOOD_NAME TEXT (75) NOT NULL, "
        "FOOD_DESCRIPTION TEXT (75) NOT NULL, "
        "FOOD_CATEGORY TEXT (50) NOT NULL, "
        "FOOD_QUANTITY TEXT (50) NOT NULL, "
        "FOOD_PRICE REAL (50) NOT NULL) ")

#Order
def Database():
    global conn, cursor
    conn = sqlite3.connect("Order.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `ORDERS` "
        "(ORDER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "CUSTOMER_ID INTEGER FOREIGN KEY NOT NULL, "
        "ORDER_STATUS TEXT (25) NOT NULL, "
        "ORDER_REMARKS TEXT (100) NOT NULL, "
        "ORDER_DATE TEXT (50) NOT NULL) ")

#OrderDetails
def Database():
    global conn, cursor
    conn = sqlite3.connect("OrderDetails.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `ORDER_DETAILS` "
        "(ORDER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "FOOD_ID INTEGER FOREIGN KEY NOT NULL, "
        "ORDER_QUANTITY TEXT (50) NOT NULL, "
        "TOTAL_ORDER_PRICE REAL (50) NOT NULL, "
        "PAYMENT_STATUS TEXT (25) NOT NULL)")

#Review
def Database():
    global conn, cursor
    conn = sqlite3.connect("Review.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `REVIEW` "
        "(REVIEW_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
        "CUSTOMER_ID INTEGER FOREIGN KEY NOT NULL"
        "REVIEW TEXT (300) NOT NULL, "
        "REVIEW_DATE TEXT (25) NOT NULL)")




