data = tuple(map(int, input("Enter integers separated by space: ").split()))

print("Total items:", len(data))
print("Last item:", data[-1] if data else "Tuple is empty")
print("Reverse order:", data[::-1])
print("Yes" if 5 in data else "No")

result = sorted(data[1:-1]) if len(data) > 2 else []
print("After removing first and last, sorted:", result)