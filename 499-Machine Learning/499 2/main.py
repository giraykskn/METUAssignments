import numpy as np
import matplotlib.pyplot as plt

from hac import hac, single_linkage, complete_linkage, average_linkage, centroid_linkage
from kmeans import kmeans, assign_clusters
from knn import cross_validation, knn

def knnMain():
    k_fold = 10
    train_data = np.load('hw2_data/knn/train_data.npy')
    train_labels = np.load('hw2_data/knn/train_labels.npy')
    test_data = np.load('hw2_data/knn/test_data.npy')
    test_labels = np.load('hw2_data/knn/test_labels.npy')
    accuracies = []
    for k in range(1, 200):
        accuracies.append(cross_validation(train_data, train_labels, k, k_fold))
    best = knn(train_data, train_labels, test_data, test_labels, accuracies.index(max(accuracies)))
    print("Accuracy of the best k, which is", accuracies.index(max(accuracies)), ", is",best)
    plt.plot(range(1, 200), accuracies)
    plt.ylabel("Average Accuracy")
    plt.xlabel("k")
    plt.show()

def kmeansMain():
    kmax = 10
    clustering = []
    clustering.append(np.load('hw2_data/kmeans/clustering1.npy'))
    clustering.append(np.load('hw2_data/kmeans/clustering2.npy'))
    clustering.append(np.load('hw2_data/kmeans/clustering3.npy'))
    clustering.append(np.load('hw2_data/kmeans/clustering4.npy'))
    iterator = 1
    bests = [2, 3, 4, 5]
    for cluster in clustering:
        transposed = np.transpose(cluster)
        mins = []
        maxs = []
        for dim in transposed:
            mins.append(min(dim))
            maxs.append(max(dim))
        bestObjs = []
        for k in range(1, kmax + 1):
            objs = []
            for init in range(k):
                centers = []
                for i in range(k):
                    data = []
                    for j in range(len(mins)):
                        data.append(np.random.uniform(mins[j], maxs[j]))
                    centers.append(data)
                _, obj = kmeans(cluster, np.array(centers))
                objs.append(obj)
            bestObjs.append(min(objs))
        plt.plot(range(1, kmax + 1), bestObjs)
        plt.ylabel("Value of Objective Function")
        plt.xlabel("k")
        plt.title("Cluster " + str(iterator))
        plt.show()

        k = bests[iterator - 1]
        centers2 = []
        for i in range(k):
            data2 = []
            for j in range(len(mins)):
                data2.append(np.random.uniform(mins[j], maxs[j]))
            centers2.append(data2)
        resCenters, _ = kmeans(cluster, np.array(centers2))
        assignments = assign_clusters(cluster, resCenters)
        assigned = []
        assigned2 = []
        for i in range(k):
            assigned.append([])
        for i in range(len(cluster)):
            assigned[assignments[i]].append(cluster[i])
        for arr in assigned:
            assigned2.append(np.array(arr))
        plt.clf()
        colors = ['or', 'ok', 'ob', 'og', 'oy']
        for i in range(k):
            plt.plot(assigned2[i][:, 0], assigned2[i][:, 1], colors[i])
        plt.title("K-means Clusters")
        plt.show()
        iterator += 1


def hacMain():
    datas = []
    criterion = [(single_linkage, "Single Linkage"), (complete_linkage, "Complete Linkage"),
                 (average_linkage, "Average Linkage"), (centroid_linkage, "Centroid Linkaage")]
    datas.append((np.load('hw2_data/hac/data1.npy'), 2))
    datas.append((np.load('hw2_data/hac/data2.npy'), 2))
    datas.append((np.load('hw2_data/hac/data3.npy'), 2))
    datas.append((np.load('hw2_data/hac/data4.npy'), 4))

    for data, k in datas:
        for criteria, name in criterion:
            hacData = hac(data, criteria, k)
            if k == 2:
                plt.clf()
                plt.plot(hacData[0][:, 0], hacData[0][:, 1], 'or')
                plt.plot(hacData[1][:, 0], hacData[1][:, 1], 'ok')
                plt.title(name)
                plt.show()
            else:
                plt.clf()
                plt.plot(hacData[0][:, 0], hacData[0][:, 1], 'or')
                plt.plot(hacData[1][:, 0], hacData[1][:, 1], 'ok')
                plt.plot(hacData[2][:, 0], hacData[2][:, 1], 'ob')
                plt.plot(hacData[3][:, 0], hacData[3][:, 1], 'og')
                plt.title(name)
                plt.show()

if __name__ == '__main__':
    #knnMain()
    #kmeansMain()
    hacMain()
