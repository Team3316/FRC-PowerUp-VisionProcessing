import torch
from train_lenet.train_net import BinaryImageLeNet

# Load model

model = BinaryImageLeNet()
model.load_state_dict(torch.load('train_lenet/trained_lenet.pt'))


def classify(image):
    return model(image)
