name = input("Enter employee name: ")
emp_id = input("Enter employee ID: ")
department = input("Enter department: ")
basic_salary = float(input("Enter basic salary: "))

da = 0.92 * basic_salary
hra = 0.58 * basic_salary
ta = 0.30 * basic_salary
lic = 500

gross_salary = basic_salary + da + hra + ta
net_salary = gross_salary - lic

print("Employee Details")
print("Name:", name)
print("Employee ID:", emp_id)
print("Department:", department)
print("Basic Salary:", basic_salary)
print("DA:", da)
print("HRA:", hra)
print("TA:", ta)
print("LIC Deduction:", lic)
print("Gross Salary:", gross_salary)
print("Net Salary:", net_salary)