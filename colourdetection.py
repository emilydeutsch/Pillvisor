import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, join

#yellow
'''lower = np.array([20, 100, 100])
upper = np.array([30, 255, 255])'''

#orange
lower = np.array([10, 100, 20])
upper = np.array([15, 255, 255])

mypath = "pillPictures/testorange"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
img_count = 0
for file in onlyfiles:
    img_count = img_count + 1
    image_path = mypath + "/" + file
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cropped_mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow("image",cropped_mask)
    cv2.waitKey(0)