#
#
#
#
#

import numpy as np
import scipy.stats as st
import tensorflow as tf
from tensorflow.python.framework import ops
#Inserts a 2D channel filter into a 2D kernel
#to create a 4D kernel for use in the tf.nn.conv2D
def add_channel_filter(kernel,channel):
	arr = np.empty([len(kernel),len(kernel[0]),len(channel),len(channel[0])])
	for i in range(0,len(kernel)):
		for j in range(0,len(kernel)):
			arr[i][j] = (kernel[i][j] * np.array(channel))
	return arr.tolist()

#identity filter for RGB channels
def IdentityRGB():
	return [[1,0,0],[0,1,0],[0,0,1]]


def RGB2BW():
	return [[1/3],[1/3],[1/3]]
#Gaussian blur kernel
def GaussianBlur(kernlen = 10, nsig = 3):
	kernlen = 21
	nsig = 3
	interval = (2*nsig+1.)/(kernlen)
	x = np.linspace(-nsig-interval/2., nsig+interval/2., kernlen+1)
	kern1d = np.diff(st.norm.cdf(x))
	kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
	return kernel_raw/kernel_raw.sum()

#https://en.wikipedia.org/wiki/Sobel_operator
def SobelFeldmanX():
	return [[1,0,-1],[2,0,-2],[1,0,-1]]

def SobelFeldmanY():
	return [[1,2,1],[0,0,0],[-1,-2,-1]]


def SobelFeldmanXAlt():
	return [[3,0,-3],[10,0,-10],[3,0,-3]]

def SobelFeldmanYAlt():
	return [[3,10,3],[0,0,0],[-3,-10,-3]]