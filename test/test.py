import numpy as np

l = np.array([[0, 0, 1, 0],
              [2, 3, 3, 4],
              [0, 5, 4, 0]])

dict = {"left": [2, 0, 1], "up": [1, 1, 0, 1], "right": [1, 0, 1], "down": [1, 0, 0, 1]}

print(dict)

#print({"left": ["yes" if i[0] == 0 else "no" for i in l]})