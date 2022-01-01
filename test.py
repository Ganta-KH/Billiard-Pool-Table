import numpy as np


U = np.array([
        [5, 0, 70],
        [0, 5, 50],
        [0, 0, 1]
    ])

N1 = np.array([
    [1, 1, 10],
    [2, 3, -8],
    [3, 1, 0],
    [10, -2, 4],
])

N2 = np.array([
    [6, 6, 6],
    [5, 5, 5],
    [7, 7, 7]
])

N1 -= np.array([1,1, 1])
print(np.dot(U, N1.transpose()))

print(np.dot(U, N1.T))