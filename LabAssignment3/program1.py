students = []

def add_student():
    sid = input("Enter ID: ")
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    students.append({"id": sid, "name": name, "age": age})
    print("Student added")

def view_students():
    if not students:
        print("No students found")
    else:
        for s in students:
            print(s)

def update_student():
    sid = input("Enter ID to update: ")
    for s in students:
        if s["id"] == sid:
            s["name"] = input("Enter new name: ")
            s["age"] = input("Enter new age: ")
            print("Updated")
            return
    print("Student not found")

def delete_student():
    sid = input("Enter ID to delete: ")
    for s in students:
        if s["id"] == sid:
            students.remove(s)
            print("Deleted")
            return
    print("Student not found")

def search_student():
    choice = input("Search by 1.ID 2.Name: ")
    if choice == "1":
        sid = input("Enter ID: ")
        for s in students:
            if s["id"] == sid:
                print(s)
                return
    else:
        name = input("Enter Name: ")
        for s in students:
            if s["name"].lower() == name.lower():
                print(s)
                return
    print("Not found")

while True:
    print("\n1.Add 2.View 3.Update 4.Delete 5.Search 6.Exit")
    ch = input("Enter choice: ")
    if ch == "1":
        add_student()
    elif ch == "2":
        view_students()
    elif ch == "3":
        update_student()
    elif ch == "4":
        delete_student()
    elif ch == "5":
        search_student()
    elif ch == "6":
        break
    else:
        print("Invalid choice")