#
#
#
#
#

import numpy as np
import cv2
import argparse
import os


parser = argparse.ArgumentParser(description="Haar2DShapeClassifierImageTester")
parser.add_argument('--classifier',type=str,nargs='?',metavar='C',help='Classifier to use on image',required=True)
parser.add_argument('--input',type=str,nargs='?',metavar='I',help='Input image file')
parser.add_argument('--dir',type=str,nargs='?',metavar='D',help='Image dir')
parser.add_argument('--scalefactor',type=float,nargs='?',metavar='S',default=1.3,help='detectMultiScale scale factor')
parser.add_argument('--minNeighbours',type=int,nargs='?',metavar='M',default=5,help='detectMultiScale min neighbours')
parser.add_argument('--windowSize',type=int,nargs='+',default=(1920,1080),help='Display window size')
args = parser.parse_args()

print(args)
if args.input and args.dir:
	print("Input and dir flags are mutually exclusive")
	exit(-1)

if not args.input and not args.dir:
	print("No input files provided")
	exit(-1)
cascade = cv2.CascadeClassifier(args.classifier)

if not cascade:
	print("Unable to create classifier from input: ",args.classifier)
	exit(-1)

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',args.windowSize[0],args.windowSize[1])
def showImg(file):
	img = cv2.imread(file)
	if img is None:
		print("Unable to open input file: ",file," ...skipping")
		return
	objects = cascade.detectMultiScale(img,args.scalefactor,args.minNeighbours)
	for(x,y,w,h) in objects:
		#print([x,y,w,h])
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255))
	cv2.imshow('image',img)

	while(True):
		key = cv2.waitKey(0)
		if  key & 0xFF == 27:
			exit(0)
		elif key & 0xFF == ord('s'):
			cv2.imwrite('tmp.jpg',img)
		else:
			break


if(args.input):
	showImg(args.input)
elif args.dir:
	for file in os.listdir(args.dir):
		showImg(args.dir + '/' + file)

cv2.destroyAllWindows()
