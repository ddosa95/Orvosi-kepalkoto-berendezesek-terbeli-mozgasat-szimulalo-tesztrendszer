
import numpy as np


def rotate(vector, rotation):
    x_rotation_matrix = np.array([[1, 0, 0],
                                  [0, np.cos(rotation[0]), -1 * np.sin(rotation[0])],
                                  [0, np.sin(rotation[0]), np.cos(rotation[0])]])

    y_rotation_matrix = np.array([[np.cos(rotation[1]), 0, np.sin(rotation[1])],
                                  [0, 1, 0],
                                  [-1 * np.sin(rotation[1]), 0, np.cos(rotation[1])]])

    z_rotation_matrix = np.array([[np.cos(rotation[2]), -1 * np.sin(rotation[2]), 0],
                                  [np.sin(rotation[2]), np.cos(rotation[2]), 0],
                                  [0, 0, 1]])

    coordinates = np.matmul(y_rotation_matrix, np.matmul(x_rotation_matrix, np.matmul(z_rotation_matrix, vector)))
    return coordinates


def shift(vector, position):
    coordinates = np.add(vector, position)
    return coordinates
