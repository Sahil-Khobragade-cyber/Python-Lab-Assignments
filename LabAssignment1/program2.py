name = input("Enter Vendor Name: ")
year = int(input("Enter Year of Association: "))
contact = input("Enter Contact Number: ")
email = input("Enter Email ID: ")

print("Enter Monthly Purchase Amounts")

total_purchase = 0

for i in range(1, 13):
    amount = float(input("Month " + str(i) + ": "))
    total_purchase += amount

print("Annual Purchase / Billing Report =====")
print("Vendor Name:", name)
print("Year of Association:", year)
print("Contact Number:", contact)
print("Email ID:", email)
print("Total Annual Purchase:", total_purchase)