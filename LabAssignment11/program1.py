import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales_data.csv")

plt.figure()
plt.plot(df["month_number"], df["total_profit"])
plt.xlabel("Month Number")
plt.ylabel("Total Profit")
plt.title("Total Profit per Month")
plt.show()

plt.figure()
plt.plot(df["month_number"], df["facecream"])
plt.plot(df["month_number"], df["facewash"])
plt.plot(df["month_number"], df["toothpaste"])
plt.plot(df["month_number"], df["bathingsoap"])
plt.plot(df["month_number"], df["shampoo"])
plt.plot(df["month_number"], df["moisturizer"])
plt.xlabel("Month Number")
plt.ylabel("Sales Units")
plt.title("Product Sales Data")
plt.show()

plt.figure()
x = df["month_number"]
width = 0.35
plt.bar(x - width/2, df["facecream"], width=width)
plt.bar(x + width/2, df["facewash"], width=width)
plt.xlabel("Month Number")
plt.ylabel("Sales Units")
plt.title("Facecream and Facewash Sales")
plt.show()

totals = [
    df["facecream"].sum(),
    df["facewash"].sum(),
    df["toothpaste"].sum(),
    df["bathingsoap"].sum(),
    df["shampoo"].sum(),
    df["moisturizer"].sum()
]

labels = ["facecream", "facewash", "toothpaste", "bathingsoap", "shampoo", "moisturizer"]

plt.figure()
plt.pie(totals, labels=labels, autopct="%1.1f%%")
plt.title("Total Sales Distribution")
plt.show()