import pandas as pd

data1 = {
    "EMPNO": ["E101", "E102", "E103", "E105", "E106"],
    "EMP_NAME": ["Vivek", "Vishal", "Priyal", "Shrushti", "Pranay"],
    "DEPT_NAME": ["R & D", "Marketing", "Product Development", "Product Development", "Product Development"],
    "SALARY": [145000, 90000, 120000, 80000, 100000],
    "BRANCH": ["Nagpur", "Pune", "Bangalore", "Nagpur", "Mumbai"]
}

data2 = {
    "EMPNO": ["E101", "E102", "E103", "E105", "E106"],
    "DESIGNATION": ["Project Manager", "Sales Manager", "Design Architect", "Software Developer", "Project Lead"]
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
employee_table = pd.merge(df1, df2, on="EMPNO")

print(employee_table)