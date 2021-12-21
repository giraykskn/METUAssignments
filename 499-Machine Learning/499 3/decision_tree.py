import numpy as np
import sys
import scipy.stats
from graphviz import Digraph
from IPython.display import Image
from dt import calculate_split_values, chi_squared_test

NUM_CLASSES = 3

class Node:
    def __init__(self, bucket):
        self.attr = None
        self.split = None
        self.bucket = bucket
        self.left = None
        self.right = None

    def addLeft(self, child):
        self.left = child

    def addRight(self, child):
        self.right = child

    def __str__(self):
        if self.attr == None:
            return str(self.bucket)
        else:
            return "x[" + str(self.attr) + "] < " + '{:.6f}'.format(self.split) + "\n" + str(self.bucket)

def decision_tree():
    train_data = np.load('hw3_data/iris/train_data.npy')
    train_labels = np.load('hw3_data/iris/train_labels.npy')
    test_data = np.load('hw3_data/iris/test_data.npy')
    test_labels = np.load('hw3_data/iris/test_labels.npy')

    infoGain  = regulars(train_data, train_labels, 'info_gain')
    avgGini = regulars(train_data, train_labels, 'avg_gini_index')
    pruningInfoGain = prepruning(train_data, train_labels, 'info_gain')
    pruningAvgGini = prepruning(train_data, train_labels, 'avg_gini_index')

    print("Info gain accuracy is " + str(calculateAccuracy(infoGain, test_data, test_labels)))
    print("Avg gini index accuracy is " + str(calculateAccuracy(avgGini, test_data, test_labels)))
    print("Info gain accuracy with prepuning is " + str(calculateAccuracy(pruningInfoGain, test_data, test_labels)))
    print("Avg gini index accuracy with prepuning is " + str(calculateAccuracy(pruningAvgGini, test_data, test_labels)))

    #createGraph(infoGain, "Info gain")
    #createGraph(avgGini, "Avg gini index")
    #createGraph(pruningInfoGain, "Info gain with prepuning")
    #createGraph(pruningAvgGini, "Avg gini index with prepuning")

def regulars(train_data, train_labels, method):
    initialBucket = []
    for i in range(NUM_CLASSES):
        initialBucket.append(0)
    for label in train_labels:
        initialBucket[label] += 1
    tree = Node(initialBucket)
    regRecursive(tree, train_data, train_labels, method)
    return tree

def regRecursive(node, data, labels, method):
    if node.bucket.count(0) == NUM_CLASSES - 1:
        return
    else:
        attributes = []
        for i in range(len(data[0])):
            attributes.append(calculate_split_values(data, labels, NUM_CLASSES, i, method))
        chosenAttribute = None
        chosenSplit = None
        if method == 'info_gain':
            max = sys.float_info.min
            for i in range(len(data[0])):
                for s in attributes[i]:
                    if s[1] > max:
                        max = s[1]
                        chosenAttribute = i
                        chosenSplit = s[0]
        else:
            min = sys.float_info.max
            for i in range(len(data[0])):
                for s in attributes[i]:
                    if s[1] < min:
                        min = s[1]
                        chosenAttribute = i
                        chosenSplit = s[0]
        node.attr = chosenAttribute
        node.split = chosenSplit
        leftData = []
        rightData = []
        leftLabel = []
        rightLabel = []
        leftBucket = []
        rightBucket = []

        for i in range(len(data)):
            if data[i][chosenAttribute] < chosenSplit:
                leftData.append(data[i])
                leftLabel.append(labels[i])
            else:
                rightData.append(data[i])
                rightLabel.append(labels[i])
        for i in range(NUM_CLASSES):
            leftBucket.append(0)
            rightBucket.append(0)
        for label in leftLabel:
            leftBucket[label] += 1
        for label in rightLabel:
            rightBucket[label] += 1
        left = Node(leftBucket)
        right = Node(rightBucket)
        node.addLeft(left)
        node.addRight(right)
        regRecursive(left, np.asarray(leftData), np.asarray(leftLabel), method)
        regRecursive(right, np.asarray(rightData), np.asarray(rightLabel), method)

def prepruning(train_data, train_labels, method):
    initialBucket = []
    for i in range(NUM_CLASSES):
        initialBucket.append(0)
    for label in train_labels:
        initialBucket[label] += 1
    tree = Node(initialBucket)
    prepuningRecursive(tree, train_data, train_labels, method)
    return tree

def prepuningRecursive(node, data, labels, method):
    if node.bucket.count(0) == NUM_CLASSES - 1:
        return
    else:
        attributes = []
        for i in range(len(data[0])):
            attributes.append(calculate_split_values(data, labels, NUM_CLASSES, i, method))
        chosenAttribute = None
        chosenSplit = None
        if method == 'info_gain':
            max = sys.float_info.min
            for i in range(len(data[0])):
                for s in attributes[i]:
                    if s[1] > max:
                        max = s[1]
                        chosenAttribute = i
                        chosenSplit = s[0]
        else:
            min = sys.float_info.max
            for i in range(len(data[0])):
                for s in attributes[i]:
                    if s[1] < min:
                        min = s[1]
                        chosenAttribute = i
                        chosenSplit = s[0]
        leftData = []
        rightData = []
        leftLabel = []
        rightLabel = []
        leftBucket = []
        rightBucket = []

        for i in range(len(data)):
            if data[i][chosenAttribute] < chosenSplit:
                leftData.append(data[i])
                leftLabel.append(labels[i])
            else:
                rightData.append(data[i])
                rightLabel.append(labels[i])
        for i in range(NUM_CLASSES):
            leftBucket.append(0)
            rightBucket.append(0)
        for label in leftLabel:
            leftBucket[label] += 1
        for label in rightLabel:
            rightBucket[label] += 1
        chi, dof = chi_squared_test(leftBucket, rightBucket)
        if chi < scipy.stats.chi2.ppf(q=0.90, df = dof):
            return
        left = Node(leftBucket)
        right = Node(rightBucket)
        node.attr = chosenAttribute
        node.split = chosenSplit
        node.addLeft(left)
        node.addRight(right)
        prepuningRecursive(left, np.asarray(leftData), np.asarray(leftLabel), method)
        prepuningRecursive(right, np.asarray(rightData), np.asarray(rightLabel), method)

def calculateAccuracy(tree ,test_data, test_labels):
    prediction = []
    node = tree
    correct = 0
    for data in test_data:
        while node.attr != None:
            if data[node.attr] < node.split:
                node = node.left
            else:
                node = node.right
        prediction.append(node.bucket.index(max(node.bucket)))
        node = tree
    for i in range(len(prediction)):
        if prediction[i] == test_labels[i]:
            correct += 1
    return correct / len(prediction)

def createGraph(tree, name):
    dot = Digraph()
    graphRec(tree, None, dot)
    dot.format = 'png'
    dot.render(name, view=True)

def graphRec(tree, parent, dot):
    s = str(tree)
    dot.node(name=str(id(tree)), label=s)
    if parent != None:
        dot.edge(str(id(parent)), str(id(tree)))
    if tree.attr == None:
        return
    else:
        graphRec(tree.left, tree, dot)
        graphRec(tree.right, tree, dot)

decision_tree()