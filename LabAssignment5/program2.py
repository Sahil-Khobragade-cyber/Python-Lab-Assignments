prices = tuple(map(float, input("Enter item prices separated by space: ").split()))

print("Total items sold:", len(prices))
print("Cheapest item price:", min(prices) if prices else "No data")
print("Costliest item price:", max(prices) if prices else "No data")
print("Prices in ascending order:", sorted(prices))

if prices:
    max_price = max(prices)
    count = prices.count(max_price)
    print("Number of costliest items sold:", count)
else:
    print("Number of costliest items sold: 0")