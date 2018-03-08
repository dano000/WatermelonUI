#
#
#
#
#

import Filters as filters
import numpy as np 
import tensorflow as tf
import argparse
from PIL import Image

#Execute with python EdgeDetector.py -i img_file

#Setup the Argument Parser
parser = argparse.ArgumentParser(description='BasicConv')
parser.add_argument('-i',type=str,help='Input file',nargs=1)
args = parser.parse_args()

input_file = args.i[0]

#Open the input image file

im = Image.open(input_file)

pixels = np.array(im)

#Create the Tensorflow network
input_layer = tf.reshape(tf.to_float(pixels),[-1,im.height,im.width,3])

# #Convolutional Layer 1
# identity = tf.nn.conv2d(
# 	input=input_layer,
# 	filter=[[filters.IdentityRGB()]],
# 	strides=[1,1,1,1],
# 	padding="SAME")

# #Blur layer
# blur = tf.nn.conv2d(
# 	input=identity,
# 	filter=filters.add_channel_filter(filters.GaussianBlur(),filters.IdentityRGB()),
# 	strides=[1,1,1,1],
# 	padding="SAME")

#Layer to convert from RGB uint8 to GrayScale float[0,1](outputs a grayscale image)
grayscale = tf.nn.conv2d(
	input=input_layer,
	filter=[[(np.array(filters.RGB2BW())/255).tolist()]],
	strides=[1,1,1,1],
	padding="SAME")
#Apply the sigmoid function to grayscale image 
#to turn it black and white
black_and_white = -tf.nn.sigmoid(.1*(grayscale-.5))+.5 

#Kernels to implement SobelFeldman edge detection
edgex = tf.nn.conv2d(
	input=black_and_white,
	filter=filters.add_channel_filter(filters.SobelFeldmanX(),[[1]]),
	strides=[1,1,1,1],
	padding="SAME")
edgey = tf.nn.conv2d(
	input=edgex,
	filter=filters.add_channel_filter(filters.SobelFeldmanY(),[[1]]),
	strides=[1,1,1,1],
	padding="SAME")

#Create and run the Tensorflow session
sess = tf.Session()
sess.run(tf.global_variables_initializer())

#Create a back and white image
bw_im = Image.fromarray((np.array(sess.run(black_and_white))*255).astype(np.uint8).reshape([im.height,im.width]),mode="L")

arr = np.array(sess.run(edgey))
overlay = Image.fromarray((arr*255).astype(np.uint8).reshape([im.height,im.width]),mode="L")

#Show the images
im = im.convert("RGBA")
overlay = overlay.convert("RGBA")
bw_im.show()
im.show()
new_im = Image.blend(im,overlay,.5)
new_im.show()


