import math
import numpy
import sys

def calculate_distances(train_data, test_datum):
    """
    Calculates euclidean distances between test_datum and every train_data
    :param train_data: An (N, D) shaped numpy array where N is the number of examples
    and D is the dimension of the data
    :param test_datum: A (D, ) shaped numpy array
    :return: An (N, ) shaped numpy array that contains distances
    """
    result = []
    for data in train_data:
        eu = 0
        for i in range(len(data)):
            eu = eu + (data[i] - test_datum[i]) ** 2
        result.append(math.sqrt(eu))

    return numpy.array(result)

def majority_voting(distances, labels, k):
    """
    Applies majority voting. If there are more then one major class, returns the smallest label.
    :param distances: An (N, ) shaped numpy array that contains distances
    :param labels: An (N, ) shaped numpy array that contains labels
    :param k: An integer. The number of nearest neighbor to be selected.
    :return: An integer. The label of the majority class.
    """
    indexes = []
    newDistance = []
    indexLabel = []
    counts = []
    chosenLabels = []
    for i in distances:
        newDistance.append(i)

    for ep in range(k):
        indexes.append(newDistance.index(min(newDistance)))
        newDistance[newDistance.index(min(newDistance))] = sys.float_info.max

    for i in indexes:
        indexLabel.append(labels[i])

    for i in indexLabel:
        counts.append(indexLabel.count(i))

    amount = counts.count(max(counts))
    maxC = max(counts)
    for label in range(amount):
        chosenLabels.append(indexLabel[counts.index(maxC)])
        counts[counts.index(maxC)] = -1
    return min(chosenLabels)

def knn(train_data, train_labels, test_data, test_labels, k):
    """
    Calculates accuracy of knn on test data using train_data.
    :param train_data: An (N, D) shaped numpy array where N is the number of examples
    and D is the dimension of the data
    :param train_labels: An (N, ) shaped numpy array that contains labels
    :param test_data: An (M, D) shaped numpy array where M is the number of examples
    and D is the dimension of the data
    :param test_labels: An (M, ) shaped numpy array that contains labels
    :param k: An integer. The number of nearest neighbor to be selected.
    :return: A float. The calculated accuracy.
    """
    distances = []
    predictions = []
    result = []
    for testData in test_data:
        distances.append(calculate_distances(train_data, testData))

    for distance in distances:
        predictions.append(majority_voting(distance, train_labels, k))

    for i in range(len(predictions)):
        if predictions[i] == test_labels[i]:
            result.append(1)
        else:
            result.append(0)
    return sum(result)/len(result)

def split_train_and_validation(whole_train_data, whole_train_labels, validation_index, k_fold):
    """
    Splits training dataset into k and returns the validation_indexth one as the
    validation set and others as the training set. You can assume k_fold divides N.
    :param whole_train_data: An (N, D) shaped numpy array where N is the number of examples
    and D is the dimension of the data
    :param whole_train_labels: An (N, ) shaped numpy array that contains labels
    :param validation_index: An integer. 0 <= validation_index < k_fold. Specifies which fold
    will be assigned as validation set.
    :param k_fold: The number of groups that the whole_train_data will be divided into.
    :return: train_data, train_labels, validation_data, validation_labels
    train_data.shape is (N-N/k_fold, D).
    train_labels.shape is (N-N/k_fold, ).
    validation_data.shape is (N/k_fold, D).
    validation_labels.shape is (N/k_fold, ).
    """
    train_data = []
    train_labels = []
    validation_data = []
    validation_labels = []
    for data in whole_train_data:
        train_data.append(data)
    for label in whole_train_labels:
        train_labels.append(label)
    indexArray = range(len(whole_train_data))
    indexes = numpy.array(indexArray)
    #numpy.random.shuffle(indexes)
    size = len(whole_train_labels)
    toPop = []
    for i in range(int(size/k_fold)):
        validation_data.append(train_data[indexes[validation_index * int(size / k_fold) + i]])
        validation_labels.append(train_labels[indexes[validation_index * int(size / k_fold) + i]])
        toPop.append(indexes[validation_index * int(size / k_fold) + i])
    for index in toPop:
        train_data.pop(index)
        train_labels.pop(index)
        for j in range(len(toPop)):
            if index < toPop[j]:
                toPop[j] -= 1
    return numpy.array(train_data), numpy.array(train_labels), numpy.array(validation_data), numpy.array(validation_labels)

def cross_validation(whole_train_data, whole_train_labels, k, k_fold):
    """
    Applies k_fold cross-validation and averages the calculated accuracies.
    :param whole_train_data: An (N, D) shaped numpy array where N is the number of examples
    and D is the dimension of the data
    :param whole_train_labels: An (N, ) shaped numpy array that contains labels
    :param k: An integer. The number of nearest neighbor to be selected.
    :param k_fold: An integer.
    :return: A float. Average accuracy calculated.
    """
    accuracy = []
    for i in range(k_fold):
        td, tl, vd, vl = split_train_and_validation(whole_train_data, whole_train_labels, i, k_fold)
        accuracy.append(knn(td, tl, vd, vl, k))

    return sum(accuracy)/len(accuracy)
