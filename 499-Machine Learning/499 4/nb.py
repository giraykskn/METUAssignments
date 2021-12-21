import math

def vocabulary(data):
    """
    Creates the vocabulary from the data.
    :param data: List of lists, every list inside it contains words in that sentence.
                 len(data) is the number of examples in the data.
    :return: Set of words in the data
    """
    wordsSet = {data[0][0]}
    for l in data:
        for d in l:
            if not wordsSet.__contains__(d):
                wordsSet.add(d)
    return wordsSet

def estimate_pi(train_labels):
    """
    Estimates the probability of every class label that occurs in train_labels.
    :param train_labels: List of class names. len(train_labels) is the number of examples in the training data.
    :return: pi. pi is a dictionary. Its keys are class names and values are their probabilities.
    """
    dict = {}
    labels = []
    counts = []
    for label in train_labels:
        if labels.__contains__(label):
            counts[labels.index(label)] += 1
        else:
            labels.append(label)
            counts.append(1)
    for i in range(len(labels)):
        dict[labels[i]] = counts[i]/sum(counts)
    return dict
    
def estimate_theta(train_data, train_labels, vocab):
    """
    Estimates the probability of a specific word given class label using additive smoothing with smoothing constant 1.
    :param train_data: List of lists, every list inside it contains words in that sentence.
                       len(train_data) is the number of examples in the training data.
    :param train_labels: List of class names. len(train_labels) is the number of examples in the training data.
    :param vocab: Set of words in the training set.
    :return: theta. theta is a dictionary of dictionaries. At the first level, the keys are the class names. At the
             second level, the keys are all the words in vocab and the values are their estimated probabilities given
             the first level class name.
    """
    theta = {}
    tcj = []
    labels = []
    voc = []
    vl = len(vocab)
    for word in vocab:
        voc.append(word)
    voc.sort()
    for label in train_labels:
        if not labels.__contains__(label):
            labels.append(label)
    labels.sort()
    for label in labels:
        l = []
        for v in vocab:
            l.append(0)
        tcj.append(l)
    labelConcat = []
    for label in labels:
        l = []
        for n in range(len(train_data)):
            if train_labels[n] == label:
                l = l + train_data[n]
        labelConcat.append(l)
    for c in range(len(labels)):
        for j in range(len(vocab)):
            firstSum = 1 + labelConcat[c].count(voc[j])
            secondSum = vl + len(labelConcat[c])
            tcj[c][j] = firstSum / secondSum
    for c in range(len(labels)):
        dict = {}
        for j in range(len(vocab)):
            dict[voc[j]] = tcj[c][j]
        theta[labels[c]] = dict
    return theta



def test(theta, pi, vocab, test_data):
    """
    Calculates the scores of a test data given a class for each class. Skips the words that are not occurring in the
    vocabulary.
    :param theta: A dictionary of dictionaries. At the first level, the keys are the class names. At the second level,
                  the keys are all of the words in vocab and the values are their estimated probabilities.
    :param pi: A dictionary. Its keys are class names and values are their probabilities.
    :param vocab: Set of words in the training set.
    :param test_data: List of lists, every list inside it contains words in that sentence.
                      len(test_data) is the number of examples in the test data.
    :return: scores, list of lists. len(scores) is the number of examples in the test set. Every inner list contains
             tuples where the first element is the score and the second element is the class name.
    """

    scores = []
    labels = []
    tlist = theta.items()
    for t in tlist:
        labels.append(t[0])
    for data in test_data:
        l = []
        for label in labels:
            arg = math.log(pi[label])
            for word in vocab:
                arg += data.count(word) * math.log(theta[label][word])
            l.append((arg, label))
        scores.append(l)
    return scores