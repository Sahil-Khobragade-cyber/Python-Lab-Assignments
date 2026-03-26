items = list(map(int, input("Enter item numbers separated by space: ").split()))

print("Total items:", len(items))

if items:
    print("Last item:", items[-1])
else:
    print("List is empty")

print("Sorted list:", sorted(items))

print("Yes" if 515 in items else "No")

items.extend([121, 321])
items.sort()

print("Updated list:", items)