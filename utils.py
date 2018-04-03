#
#
#
#
#

import numpy as np
import cv2
import random
import datetime
import os
import re

IM_WIDTH = 128
IM_HEIGHT = 128
IM_CHANNELS = 1

def is_ripe(path):
	if(path.split('.')[-2][-1] =='r'):
		return True
	else:
		return False

def load_images(dir,batch_size,resize=None):
	#Find all images in dir
	im_list = [];
	for image in dir:

		if os.path.isdir(image):
			for x in os.listdir(image):
				if re.match('.*\.(jpg|png)',x):
					im_list.append(image+x)
		elif os.path.isfile(image):
			im_list.extend(image)
		else:
			print("Cannot find image: ",image)
			return None

	#
	images = np.empty([batch_size,IM_WIDTH,IM_HEIGHT,IM_CHANNELS],dtype=np.float32)
	labels = np.empty([batch_size],dtype=np.int32)
	i = 0
	for im_path in im_list:
		im = cv2.imread(im_path)
		im = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
		if not resize is None:
			feature = cv2.resize(im,resize,interpolation = cv2.INTER_CUBIC)
		images[i] = np.reshape(im,[IM_WIDTH, IM_HEIGHT,IM_CHANNELS])
		labels[i] = is_ripe(im_path)
		i += 1
		if i == batch_size:
			features = {
				"images":images
			}
			return (features,labels)
	#i now contains the actual batch size
	print("Could not find ", batch_size," samples using new batch_size: ",i)
	np.reshape(images,[i,IM_WIDTH,IM_HEIGHT,IM_CHANNELS])
	np.reshape(labels,[i])

	features = {
		"images":images
	}
	return (features,labels)

OFF = 0
UV_ON = 1
LED_ON = 2

SPECT_LENGTH = 288

def load_spect(dir,batch_size):
	spect = np.random.uniform(size=(batch_size,SPECT_LENGTH))
	labels = np.random.randint(0,1,(batch_size))
	
	features = {
		"spect":spect
	}
	return (features,labels)

