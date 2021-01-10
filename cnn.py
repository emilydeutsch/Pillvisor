import tensorflow as tf

import math
import numpy as np
import re

from collections import Counter
from matplotlib import pyplot as plt
from PIL import Image
#import tensorflow.keras.preprocessing.image.ImageDataGenerator as ImageDataGenerator

import cv2

import os
from os import listdir
from os.path import isfile, join

mypath = "pillPictures/saved"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

pills = {0:"white pill",
         1:"orange pill",
         2:"yellow pill",
         3:"multicolour pill"}

datagen = tf.keras.preprocessing.image.ImageDataGenerator(rotation_range=90,brightness_range=[0.5,1.0])
imres = 250
dim = (imres,imres)
pairs = []
for img_count in range(len(onlyfiles)):
  image_path = mypath + '/' + onlyfiles[img_count]
  identity = onlyfiles[img_count][0]
  img = cv2.imread(image_path)
  print(image_path)
  img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
  pairs.append([img.copy(),int(identity)])
  samples = np.expand_dims(img, 0)
  count = 0
  # prepare iterator
  it = datagen.flow(samples, batch_size=1)
  for j in range(3):
    for i in range(9):
      count = count + 1
      # define subplot
      plt.subplot(330 + 1 + i)
      # generate batch of images
      batch = it.next()
      # convert to unsigned integers for viewing
      image = batch[0].astype('uint8')
      # plot raw pixel data
      resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

      plt.imshow(resized_image)
      pairs.append([resized_image.copy(),int(identity)])
