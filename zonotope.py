import numpy as np
import matplotlib.pyplot as plt

class zonotope:
    def __init__(self, center, generators):
        self.center = center
        self.generators = generators
        self.dimensionality = len(center)

    # zwraca punkty hiperkostki bez przekształceń (chyba bez przekształceń)
    def gethypercubepoints(self):
        points = np.zeros((2**self.dimensionality, self.dimensionality))
        for i in range(2**self.dimensionality):
            for j in range(self.dimensionality):
                if i & (1 << j):
                    points[i] += self.generators[j]
        points[points == 0] = -1
        points += self.center
        return points
    
G = np.array([[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]])

Z = zonotope(np.array([0, 0, 0]), G)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
points = Z.gethypercubepoints()
ax.scatter(points[:, 0], points[:, 1], points[:, 2])
plt.show()