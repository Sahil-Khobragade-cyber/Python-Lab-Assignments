class Book:
    def __init__(self, bid, title, author):
        self.bid = bid
        self.title = title
        self.author = author
        self.available = True

    def display(self):
        status = "Available" if self.available else "Lent"
        print(self.bid, self.title, self.author, status)


class Member:
    def __init__(self, mid, name):
        self.mid = mid
        self.name = name
        self.books = []

    def display(self):
        print(self.mid, self.name, self.books)


class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self):
        bid = input("Enter Book ID: ")
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        self.books[bid] = Book(bid, title, author)

    def add_member(self):
        mid = input("Enter Member ID: ")
        name = input("Enter Name: ")
        self.members[mid] = Member(mid, name)

    def lend_book(self):
        bid = input("Enter Book ID: ")
        mid = input("Enter Member ID: ")
        if bid in self.books and mid in self.members:
            book = self.books[bid]
            if book.available:
                book.available = False
                self.members[mid].books.append(bid)
                print("Book lent")
            else:
                print("Book not available")
        else:
            print("Invalid IDs")

    def return_book(self):
        bid = input("Enter Book ID: ")
        mid = input("Enter Member ID: ")
        if bid in self.books and mid in self.members:
            book = self.books[bid]
            if bid in self.members[mid].books:
                book.available = True
                self.members[mid].books.remove(bid)
                print("Book returned")
            else:
                print("This member does not have the book")
        else:
            print("Invalid IDs")

    def display_books(self):
        for b in self.books.values():
            b.display()


lib = Library()

while True:
    print("\n1.Add Book 2.Add Member 3.Lend Book 4.Return Book 5.Display Books 6.Exit")
    ch = input("Enter choice: ")

    if ch == "1":
        lib.add_book()
    elif ch == "2":
        lib.add_member()
    elif ch == "3":
        lib.lend_book()
    elif ch == "4":
        lib.return_book()
    elif ch == "5":
        lib.display_books()
    elif ch == "6":
        break
    else:
        print("Invalid choice")