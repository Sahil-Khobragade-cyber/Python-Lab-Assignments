import pandas as pd

inventory_data = {
    "ITEM_ID": ["C101", "C102", "C103", "C104", "C105"],
    "ITEM_NAME": ["Denim Jeans", "Cotton Shirt", "Silk Saree", "Woolen Sweater", "Sports T-Shirt"],
    "CATEGORY": ["Bottomwear", "Topwear", "Ethnicwear", "Winterwear", "Active Wear"],
    "PRICE": [1500, 1200, 5000, 2000, 800],
    "STOCK": [30, 50, 20, 15, 60],
    "SUPPLIER": ["Levis", "Raymond", "Fabindia", "Spark", "Nike"]
}

supplier_data = {
    "SUPPLIER_ID": ["S201", "S202", "S203", "S204", "S205"],
    "SUPPLIER_NAME": ["Levi's", "Raymond", "Fabindia", "Monte Carlo", "Nike"],
    "CONTACT": [9876543210, 9123456789, 9988776655, 9345678123, 9234567890],
    "LOCATION": ["Mumbai", "Delhi", "Bangalore", "Chandigarh", "Pune"]
}

df_inventory = pd.DataFrame(inventory_data)
df_suppliers = pd.DataFrame(supplier_data)

print(df_inventory)
print("\n")
print(df_suppliers)