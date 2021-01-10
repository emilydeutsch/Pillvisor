#modeltest.py

import tensorflow as tf

from os import listdir
from os.path import isfile, join

import cv2
import numpy as np
from matplotlib import pyplot as plt

mypath = "pillPictures/saved"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

num = 4
image_path = mypath + "/" + onlyfiles[num]
img = cv2.imread(image_path)

dim = (250,250)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
cv2.imshow("resized",resized)
cv2.waitKey(3)
re_img = resized/255.0


conv_model = tf.keras.models.load_model("hackathoncnn")

img_aug = np.expand_dims(re_img, axis=0)
y_predict = conv_model.predict(img_aug)[0]

indices = [i for i, x in enumerate(y_predict) if x == max(y_predict)]

print(y_predict)
print(onlyfiles[num])

print(indices[0])
