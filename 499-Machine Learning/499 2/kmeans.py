import math
import numpy

def assign_clusters(data, cluster_centers):
    """
    Assigns every data point to its closest (in terms of euclidean distance) cluster center.
    :param data: An (N, D) shaped numpy array where N is the number of examples
    and D is the dimension of the data
    :param cluster_centers: A (K, D) shaped numpy array where K is the number of clusters
    and D is the dimension of the data
    :return: An (N, ) shaped numpy array. At its index i, the index of the closest center
    resides to the ith data point.
    """
    closestCenter = []
    for d in data:
        distances = []
        for centers in cluster_centers:
            eu = 0
            for i in range(len(d)):
                eu = eu + (d[i] - centers[i]) ** 2
            distances.append(math.sqrt(eu))
        closestCenter.append(distances.index(min(distances)))
    return numpy.array(closestCenter)

def calculate_cluster_centers(data, assignments, cluster_centers, k):
    """
    Calculates cluster_centers such that their squared euclidean distance to the data assigned to
    them will be lowest.
    If none of the data points belongs to some cluster center, then assign it to its previous value.
    :param data: An (N, D) shaped numpy array where N is the number of examples
    and D is the dimension of the data
    :param assignments: An (N, ) shaped numpy array with integers inside. They represent the cluster index
    every data assigned to.
    :param cluster_centers: A (K, D) shaped numpy array where K is the number of clusters
    and D is the dimension of the data
    :param k: Number of clusters
    :return: A (K, D) shaped numpy array that contains the newly calculated cluster centers.
    """
    newCenters = []
    clusters = []
    for i in range(k):
        clusterDatas = []
        clusters.append(clusterDatas)
    for i in range(len(assignments)):
        clusters[assignments[i]].append(data[i])
    for i in range(len(clusters)):
        if len(clusters[i]) == 0:
            newCenters.append(cluster_centers[i])
        else:
            center = []
            dim = data.shape[1]
            for j in range(dim):
                axisDatas = []
                for d in clusters[i]:
                    axisDatas.append(d[j])
                center.append(sum(axisDatas) / len(axisDatas))
            newCenters.append(center)
    return numpy.array(newCenters)




def kmeans(data, initial_cluster_centers):
    """
    Applies k-means algorithm.
    :param data: An (N, D) shaped numpy array where N is the number of examples
    and D is the dimension of the data
    :param initial_cluster_centers: A (K, D) shaped numpy array where K is the number of clusters
    and D is the dimension of the data
    :return: cluster_centers, objective_function
    cluster_center.shape is (K, D).
    objective function is a float. It is calculated by summing the squared euclidean distance between
    data points and their cluster centers.
    """
    centers = initial_cluster_centers
    while True:
        assignments = assign_clusters(data, centers)
        newCenters = calculate_cluster_centers(data, assignments, centers, len(centers))
        if(newCenters == centers).all():
            break
        else:
            centers = newCenters
    objectiveFunc = 0
    for i in range(len(data)):
        eu = 0
        for j in range(len(data[i])):
            eu += (data[i][j] - centers[assignments[i]][j]) ** 2
        objectiveFunc += eu

    return centers, objectiveFunc