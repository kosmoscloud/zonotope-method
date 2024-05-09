import numpy as np
from math import sin, cos
import matplotlib.pyplot as plt

class hypercube:
    def __init__(self, center):
        self.center = center
        self.dimensionality = len(center)
        self.vertices = self.__getvertices()

    def __getvertices(self):
        points = np.zeros((2**self.dimensionality, self.dimensionality))
        for i in range(2**self.dimensionality):
            for j in range(self.dimensionality):
                if i & (1 << j):
                    points[i][j] = 1
        points[points == 0] = -1
        points += self.center
        return points

class zonotope:
    def __init__(self, center, generators):
        self.center = center
        self.generators = generators
        self.hypercube = hypercube(center)
    
G = np.array([[1, 0, 1],
                [0, cos(45), -sin(45)],
                [0, sin(45), cos(45)]])

Z = zonotope(np.array([0, 0, 0]), G)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
points = Z.hypercube.vertices
ax.scatter(points[:, 0], points[:, 1], points[:, 2])
plt.show()