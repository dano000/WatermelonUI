#
#
#
#
#

import numpy as np
import cv2
import tensorflow as tf
import model
import argparse
import importlib
import os
from itertools import chain
import glob
import random
from datetime import datetime
import re
random.seed(datetime.now())

parser = argparse.ArgumentParser(description="RipenessClassifierModelTrainer");

parser.add_argument('--dir',type=str,nargs='?',default="Model",help="Saved model checkpoints directory")
parser.add_argument('--model',type=str,nargs='?',required=True,help="Python module containing model function")
parser.add_argument('--classifier',type=str,nargs='?',default="/cygdrive/c/Users/chris/Documents/WatermelonCapstone/WatermelonClassifier/cascade.xml",help="Classifier for input images")
parser.add_argument('--images',type=str,nargs='+',required=True,help="Images to train network with")
parser.add_argument('--batch_size',type=int,nargs='?',default=128,help="Training batch size")
parser.add_argument('--steps',type=int,nargs='?',default=1,help="Number of steps to train with")
parser.add_argument('--log_steps',type=int,nargs='?',default=10,help="Will log tf.INFO or every log_steps steps")
parser.add_argument('--export',type=str,nargs='?',help="Optionaly export model to a dir")
args = parser.parse_args()

try:
	model_module = importlib.import_module(str(args.model))
except:
	print("Cannot import module: ",args.model)
	exit(0);
try:
	model = model_module.model
except:
	print("Supplied model: (" + args.model + "), has no model")
	exit(0);

im_list = [];
for image in args.images:

	if os.path.isdir(image):
		for x in os.listdir(image):
			if re.match('.*\.(jpg|png)',x):
				im_list.append(image+x)

	elif os.path.isfile(image):
		im_list.extend(image)
	else:
		print("Cannot find image: ",image)
		exit(0)


cascade = cv2.CascadeClassifier(args.classifier)


tf.logging.set_verbosity(tf.logging.INFO)

def load_features():
	features = np.empty([args.batch_size,28,28,1],dtype=np.float32)
	labels = np.empty([args.batch_size],dtype=np.int32)
	i = 0
	for im_path in im_list:
		im = cv2.imread(im_path)
		im = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
		melons = cascade.detectMultiScale(im,1.1,3);
		for (x,y,w,h) in melons:
			roi = im[y:y+h, x:x+w]
			feature = cv2.resize(roi,(28,28),interpolation = cv2.INTER_CUBIC)
			features[i] = np.reshape(feature,[28, 28, 1])
			labels[i] = random.randint(0,1)
			i += 1
			if i == args.batch_size:
				return [features,labels]
	#i now contains the actual batch size
	print("Could not find ", args.batch_size," samples using new batch_size: ",i)
	np.reshape(features,[i,28,28,1])
	np.reshape(labels,[i])
	return [feautures,labels]


def main(unused_argv):
	#Load training and eval data fom provided images
	
	#Load training and eval data
	train_data,train_labels = load_features()
	eval_data = train_data
	eval_labels = train_labels
	

	ripeness_classifier = tf.estimator.Estimator(
		model_fn=model, model_dir=args.dir)
	#Set up loging for predictions 
	tensors_to_log = {"probabilites": "softmax_tensor"}
	logging_hook = tf.train.LoggingTensorHook(
		tensors=tensors_to_log, every_n_iter=args.log_steps)
	#Train the model
	train_input_fn = tf.estimator.inputs.numpy_input_fn(
		x={"x": train_data},
		y=train_labels,
		batch_size=args.batch_size,
		num_epochs=None,
		shuffle=True)

	ripeness_classifier.train(
		input_fn=train_input_fn,
		steps=args.steps,
		hooks=[logging_hook])
	#Evaluate model and print results
	eval_input_fn = tf.estimator.inputs.numpy_input_fn(
		x={"x": eval_data},
		y=eval_labels,
		num_epochs=1,
		shuffle=False)
	eval_results = ripeness_classifier.evaluate(input_fn=eval_input_fn)
	print("Eval results: ",eval_results)

	if( args.export != None and os.path.isdir(args.export)):
		feature_spec = {
			'x': tf.placeholder(dtype=np.float32,shape=[28,28,1],name='x')
		}
		ripeness_classifier.export_savedmodel(args.export,tf.estimator.export.build_raw_serving_input_receiver_fn(feature_spec))
 
if __name__ == "__main__":
	tf.app.run();