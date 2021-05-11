import torch.nn as nn
import torch.nn.functional as functional
import torch

class myModel(nn.Module):
    def __init__(self, layer, aFunction, neuron):
        super(myModel, self).__init__()
        self.fc = []
        self.aFunction = aFunction
        if layer == 1:
            self.fc.append(nn.Linear(3*40*40, 10))
        else:
            self.fc.append(nn.Linear(3*40*40, neuron))
            for i in range(layer - 2):
                self.fc.append(nn.Linear(neuron, neuron))
            self.fc.append(nn.Linear(neuron, 10))
        self.fc = nn.ModuleList(self.fc)

    def forward(self, forw):
        forw = forw.view(forw.size(0), -1)
        forw = self.fc[0](forw)
        for i in range(len(self.fc) - 1):
            if self.aFunction == "S":
                forw = torch.sigmoid(forw)
            elif self.aFunction == "R":
                forw = functional.relu(forw)
            elif self.aFunction == "T":
                forw = torch.tanh(forw)
            forw = self.fc[i + 1](forw)
        forw = torch.log_softmax(forw, dim=1)
        return forw
