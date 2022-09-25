import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import os
import random
import torch
from tqdm.notebook import tqdm
from torchvision.datasets import ImageFolder

#Existing path of images in drive
image_path = '/content/drive/MyDrive/Images'

#New path that will be created after copying the folder
image_path_new = '/content/drive/MyDrive/Images_new'

#Copying the source folder using Linus commands
#path that contains folder you want to copy
%cd /content/drive/MyDrive/
%cp -av Images/ Images_new

#Structuring the data in the form of a Dataframe
image_folders = []
for element in os.listdir(image_path):
    path = image_path + '/' + element
    breed = element.split('-')[1]
    images = len(os.listdir(os.path.join(image_path,element)))
    image_folders.append((path, breed, images))

df = pd.DataFrame(image_folders, columns = ['Path', 'Breeds', 'Images'])

plt.figure(figsize=(20,4))
plt.title('Class wise distribution in descending order')
sns.barplot(x = 'Breeds', y = 'Images', data = df.sort_values('Images', ascending = False), palette = "GnBu_d")

#Sorting folders in Descending order
sorted_df = df.sort_values('Images', ascending = False, ignore_index = True)

difference = sorted_df['Images'][0]

for path, breed, images_count in sorted_df.values:
    
  if images_count > difference:
    z = images_count - difference
    x = images_count - z

    files = os.listdir(path)  # Get filenames in current folder
    files = random.sample(files, z)  # Pick z random files
    
    for file in files:  # Go over each file name to be deleted
      f = os.path.join(path, file) # Create valid path to file
      os.remove(f)  # Remove the file

  difference = difference - 2

image_folders = []
for element in os.listdir(image_path_new):
    path = image_path_new + '/' + element
    breed = element.split('-')[1]
    images = len(os.listdir(os.path.join(image_path_new,element)))
    image_folders.append((path, breed, images))

df = pd.DataFrame(image_folders, columns = ['Path', 'Breeds', 'Images'])
sorted_new_df = df.sort_values('Images', ascending = False, ignore_index = True)
plt.figure(figsize=(20,4))
plt.title('Class wise distribution in descending order')
sns.barplot(x = 'Breeds', y = 'Images', data = df.sort_values('Images', ascending = False), palette = "GnBu_d")