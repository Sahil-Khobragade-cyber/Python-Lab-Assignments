import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("recruitment.csv")

plt.figure()
plt.bar(df["Company"], df["Recruitments"])
plt.xlabel("Company")
plt.ylabel("Number of Recruitments")
plt.title("New Recruitments by Company")
plt.xticks(rotation=45)
plt.show()

plt.figure()
plt.pie(df["Recruitments"], labels=df["Company"], autopct="%1.1f%%")
plt.title("Recruitments Distribution")
plt.show()

plt.figure()
colors = ["gold","lightcoral","lightskyblue","lightgreen","pink","cyan","orange","violet"]
explode = [0.1 if i == df["Recruitments"].idxmax() else 0 for i in range(len(df))]
plt.pie(df["Recruitments"], labels=df["Company"], autopct="%1.1f%%", colors=colors, explode=explode, shadow=True)
plt.title("Customized Pie Chart")
plt.show()

plt.figure()
plt.pie(df["Recruitments"], labels=df["Company"], autopct="%1.1f%%")
centre_circle = plt.Circle((0,0),0.70,fc="white")
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title("Doughnut Chart")
plt.show()

ibm = df[df["Company"] == "IBM"]["Recruitments"].values[0]
amdocs = df[df["Company"] == "Amdocs"]["Recruitments"].values[0]

plt.figure()
plt.bar(["IBM","Amdocs"], [ibm, amdocs])
plt.xlabel("Company")
plt.ylabel("Number of Recruitments")
plt.title("IBM vs Amdocs Recruitment Comparison")
plt.show()