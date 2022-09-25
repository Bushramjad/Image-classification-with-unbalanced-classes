# Image-classification-with-unbalanced-classes

- The dataset is the Stanford Dog dataset which comprises of 120 dog classes. There are approximately ~200 images per dog category. The web page for the dataset is at http://vision.stanford.edu/aditya86/ImageNetDogs/ . 

-  The first step is data preparation. The Stanford dataset itself is balanced. We want to first create an unbalanced dataset out of it. To do this a script is provided in python which orders the class folders from highest to lowest number of images in them. The highest training examples for a class are 252. 

Say the highest represented class has 252 images,  the second highest represented class should have 250 images (reduction of 2 images), so if this second highest represented class has say 251 image you would reduce the size to 250 images by randomly removing one image. If its size is already 250 or less then you don't need to do any such thing. Look at the following sequence suppose the classes when ordered in descending order had number of images such as 252, 247, 246, 245, 244, 243, 242. According to our 2 image reduction rule they should have maximum images 252, 250, 248, 246, 244, 242, 240 so the actual number of images we end up with 252, 247(already below threshold), 246(already below threshold), 245(already below threshold), 244, 242(one removed), 240(two removed).
![download](https://user-images.githubusercontent.com/80513387/192157103-dd39dfd4-bf7c-4eea-97bc-9761017e6e32.png)
![download (1)](https://user-images.githubusercontent.com/80513387/192157106-10b4bae9-9014-43ff-acf0-1ddac65d4de6.png)

- The class used to handle the oversampling or undersampling of the data for unbalanced classes is called the WeightedRandomSampler and can be found in torch.utils.data. 

Provided are the 2 python files. One for the data creation and the second one for the training.


