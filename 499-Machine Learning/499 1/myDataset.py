from torch.utils.data import Dataset
from PIL import Image
import os

class myDataset(Dataset):
    def __init__(self, transform, tag):
        path = os.path.join("data", tag)
        with open(os.path.join(path, "labels.txt"), 'r') as file:
            self.dataPaths = []
            for line in file:
                if(tag == "test"):
                    line = line.strip()
                    dataName = line
                    dataPath = os.path.join(path, dataName)
                    self.dataPaths.append((dataPath, -1))
                else:
                    dataName, label = line.split()
                    dataPath = os.path.join(path, dataName)
                    label = int(label)
                    self.dataPaths.append((dataPath, label))
        self.transform = transform
        self.datas = []
        for data in self.dataPaths:
            curDataPath = data[0]
            curLabel = data[1]
            curData = Image.open(curDataPath)
            curData = self.transform(curData)
            self.datas.append((curData, curLabel))

    def __len__(self):
        return len(self.datas)

    def __getitem__(self, item):
        return self.datas[item]
