import os
from os import listdir
from os.path import isfile, join
import cv2
import numpy as np

number = 2

mypath = "pillPictures/" + str(number)
savepath = "pillPictures/saved"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

img_count = 0
for file in onlyfiles:
	img_count = img_count + 1
	image_path = mypath + "/" + file
	img = cv2.imread(image_path)
	#print(np.shape(img))
	img = img[500:2500,1000:3000]
	#print(np.shape(img))
	print(img_count)
	cv2.imwrite(os.path.join(savepath +"/" + str(number) + "_pill" + "_" +str(img_count)+'.jpg'),img)
