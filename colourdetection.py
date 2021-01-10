import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, join

colour = 0

if colour == 0:
    #white
    sensitivity = 15
    lower = np.array([0,0,0])
    upper = np.array([255,sensitivity,255])
elif colour == 1:
    #orange
    lower = np.array([7, 100, 20])
    upper = np.array([15, 255, 255])
elif colour == 2:
    # yellow
    lower = np.array([20, 100, 20])
    upper = np.array([38, 255, 255])
elif colour ==3:
    # dark red
    lower = np.array([20, 100, 20])
    upper = np.array([38, 255, 255])
else:
    # all
    lower = np.array([0, 0, 0])
    upper = np.array([255, 255, 255])

mypath = "pillPictures/0"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
img_count = 0
dim = (250,250)
for file in onlyfiles:
    img_count = img_count + 1
    image_path = mypath + "/" + file
    img = cv2.imread(image_path)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cropped_mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(img, img, mask=cropped_mask)
    cv2.imshow("image",res)
    cv2.waitKey(3)