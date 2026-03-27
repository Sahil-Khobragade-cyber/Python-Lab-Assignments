class Employee:
    def __init__(self):
        self.name = ""
        self.age = 0
        self.salary = 0.0
        self.address = ""

    def get_data(self):
        self.name = input("Enter name: ")
        self.age = int(input("Enter age: "))
        self.salary = float(input("Enter salary: "))
        self.address = input("Enter address: ")

    def display(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("Salary:", self.salary)
        print("Address:", self.address)


class Manager(Employee):
    pass


managers = []

for i in range(10):
    print(f"\nEnter details of Manager {i+1}:")
    m = Manager()
    m.get_data()
    managers.append(m)

print("\nManager Details:")
for m in managers:
    m.display()
    print()