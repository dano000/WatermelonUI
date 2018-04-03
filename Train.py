#
#
#
#
#

import cv2
import numpy as np
import argparse
import importlib
import tensorflow as tf
import traceback
import utils
IM_WIDTH = 128
IM_HEIGHT = 128
IM_CHANNELS = 1
SPECT_LENGTH = 288


parser = argparse.ArgumentParser(description="Download test data from server");

parser.add_argument('-d','--dir',type=str,nargs='?',default="Model",help="Saved model checkpoints directory")
parser.add_argument('-m','--model',type=str,nargs='?',required=True,help="Python module containing model function")
parser.add_argument('--mode',type=str,nargs='?',default="TRAIN",help="TRAIN, EVAL or PREDICT")
parser.add_argument('-i','--input',type=str,nargs='+',required=True,help="Images to train network with")
parser.add_argument('-b','--batch_size',type=int,nargs='?',default=128,help="Training batch size")
parser.add_argument('-s','--steps',type=int,nargs='?',default=100,help="Number of steps to train with")
parser.add_argument('-l','--log_steps',type=int,nargs='?',default=50,help="Will log tf.INFO or every log_steps steps")

args = parser.parse_args()
try:
	model_module = importlib.import_module(str(args.model))
except:
	traceback.print_exc()
	print("Cannot import module: ",args.model)
	exit(0);
try:
	model = model_module.model_fn
except:
	traceback.print_exc()
	print("Supplied model: (" + args.model + "), has no model")
	exit(0);
try:
	model_type = model_module.model_type
	assert model_type == "AUDIO" or model_type =="SPECT" or model_type == "IMAGE"
except:
	traceback.print_exc()
	print("Supplied model: (" + args.model + "), has no valid model type")
	exit(0);
	
	
tf.logging.set_verbosity(tf.logging.INFO)

# im_list = [];
# for image in args.images:

# 	if os.path.isdir(image):
# 		for x in os.listdir(image):
# 			if re.match('.*\.(jpg|png)',x):
# 				im_list.append(image+x)

# 	elif os.path.isfile(image):
# 		im_list.extend(image)
# 	else:
# 		print("Cannot find image: ",image)
# 		exit(0)

# def is_ripe(path):
# 	if(path.split('.')[-2][-1] =='r'):
# 		return True
# 	else:
# 		return False

# def load_features():
# 	features = np.empty([args.batch_size,IM_WIDTH,IM_HEIGHT,IM_CHANNELS],dtype=np.float32)
# 	labels = np.empty([args.batch_size],dtype=np.int32)
# 	i = 0
# 	for im_path in im_list:
# 		im = cv2.imread(im_path)
# 		im = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
# 		feature = cv2.resize(im,(IM_WIDTH,IM_HEIGHT),interpolation = cv2.INTER_CUBIC)
# 		features[i] = np.reshape(im,[IM_WIDTH, IM_HEIGHT,IM_CHANNELS])
# 		labels[i] = is_ripe(im_path)
# 		i += 1
# 		if i == args.batch_size:
# 			return [features,labels]
# 	#i now contains the actual batch size
# 	print("Could not find ", args.batch_size," samples using new batch_size: ",i)
# 	np.reshape(features,[i,IM_WIDTH,IM_HEIGHT,IM_CHANNELS])
# 	np.reshape(labels,[i])
# 	return [feautures,labels]

def main(_):

	if model_type == "IMAGE":
		features,labels = utils.load_images(args.input,args.batch_size)
	elif model_type == "AUDIO":
		features,labels = utils.load_audio(args.input,args.batch_size)
	elif model_type =="SPECT":
		features,labels = utils.load_spect(args.input,args.batch_size)
	print(features)
	ripeness_classifier = tf.estimator.Estimator(
		model_fn=model, model_dir=args.dir)
	#Set up loging for predictions 
	tensors_to_log = {"probabilites": "Predictions/softmax_tensor"}
	logging_hook = tf.train.LoggingTensorHook(
		tensors=tensors_to_log, every_n_iter=args.log_steps)
	#Train the model
	if args.mode == "TRAIN":
		input_fn = tf.estimator.inputs.numpy_input_fn(
			x=features,
			y=labels,
			batch_size=args.batch_size,			
			num_epochs=None,
			shuffle=True)

		ripeness_classifier.train(
			input_fn=input_fn,
			steps=args.steps,
			hooks=[logging_hook])

		print("Training completed")
	elif args.mode == "EVAL":
		input_fn = tf.estimator.inputs.numpy_input_fn(
			x=features,
			y=labels,
			batch_size=args.batch_size,
			num_epochs=1,
			shuffle=False)
		eval_results = ripeness_classifier.evaluate(input_fn=input_fn)
		print("Eval results:")
		print(eval_results)
	elif args.mode == "PREDICT":
		input_fn = tf.estimator.inputs.numpy_input_fn(
			x=features,
			batch_size=args.batch_size,
			num_epochs=1,
			shuffle=False)
		pred = list(est.predict(pred_input_fn))
		print("Prediction results:")
		print(pred)



	

if __name__ == "__main__":
	tf.app.run()
