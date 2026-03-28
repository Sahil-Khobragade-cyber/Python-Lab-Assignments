import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

inventory = [
    (101, "Pen", 10, 50),
    (102, "Notebook", 50, 20),
    (103, "Marker", 30, 5),
    (104, "Pencil", 5, 100),
    (105, "Eraser", 3, 60)
]

vendors = {
    101: ("ABC Suppliers", "abc@gmail.com", 2018),
    102: ("XYZ Traders", "xyz@gmail.com", 2020),
    103: ("PQR Wholesalers", "pqr@gmail.com", 2015),
    104: ("LMN Stationers", "lmn@gmail.com", 2019),
    105: ("RST Supplies", "rst@gmail.com", 2021)
}

def search_item(item_id):
    for item in inventory:
        if item[0] == item_id:
            return item
    return "Item not found"

def update_stock(item_id, new_stock):
    global inventory
    inventory = [(i[0], i[1], i[2], new_stock) if i[0] == item_id else i for i in inventory]

def check_low_stock(threshold=10):
    for item in inventory:
        if item[3] < threshold:
            print("Low stock:", item)

def add_item():
    global inventory, vendors
    
    item_id = int(input("Enter ID: "))
    
    for item in inventory:
        if item[0] == item_id:
            print("ID already exists!")
            return
    
    name = input("Enter Name: ")
    price = int(input("Enter Price: "))
    stock = int(input("Enter Stock: "))
    
    inventory.append((item_id, name, price, stock))
    
    v_name = input("Enter Vendor Name: ")
    v_email = input("Enter Vendor Email: ")
    v_year = int(input("Enter Association Year: "))
    
    vendors[item_id] = (v_name, v_email, v_year)
    
    print("Item added successfully!")

def remove_item():
    global inventory, vendors
    
    item_id = int(input("Enter ID to remove: "))
    
    inventory = [item for item in inventory if item[0] != item_id]
    
    if item_id in vendors:
        del vendors[item_id]
    
    print("Item removed successfully!")

def sort_items():
    df = pd.DataFrame(inventory, columns=["ID", "Name", "Price", "Stock"])
    df = df.sort_values(by="Stock", ascending=False)
    print(df)

def vendor_report():
    for item in inventory:
        vendor = vendors.get(item[0])
        if vendor:
            total_value = item[2] * item[3]
            print(item[1], "|", vendor[0], "| Value:", total_value)

def generate_report():
    prices = np.array([i[2] for i in inventory])
    stocks = np.array([i[3] for i in inventory])
    total_value = np.sum(prices * stocks)
    print("Total Inventory Value:", total_value)

def plot_bar():
    df = pd.DataFrame(inventory, columns=["ID", "Name", "Price", "Stock"])
    plt.bar(df["Name"], df["Stock"])
    plt.title("Stock Levels")
    plt.show()

def plot_pie():
    df = pd.DataFrame(inventory, columns=["ID", "Name", "Price", "Stock"])
    plt.pie(df["Stock"], labels=df["Name"], autopct="%1.1f%%")
    plt.show()

while True:
    print("\n1.View 2.Search 3.Update 4.LowStock 5.Report 6.Sort 7.Vendor 8.Bar 9.Pie 10.Add 11.Remove 12.Exit")
    ch = int(input("Enter: "))

    if ch == 1:
        print(pd.DataFrame(inventory, columns=["ID", "Name", "Price", "Stock"]))
    elif ch == 2:
        print(search_item(int(input("ID: "))))
    elif ch == 3:
        update_stock(int(input("ID: ")), int(input("Stock: ")))
    elif ch == 4:
        check_low_stock()
    elif ch == 5:
        generate_report()
    elif ch == 6:
        sort_items()
    elif ch == 7:
        vendor_report()
    elif ch == 8:
        plot_bar()
    elif ch == 9:
        plot_pie()
    elif ch == 10:
        add_item()
    elif ch == 11:
        remove_item()
    elif ch == 12:
        break