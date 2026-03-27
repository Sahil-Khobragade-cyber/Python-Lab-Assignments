balance = 0.0

def display_balance():
    print("Current Balance:", balance)

def deposit():
    global balance
    amt = float(input("Enter amount to deposit: "))
    if amt > 0:
        balance += amt
        print("Deposited:", amt)
    else:
        print("Invalid amount")

def withdraw():
    global balance
    amt = float(input("Enter amount to withdraw: "))
    if amt <= balance and amt > 0:
        balance -= amt
        print("Withdrawn:", amt)
    else:
        print("Insufficient balance or invalid amount")

while True:
    print("\n1.Display Balance 2.Deposit 3.Withdraw 4.Exit")
    ch = input("Enter choice: ")

    if ch == "1":
        display_balance()
    elif ch == "2":
        deposit()
    elif ch == "3":
        withdraw()
    elif ch == "4":
        break
    else:
        print("Invalid choice")