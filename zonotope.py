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
     def split(self):
        # Obliczenie hiperpłaszczyzn
        plane_normals = np.eye(self.center.size)

        # Przesunięcie płaszczyzn do centrum zonotypu
        plane_offsets = np.dot(plane_normals, self.center)

        left_half_vertices = []
        right_half_vertices = []
        for vertex in self.hypercube.vertices:
            if np.all(np.dot(plane_normals, vertex) - plane_offsets <= 0):
                left_half_vertices.append(vertex)
            else:
                right_half_vertices.append(vertex)

        left_half = zonotope(np.mean(np.array(left_half_vertices), axis=0), self.generators)
        right_half = zonotope(np.mean(np.array(right_half_vertices), axis=0), self.generators)

        return left_half, right_half
    
    def combine(self, other):
        combined_vertices = np.concatenate((self.hypercube.vertices, other.hypercube.vertices), axis=0)
        combined_center = np.mean(combined_vertices, axis=0)
        return zonotope(combined_center, self.generators)

def compute_do_di(zonotope, norm='euclidean'):
    generators = zonotope.generators

    K = generators.shape[1] 
    m = generators.shape[0]  

    A_eq = generators.T
    b_eq = np.ones(K)
    c = np.zeros(m)

    if norm == 'euclidean':
        res_do = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(None, None)] * m)
        do_x = res_do.fun

    elif norm == 'manhattan':
        res_do = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * m)
        do_x = res_do.fun

    else:
        raise ValueError("Invalid norm. Please choose from 'euclidean', 'manhattan'")

    di_x = np.inf
    for i in range(m):
        res_di = linprog(-generators[i], A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * m)
        di_i = res_di.fun
        di_x = min(di_x, di_i)

    return do_x, di_x

def branch_and_prune(zonotope_obj, depth=0, MAX_DEPTH=10, norm='manhattan'):
    if depth >= MAX_DEPTH:
        return zonotope_obj 

    do_x, di_x = compute_do_di(zonotope_obj, norm)

    if do_x > di_x:
        return zonotope(zonotope_obj.center, np.zeros_like(zonotope_obj.generators))

    if depth == 0:
        print(f"At depth {depth}, do(x) = {do_x}, di(x) = {di_x}")

    left_half, right_half = zonotope_obj.split()

    left_result = branch_and_prune(left_half, depth + 1, MAX_DEPTH)
    right_result = branch_and_prune(right_half, depth + 1, MAX_DEPTH)

    return left_result.combine(right_result)
    
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


result = branch_and_prune(Z)
print("Combined Zonotope Center:", result.center)
print("Combined Zonotope Vertices:", result.hypercube.vertices)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
input_vertices = Z.vertices
result_vertices = result.vertices
input_x, input_y, input_z = input_vertices[:, 0], input_vertices[:, 1], input_vertices[:, 2]
result_x, result_y, result_z = result_vertices[:, 0], result_vertices[:, 1], result_vertices[:, 2]
ax.scatter(input_x, input_y, input_z, c='blue', label='Input Zonotope')
ax.scatter(result_x, result_y, result_z, c='red', label='Pruned and Combined Zonotope')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Pruned and Combined Zonotope')
ax.legend()
plt.show()
