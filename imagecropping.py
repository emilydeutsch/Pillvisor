import os
from os import listdir
from os.path import isfile, join
import cv2

mypath = "pillPictures"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]