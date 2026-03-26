import numpy as np

A = []
print("Enter elements for 5x3 matrix:")
for i in range(5):
    row = list(map(int, input().split()))
    A.append(row)

B = []
print("Enter elements for 3x2 matrix:")
for i in range(3):
    row = list(map(int, input().split()))
    B.append(row)

A = np.array(A)
B = np.array(B)

product = np.dot(A, B)

print("Product matrix:")
print(product)