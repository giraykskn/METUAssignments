import sys
import numpy as np
import math

def single_linkage(c1, c2):
    """
    Given clusters c1 and c2, calculates the single linkage criterion.
    :param c1: An (N, D) shaped numpy array containing the data points in cluster c1.
    :param c2: An (M, D) shaped numpy array containing the data points in cluster c2.
    :return: A float. The result of the calculation.
    """
    distances = []
    for d1 in c1:
        for d2 in c2:
            eu = 0
            for i in range(len(d1)):
                eu += (d1[i] - d2[i]) ** 2
            distances.append(eu)
    return math.sqrt(min(distances))

def complete_linkage(c1, c2):
    """
    Given clusters c1 and c2, calculates the complete linkage criterion.
    :param c1: An (N, D) shaped numpy array containing the data points in cluster c1.
    :param c2: An (M, D) shaped numpy array containing the data points in cluster c2.
    :return: A float. The result of the calculation.
    """
    distances = []
    for d1 in c1:
        for d2 in c2:
            eu = 0
            for i in range(len(d1)):
                eu += (d1[i] - d2[i]) ** 2
            distances.append(eu)
    return math.sqrt(max(distances))

def average_linkage(c1, c2):
    """
    Given clusters c1 and c2, calculates the average linkage criterion.
    :param c1: An (N, D) shaped numpy array containing the data points in cluster c1.
    :param c2: An (M, D) shaped numpy array containing the data points in cluster c2.
    :return: A float. The result of the calculation.
    """
    distances = []
    for d1 in c1:
        for d2 in c2:
            eu = 0
            for i in range(len(d1)):
                eu += (d1[i] - d2[i]) ** 2
            distances.append(math.sqrt(eu))
    return sum(distances) / len(distances)

def centroid_linkage(c1, c2):
    """
    Given clusters c1 and c2, calculates the centroid linkage criterion.
    :param c1: An (N, D) shaped numpy array containing the data points in cluster c1.
    :param c2: An (M, D) shaped numpy array containing the data points in cluster c2.
    :return: A float. The result of the calculation.
    """
    ac1 = np.sum(c1, axis=0) / len(c1)
    ac2 = np.sum(c2, axis=0) / len(c2)
    eu = 0
    for i in range(len(ac1)):
        eu += (ac1[i] - ac2[i]) ** 2
    return math.sqrt(eu)

def hac(data, criterion, stop_length):
    """
    Applies hierarchical agglomerative clustering algorithm with the given criterion on the data
    until the number of clusters reaches the stop_length.
    :param data: An (N, D) shaped numpy array containing all of the data points.
    :param criterion: A function. It can be single_linkage, complete_linkage, average_linkage, or
    centroid_linkage
    :param stop_length: An integer. The length at which the algorithm stops.
    :return: A list of numpy arrays with length stop_length. Each item in the list is a cluster
    and a (Ni, D) sized numpy array.
    """
    hac = []
    for d in data:
        hac.append(np.array([d]))
    while len(hac) > stop_length:
        min = sys.float_info.max
        indexes = -1, -1
        for i in range(len(hac)):
            for j in range(len(hac)):
                if i != j and (j, i) != indexes:
                    linkage = criterion(hac[i], hac[j])
                    if linkage < min:
                        min = linkage
                        indexes = i, j
        new = []
        for d in hac[indexes[0]]:
            new.append(d)
        for d in hac[indexes[1]]:
            new.append(d)
        hac.pop(indexes[0])
        hac.pop(indexes[1] - 1)
        hac.append(np.array(new))
    return hac