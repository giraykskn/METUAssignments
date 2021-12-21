from nb import estimate_pi, vocabulary, estimate_theta, test
import sys

def readFile(name):
    data = []
    labels = []
    dataFile = open('hw4_data/sentiment/' + name + '_data.txt', 'r', encoding='utf8')
    labelsFile = open('hw4_data/sentiment/' + name + '_labels.txt', 'r', encoding='utf8')
    dataLines = dataFile.readlines()
    labelsLines = labelsFile.readlines()
    for line in dataLines:
        data.append(line.rstrip('\n').split(' '))
    for line in labelsLines:
        labels.append(line.rstrip('\n'))
    return data, labels

train_data, train_labels = readFile('train')
test_data, test_labels = readFile('test')

vocab = vocabulary(train_data)
pi = estimate_pi(train_labels)
theta = estimate_theta(train_data, train_labels, vocab)
t = test(theta, pi, vocab, test_data)
predicted = []
for data in t:
    pred = None
    maxScore = -sys.float_info.max
    for score in data:
        if score[0] > maxScore:
            maxScore = score[0]
            pred = score[1]
    predicted.append(pred)

correct = 0
for i in range(len(test_labels)):
    if test_labels[i] == predicted[i]:
        correct += 1

accuracy = correct / len(test_labels)
print("The accuracy is " + str(accuracy))