def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    return "Cannot divide by zero" if b == 0 else a / b

def mod(a, b):
    return "Cannot mod by zero" if b == 0 else a % b

while True:
    print("\n1.Addition 2.Subtraction 3.Multiplication 4.Division 5.Modulus 6.Exit")
    ch = input("Enter choice: ")

    if ch == "6":
        break

    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    if ch == "1":
        print("Result:", add(a, b))
    elif ch == "2":
        print("Result:", sub(a, b))
    elif ch == "3":
        print("Result:", mul(a, b))
    elif ch == "4":
        print("Result:", div(a, b))
    elif ch == "5":
        print("Result:", mod(a, b))
    else:
        print("Invalid choice")