from scipy.linalg import orthogonal_procrustes
import numpy as np

def standard_normalization(shape):
    shape = shape.astype(float)
    shape -= np.mean(shape, axis=0)
    shape /= np.sqrt((shape**2).sum())
    return shape

def procrustes_distance(mtx1, mtx2):
    R, s = orthogonal_procrustes(mtx1, mtx2)
    mtx2 = np.dot(mtx2, R.T) * s
    return np.sum(np.square(mtx1 - mtx2))

def similarity(distance):
    return max(1-round(distance,3),0)

class Bruteforce:
    def __init__(self, space, distance=procrustes_distance):
        self.space = space
        self.distance = distance
    def query(self, X, k=1, return_distance=False):
        n = len(self.space)
        X = standard_normalization(X)
        distances = np.zeros(n)
        for i in range(n):
            distances[i] = self.distance(X, self.space[i]['matrix'])
        nearest_indices = np.argsort(distances)[:k]
        return distances[nearest_indices], nearest_indices
    def classify(self, matrix, threshold=0.96):
        distances, indices = self.query(matrix)
        if similarity(distances[0]) >= threshold:
           return self.space[indices][0]['name']
        return " "
    
