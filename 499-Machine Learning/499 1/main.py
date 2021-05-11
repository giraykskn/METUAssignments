import torch
from torch.utils.data import DataLoader
import torchvision.transforms as Transforms
from myDataset import myDataset
from myModel import myModel
import torch.nn.functional as functional
import os
import matplotlib.pyplot as pyplot

def train(model, optimizer, dataLoader, valLoader, epochs, device):
    bestValLoss = float('inf')
    valLossQueue = []
    for epochId in range(epochs):
        model.train()
        for images, labels in dataLoader:
            images = images.to(device)
            optimizer.zero_grad()
            model(images)
            optimizer.step()
        model.eval()
        losses = []
        for valImages, valLabels in valLoader:
            valImages = valImages.to(device)
            valLabels = valLabels.to(device)
            optimizer.zero_grad()
            pred = model(valImages)
            loss = functional.nll_loss(pred, valLabels)
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
        valLoss = sum(losses)/len(losses)
        if valLoss < bestValLoss:
            bestValLoss = valLoss
            valLossQueue = []
        else:
            valLossQueue.append(valLoss)
            if(len(valLossQueue) == 11):
                break
    return bestValLoss

def test(model, transforms, device):
    model.load_state_dict(torch.load("model_state_dict"))
    model.eval()
    testSet = myDataset(transforms, "test")
    testLoader = DataLoader(testSet, pin_memory=True)
    path = os.path.join("data", "test")
    with open(os.path.join(path, "results.txt"), 'w') as file:
        with open(os.path.join(path, "labels.txt"), 'r') as r:
            for images, labels in testLoader:
                images = images.to(device)
                pred = model(images)
                prediction = torch.max(pred,1)[1].item()
                file.write(r.readline().strip() + " " + str(prediction) + "\n")

def main():
    layers = [1, 2, 3]
    aFunctions = ["S", "R", "T"]
    neurons = [256, 512, 1024]
    learningRates = [0.01, 0.003, 0.001, 0.0003, 0.0001, 0.00003]
    noOfEpochs = 400

    device = torch.device("cuda")
    torch.manual_seed(0)
    transforms = Transforms.ToTensor()
    dataset = myDataset(transforms, "train")
    trainSet, validationSet = torch.utils.data.random_split(dataset, [24000, 6000])
    dataLoader = DataLoader(trainSet, batch_size=50,  shuffle=True, pin_memory=True)
    valLoader = DataLoader(validationSet, batch_size=50,  shuffle=True, pin_memory=True)
    sanityCheck(trainSet)
    bestValue = float('inf')
    bestModel = None
    bestParameters = []
    with open("grid.txt", 'w') as g:
        for layer in layers:
            if layer > 1:
                for aFunction in aFunctions:
                    for neuron in neurons:
                        for learningRate in learningRates:
                            model = myModel(layer, aFunction, neuron)
                            model = model.to(device)
                            optimizer = torch.optim.Adam(model.parameters(), lr=learningRate)
                            value = train(model, optimizer, dataLoader, valLoader, noOfEpochs, device)
                            print("Layer:", layer, " Activation Function:", aFunction, " Neuron:", neuron,
                                  " Learning rate:", learningRate, ":::: Value:", value)
                            g.write("Layer: " + str(layer) + "Activation Function: " + str(aFunction) + "Neuron: " + str(neuron) + "Learning rate: " + str(learningRate) + "::::Value: " + str(
                                value) + "\n")
                            if value < bestValue:
                                torch.save(model.state_dict(), "model_state_dict")
                                bestModel = model
                                bestParameters = []
                                bestParameters.append(layer)
                                bestParameters.append(aFunction)
                                bestParameters.append(neuron)
                                bestParameters.append(learningRate)
            else:
                for learningRate in learningRates:
                    model = myModel(layer, "None", None)
                    model = model.to(device)
                    optimizer = torch.optim.Adam(model.parameters(), lr=learningRate)
                    value = train(model, optimizer, dataLoader, valLoader, noOfEpochs, device)
                    print("Layer:", layer, " Learning rate:", learningRate, ":::: Value:", value)
                    g.write("Layer: " + str(layer) + "Learning rate: " + str(learningRate) + "::::Value: " + str(value) + "\n")
                    if value < bestValue:
                        torch.save(model.state_dict(), "model_state_dict")
                        bestModel = model
                        bestParameters = []
                        bestParameters.append(layer)
                        bestParameters.append(learningRate)
        if(bestParameters[0] == 1):
            g.write(str(bestParameters[0]) + " " + str(bestParameters[1]) + "\n")
        else:
            g.write(str(bestParameters[0]) + " " + str(bestParameters[1]) + " " + str(bestParameters[2]) + " " + str(bestParameters[3]) + "\n")

    plot(bestParameters, trainSet, validationSet, device)
    test(bestModel, transforms, device)

def sanityCheck(trainSet):
    sanityLoader = DataLoader(trainSet)
    model = myModel(1, None, None)
    losses = []
    accuracies = []
    for images, labels in sanityLoader:
        pred = model(images)
        loss = functional.nll_loss(pred, labels)
        loss.backward()
        losses.append(loss.item())
        prediction = torch.max(pred, 1)[1].item()
        if(prediction == labels):
            accuracies.append(1)
        else:
            accuracies.append(0)

    Loss = sum(losses) / len(losses)
    Accuracy = sum(accuracies) / len(accuracies)
    print("Initial loss:", Loss)
    print("Initial Accuracy:", Accuracy)

def plot(parameters, trainSet, validationSet, device):
    epochs = 400
    trainingLossesPerEpochs = []
    validationLossesPerEpochs = []
    bestValLoss = float('inf')
    valLossQueue = []
    maxEpoch = -1
    dataLoader = DataLoader(trainSet, batch_size=50, shuffle=True, pin_memory=True)
    valLoader = DataLoader(validationSet, batch_size=50, shuffle=True, pin_memory=True)
    if(parameters[0] == 1):
        model = myModel(parameters[0], "None", None)
        model = model.to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=parameters[1])
    else:
        model = myModel(parameters[0], parameters[1], parameters[2])
        model = model.to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=parameters[3])
    for epoch in range(epochs):
        maxEpoch = epoch
        trainingLosses = []
        model.train()
        for images, labels in dataLoader:
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            pred = model(images)
            loss = functional.nll_loss(pred, labels)
            loss.backward()
            optimizer.step()
            trainingLosses.append(loss.item())
        trainingLoss = sum(trainingLosses) / len(trainingLosses)
        trainingLossesPerEpochs.append(trainingLoss)
        model.eval()
        validationLosses = []
        for images, labels in valLoader:
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            pred = model(images)
            loss = functional.nll_loss(pred, labels)
            loss.backward()
            optimizer.step()
            validationLosses.append(loss.item())
        validationLoss = sum(validationLosses) / len(validationLosses)
        validationLossesPerEpochs.append(validationLoss)
        if validationLoss < bestValLoss:
            bestValLoss = validationLoss
            valLossQueue = []
        else:
            valLossQueue.append(validationLoss)
            if(len(valLossQueue) == 11):
                break
    x = range(0,maxEpoch+1)
    pyplot.plot(x, trainingLossesPerEpochs, label = "Training Loss")
    pyplot.plot(x, validationLossesPerEpochs, label="Validation Loss")
    pyplot.xlabel("Epochs")
    pyplot.ylabel("Losses")
    pyplot.title("Losses vs Epochs")
    pyplot.legend()
    pyplot.show()

if __name__ == '__main__':
    main()