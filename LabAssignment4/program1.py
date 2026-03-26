import numpy as np

identity_matrix = np.eye(4)
print("4x4 Identity Matrix:\n", identity_matrix)

A = np.random.randint(1, 10, (3, 3))
B = np.random.randint(1, 10, (3, 3))

print("\nMatrix A:\n", A)
print("\nMatrix B:\n", B)

addition = A + B
print("\nAddition (A + B):\n", addition)

multiplication = np.dot(A, B)
print("\nMultiplication (A * B):\n", multiplication)