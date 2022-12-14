from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import matplotlib.pyplot as plt
import os
import random
import torch
from torch.utils.data import Dataset, DataLoader , random_split , WeightedRandomSampler
from albumentations import RandomCrop, HorizontalFlip, CenterCrop, Compose, Normalize
from albumentations.pytorch.transforms import ToTensor
from sklearn.metrics import accuracy_score
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision import datasets, models, transforms
from torchvision.utils import make_grid
from tqdm.notebook import tqdm
from torchvision.datasets import ImageFolder
from os import listdir
from os.path import join, isdir
from glob import glob
import cv2
import numpy as np

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device

image_path = '/content/drive/MyDrive/Images_new'

## Using Pretrained Resnet and modification in the output layer

model_ft = models.resnet50(pretrained=True)

for param in model_ft.parameters():
    param.requires_grad = False

num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, 120)

model_ft = model_ft.to(device)

##Change the optimizer to Adagrad 

criterion = nn.CrossEntropyLoss()
optimizer_ft = optim.Adagrad(model_ft.parameters(), lr=0.001)

## Calculate the customized values of RGB means and standard deviations for your own data and plug them into the transform component of the dataset

channels = 3

def cal_dir_stat(root):
    cls_dirs = [d for d in listdir(root) if isdir(join(root, d))]
    pixel_num = 0 # store all pixel number in the dataset
    channel_sum = np.zeros(channels)
    channel_sum_squared = np.zeros(channels)

    for idx, d in enumerate(cls_dirs):
        im_pths = glob(join(root, d, "*.jpg"))

        for path in tqdm(im_pths):
            im = cv2.imread(path) # image in M*N*CHANNEL_NUM shape, channel in BGR order
            im = im/255.0
            pixel_num += (im.size/channels)
            channel_sum += np.sum(im, axis=(0, 1))
            channel_sum_squared += np.sum(np.square(im), axis=(0, 1))

    bgr_mean = channel_sum / pixel_num
    bgr_std = np.sqrt(channel_sum_squared / pixel_num - np.square(bgr_mean))
    
    # change the format from bgr to rgb
    rgb_mean = list(bgr_mean)[::-1]
    rgb_std = list(bgr_std)[::-1]
    
    return rgb_mean, rgb_std


train_root = image_path
mean, std = cal_dir_stat(train_root)

# These values came from the above script

mean = [0.4733035079660368, 0.4493133692310059, 0.39019856482208]
std = [0.2623949980190315, 0.25695371923552357, 0.26302654550084426]

transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.4733, 0.4493, 0.3901], [0.2623, 0.2569, 0.2630])
])

## The class used to handle the oversampling or undersampling of the data for unbalanced classes is called the WeightedRandomSampler

class_weights = []

for root, subdir, files in os.walk(image_path):
      if len(files) > 0:
        class_weights.append(1/len(files))

sample_weights = [0] * len(dataset)
idx = 0
for  (data, label) in tqdm(dataset.imgs):
        class_weight = class_weights[label]
        sample_weights[idx] = class_weight
        idx = idx +1

train_sampler = WeightedRandomSampler(sample_weights, 
                                    num_samples=len(sample_weights), 
                                    replacement=True)

batch_size = 10

dataset = ImageFolder(image_path, transform=transform)

trainloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                          num_workers=2,
                                          sampler=train_sampler)

# Visualization of a single random batch

def batch(dl):
    for img, lb in dl:
        fig, ax = plt.subplots(figsize=(16, 16))
        ax.set_xticks([]); ax.set_yticks([])
        ax.imshow(make_grid(img.cpu(), nrow=16).permute(1,2,0))
        break

batch(trainloader)

dataset_sizes = len(dataset)
dataset_sizes

# Model training 
def train_model(model, criterion, optimizer, num_epochs):

    for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)
        
            model.train()  # Set model to training mode
            
            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in tqdm(trainloader):
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)

                loss = criterion(outputs, labels)
                loss.backward()

                optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            

            epoch_loss = running_loss / dataset_sizes
            epoch_acc = running_corrects.double() / dataset_sizes

            print('Loss: {:.4f} Acc: {:.4f}'.format(epoch_loss, epoch_acc))

    return model

# Training
model_ft = train_model(model_ft, criterion, optimizer_ft, num_epochs=30)

# Saving Model
torch.save(model_ft.state_dict(), '/content/drive/MyDrive/savedModel')
