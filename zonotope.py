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
        self.vertices = self.__getvertices()

    def __getvertices(self):
        return self.hypercube.vertices + np.dot(self.generators, self.hypercube.vertices.T).T
    
    def translate(self, vector):
        self.center += vector
        self.vertices += vector

    def contains(self, point):
        return np.all(np.abs(point - self.center) <= np.sum(np.abs(self.generators), axis=1))
    
    def calculate_distance(self, other):
        if isinstance(other, zonotope):
            return np.linalg.norm(self.center - other.center)
        else:
            return np.linalg.norm(self.center - other)
    
    
G_rotate = np.array([[1, 0, 1],
                [0, cos(45), -sin(45)],
                [0, sin(45), cos(45)]])

G_scale = np.array([[2, 0, 0],
                [0, 2, 0],
                [0, 0, 2]])

Z = zonotope(np.array([0, 0, 0]), G_scale)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
points = Z.vertices
ax.scatter(points[:, 0], points[:, 1], points[:, 2])
plt.show()