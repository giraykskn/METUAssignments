import math
import numpy
import numpy as np


def entropy(bucket):
    """
    Calculates the entropy.
    :param bucket: A list of size num_classes. bucket[i] is the number of
    examples that belong to class i.
    :return: A float. Calculated entropy.
    """
    entropy = 0
    total = sum(bucket)
    for amount in bucket:
        if amount == 0:
            pass
        else:
            entropy += -amount/total * math.log2(amount/total)
    return entropy

def info_gain(parent_bucket, left_bucket, right_bucket):
    """
    Calculates the information gain. A bucket is a list of size num_classes.
    bucket[i] is the number of examples that belong to class i.
    :param parent_bucket: Bucket belonging to the parent node. It contains the
    number of examples that belong to each class before the split.
    :param left_bucket: Bucket belonging to the left child after the split.
    :param right_bucket: Bucket belonging to the right child after the split.
    :return: A float. Calculated information gain.
    """
    gain = entropy(parent_bucket)
    gain -= (sum(left_bucket) / sum(parent_bucket)) * entropy(left_bucket)
    gain -= (sum(right_bucket) / sum(parent_bucket)) * entropy(right_bucket)
    return gain

def gini(bucket):
    """
    Calculates the gini index.
    :param bucket: A list of size num_classes. bucket[i] is the number of
    examples that belong to class i.
    :return: A float. Calculated gini index.
    """
    gini = 1
    for amount in bucket:
        if sum(bucket) == 0:
            pass
        else:
            gini -= (amount / sum(bucket)) ** 2
    return gini

def avg_gini_index(left_bucket, right_bucket):
    """
    Calculates the average gini index. A bucket is a list of size num_classes.
    bucket[i] is the number of examples that belong to class i.
    :param left_bucket: Bucket belonging to the left child after the split.
    :param right_bucket: Bucket belonging to the right child after the split.
    :return: A float. Calculated average gini index.
    """
    avg = 0
    total = sum(left_bucket) + sum(right_bucket)
    avg += (sum(left_bucket) / total) * gini(left_bucket)
    avg += (sum(right_bucket) / total) * gini(right_bucket)
    return avg

def calculate_split_values(data, labels, num_classes, attr_index, heuristic_name):
    """
    For every possible values to split the data for the attribute indexed by
    attribute_index, it divides the data into buckets and calculates the values
    returned by the heuristic function named heuristic_name. The split values
    should be the average of the closest 2 values. For example, if the data has
    2.1 and 2.2 in it consecutively for the values of attribute index by attr_index,
    then one of the split values should be 2.15.
    :param data: An (N, M) shaped numpy array. N is the number of examples in the
    current node. M is the dimensionality of the data. It contains the values for
    every attribute for every example.
    :param labels: An (N, ) shaped numpy array. It contains the class values in
    it. For every value, 0 <= value < num_classes.
    :param num_classes: An integer. The number of classes in the dataset.
    :param attr_index: An integer. The index of the attribute that is going to
    be used for the splitting operation. This integer indexs the second dimension
    of the data numpy array.
    :param heuristic_name: The name of the heuristic function. It should either be
    'info_gain' of 'avg_gini_index' for this homework.
    :return: An (L, 2) shaped numpy array. L is the number of split values. The
    first column is the split values and the second column contains the calculated
    heuristic values for their splits.
    """
    dataAttr = data[:, attr_index]
    splitValues = []
    sorted = numpy.sort(dataAttr)
    for i in range(len(dataAttr) - 1):
        splitValues.append([(sorted[i + 1] + sorted[i]) / 2])
    for split in splitValues:
        parentBucket = []
        leftBucket = []
        rightBucket = []
        for l in range(num_classes):
            parentBucket.append(0)
            leftBucket.append(0)
            rightBucket.append(0)
        for d in range(len(dataAttr)):
            for l in range(num_classes):
                if labels[d] == l:
                    parentBucket[l] += 1
                    if dataAttr[d] < split[0]:
                        leftBucket[l] += 1
                    else:
                        rightBucket[l] += 1
        if heuristic_name == "info_gain":
            split.append(info_gain(parentBucket, leftBucket, rightBucket))
        elif heuristic_name == "avg_gini_index":
            split.append(avg_gini_index(leftBucket, rightBucket))
    return splitValues

def chi_squared_test(left_bucket, right_bucket):
    """
    Calculates chi squared value and degree of freedom between the selected attribute
    and the class attribute. A bucket is a list of size num_classes. bucket[i] is the
    number of examples that belong to class i.
    :param left_bucket: Bucket belonging to the left child after the split.
    :param right_bucket: Bucket belonging to the right child after the split.
    :return: A float and and integer. Chi squared value and degree of freedom.
    """

    ObsTmp = [[], []]
    Ex = [[], []]
    chi = 0
    fullZeros = 0
    for amount in left_bucket:
        ObsTmp[0].append(amount)
    for amount in right_bucket:
        ObsTmp[1].append(amount)
    Obs = numpy.asarray(ObsTmp)
    Obs0 = numpy.sum(Obs, axis=0)
    Obs1 = numpy.sum(Obs, axis=1)
    fullZeros += np.count_nonzero(Obs0 == 0)
    for i in range(len(Obs[0])):
        Ex[0].append((Obs0[i] / sum(Obs0)) * (Obs1[0] / sum(Obs1)) * sum(Obs0))
        Ex[1].append((Obs0[i] / sum(Obs0)) * (Obs1[1] / sum(Obs1)) * sum(Obs0))

    for i in range(2):
        for j in range(len(Obs[0])):
            if Ex[i][j] == 0:
                pass
            else:
                chi += (Obs[i][j] - Ex[i][j]) ** 2 / Ex[i][j]

    return chi, len(left_bucket) - 1 - fullZeros