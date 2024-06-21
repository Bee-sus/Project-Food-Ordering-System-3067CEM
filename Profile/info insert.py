import sqlite3


def Database():
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
    conn.commit()

    # Insert sample data
    customers = [
        ('John', 'Doe', 'john doe', '123 Elm Street', '512-1234', 'johndoe@gmail.com', '1980-01-01', 'password123'),
        ('Jane', 'Smith', 'jane smith', '456 Oak Street', '513-5678', 'janesmith@gmail.com', '1985-02-02',
         'password456'),
        ('Alice', 'Johnson', 'alice j', '789 Pine Street', '514-9101', 'alicej@example.com', '1990-03-03', 'alice pass'),
        ('Bob', 'Brown', 'bobb', '101 Maple Street', '515-1122', 'bobb@example.com', '1975-04-04', 'bob password'),
        ('Charlie', 'Davis', 'charlie d', '202 Birch Street', '5516-3344', 'charlied@example.com', '1982-05-05',
         'charlie pass'),
        ('Diana', 'Evans', 'diana e', '303 Cedar Street', '517-5566', 'dianae@example.com', '1995-06-06', 'diana pass'),
        ('Eve', 'Foster', 'eve f', '404 Spruce Street', '518-7788', 'evef@example.com', '1978-07-07', 'eve password'),
        ('Frank', 'Garcia', 'frank g', '505 Walnut Street', '519-9900', 'frankg@example.com', '1988-08-08', 'frank pass'),
        ('Grace', 'Harris', 'grace h', '606 Aspen Street', '520-2233', 'graceh@example.com', '1992-09-09',
         'grace password'),
        ('Hank', 'Ivy', 'hanki', '707 Beech Street', '555-4455', 'hanki@example.com', '1983-10-10', 'hank password')
    ]

    cursor.executemany(
        "INSERT INTO CUSTOMER (FIRST_NAME, LAST_NAME, USERNAME, ADDRESS, PHONE_NUMBER, EMAIL_ADDRESS, DATE_OF_BIRTH, PASSWORD) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        customers
    )
    conn.commit()
    conn.close()


# Run the database initialization and data insertion
Database()