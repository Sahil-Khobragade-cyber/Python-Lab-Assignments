import pandas as pd

data = {
    "State": ["Maharashtra", "Uttar Pradesh", "Rajasthan", "Gujarat", "Tamil Nadu"],
    "Area": [307713, 243286, 342239, 196244, 130058],
    "Population": [112374333, 199812341, 68548437, 60439692, 72147030]
}

df = pd.DataFrame(data)

print("\nComplete Information:\n")
print(df.to_string(index=False))

print("\nState with Largest Area:\n")
print(df.loc[df["Area"].idxmax(), "State"])

print("\nState with Largest Population:\n")
print(df.loc[df["Population"].idxmax(), "State"])

df["Density"] = df["Population"] / df["Area"]

print("\nPopulation Density:\n")
print(df[["State", "Density"]].to_string(index=False))

print("\nState with Highest Population Density:\n")
print(df.loc[df["Density"].idxmax(), "State"])