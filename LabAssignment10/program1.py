import pandas as pd

df = pd.read_csv("books.csv")

print("\nComplete Report:\n")
print(df.to_string(index=False))

author = input("\nEnter author name: ")
print("\nBooks by Author:\n")
print(df[df["author"] == author].to_string(index=False))

publisher = input("\nEnter publishing house: ")
print("\nBooks by Publishing House:\n")
print(df[df["publishing_house"] == publisher].to_string(index=False))

cheapest = df[df["price"] == df["price"].min()]
costliest = df[df["price"] == df["price"].max()]
print("\nCheapest Book:\n")
print(cheapest[["title"]].to_string(index=False))
print("\nCostliest Book:\n")
print(costliest[["title"]].to_string(index=False))

print("\nSorted by Publication Year:\n")
print(df.sort_values(by="publication_year").to_string(index=False))