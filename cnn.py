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

from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

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

def convert_to_one_hot(Y, C):
	Y = np.eye(C)[Y.reshape(-1)].T
	return Y

NUMBER_OF_LABELS = 4
CONFIDENCE_THRESHOLD = 0.01
VALIDATION_SPLIT = 0.2

X_dataset_orig = np.array([data[0] for data in pairs[:]])
Y_dataset_orig = np.array([data[1] for data in pairs])

# Normalize the data set

X_dataset = X_dataset_orig/255.0 #np.divide(X_dataset_orig,255)#[data[0] for data in X_dataset_orig]#/255.
Y_dataset = convert_to_one_hot(Y_dataset_orig, NUMBER_OF_LABELS).T

print("Total examples: {:f}\nTraining examples: {:f}\nTest examples: {:f}".
      format(X_dataset.shape[0],
             math.ceil(X_dataset.shape[0] * (1-VALIDATION_SPLIT)),
             math.floor(X_dataset.shape[0] * VALIDATION_SPLIT)))
print("X shape: " + str(X_dataset.shape))
print("Y shape: " + str(Y_dataset.shape))

# Display images in the training data set. 
def displayImage(index):
	#print(X_dataset[index])
	plt.imshow(X_dataset[index])
	caption = ("y = " + str(Y_dataset_orig[index])) #str(np.squeeze(Y_dataset_orig[:, index])) #
	plt.text(0.5, 0.5, caption, 
			color='orange', fontsize = 20,
			horizontalalignment='left', verticalalignment='top')

displayImage(2)

conv_model = tf.keras.models.Sequential()
conv_model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
                             input_shape=(imres, imres, 3))) #size of the x-dataset
conv_model.add(tf.keras.layers.MaxPooling2D((2, 2)))
conv_model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
conv_model.add(tf.keras.layers.MaxPooling2D((2, 2)))
#conv_model.add(layers.Conv2D(128, (3, 3), activation='relu'))
#conv_model.add(layers.MaxPooling2D((2, 2)))
#conv_model.add(layers.Conv2D(128, (3, 3), activation='relu'))
#conv_model.add(layers.MaxPooling2D((2, 2)))
conv_model.add(tf.keras.layers.Flatten())
conv_model.add(tf.keras.layers.Dropout(0.5))
conv_model.add(tf.keras.layers.Dense(128, activation='relu'))
conv_model.add(tf.keras.layers.Dense(NUMBER_OF_LABELS, activation='softmax')) # the number of layers

LEARNING_RATE = 1e-4
conv_model.compile(loss='categorical_crossentropy',
                   optimizer=tf.keras.optimizers.RMSprop(lr=LEARNING_RATE),
                   metrics=['acc'])

history_conv = conv_model.fit(X_dataset, Y_dataset, 
                              validation_split=VALIDATION_SPLIT, 
                              epochs=6, 
                              batch_size=16)

conv_model.save("hackathoncnn2")

plt.plot(history_conv.history['loss'])
plt.plot(history_conv.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train loss', 'val loss'], loc='upper left')
plt.show()

plt.plot(history_conv.history['acc'])
plt.plot(history_conv.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy (%)')
plt.xlabel('epoch')
plt.legend(['train accuracy', 'val accuracy'], loc='upper left')
plt.show()



def displayImage(index):
  img = X_dataset[index]
  
  img_aug = np.expand_dims(img, axis=0)
  y_predict = conv_model.predict(img_aug)[0]
  plt.imshow(img)
  indices = [i for i, x in enumerate(y_predict) if x == max(y_predict)] #find index with highest confidence
  print(indices)
  confidence = y_predict[indices[0]] #Y_dataset[index][indices[0]]
  caption = (str(indices[0])+" | " + str(confidence)) #str(Y_dataset[index]) + "\n" + str(y_predict))
  plt.text(0.5, 0.5, caption, 
           color='orange', fontsize = 16,
           horizontalalignment='left', verticalalignment='bottom')


displayImage(547)

predicted_size = len(X_dataset)
y_pred_array = np.zeros(predicted_size)
print(type(Y_dataset))
for index in range(predicted_size):
  #print("img:",img)
  #print("index:", index)
  img = X_dataset[index]
  img_aug = np.expand_dims(img, axis=0)
  y_predict = conv_model.predict(img_aug)[0]
  indices = np.argmax(y_predict)#[i for i, x in enumerate(y_predict) if x == max(y_predict)]
  
  #print(indices)
  max_ind = np.array(indices)
  y_pred_array[index] = max_ind
  #y_true[index] = 
print(y_pred_array)
print("NUMBER_OF_LABELS: ",NUMBER_OF_LABELS)
#y_pred_array2 = convert_to_one_hot(y_pred_array.astype(int),NUMBER_OF_LABELS).T
print(len(y_pred_array))
print(len(Y_dataset_orig))
confuse_array = confusion_matrix(Y_dataset_orig, y_pred_array)

df_cm = pd.DataFrame(confuse_array, [i for i in "0123"], [i for i in "0123"])
plt.figure()#figsize=(15,15))
#sn.set(font_scale=1.4) # for label size
sn.heatmap(df_cm)#, annot=True, annot_kws={"size": 16}) # font size

plt.show()