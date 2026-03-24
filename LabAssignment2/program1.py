V = float(input("Enter voltage (V): "))
R = float(input("Enter resistance (R): "))

if R == 0:
    print("Resistance cannot be zero.")
else:
    I = V / R

    print(f"Current (I) = {I:.2f} A")

    if I < 0.5:
        print("Low current")
    elif 0.5 <= I <= 2:
        print("Normal current")
    else:
        print("High current")