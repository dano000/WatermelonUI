#
#
#
#
#
import sys
import numpy as np
import cv2
import time
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFormLayout,QLabel
import picamera
import picamera.array
import os.path


if not ( os.path.exists(cv2.__path__[0] + '/data/haarcascade_frontalface_default.xml') and
     os.path.exists(cv2.__path__[0] + '/data/haarcascade_eye.xml')):
        print('Unable to find default opencv classifiers')
        exit(-1)
face_cascade = cv2.CascadeClassifier(cv2.__path__[0] + '/data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.__path__[0] + '/data/haarcascade_eye.xml')


class VideoCapture():
	def __init__(self,draw_frame):
		self.cap = picamera.PiCamera()#webcam
		self.cap.resolution = (512,400)
		self.frame = picamera.array.PiRGBArray(self.cap)
		self.draw_frame=draw_frame
		self.refresh_rate = 1000.0/30
	def nextFrame(self):
		#Capture frame-by-frame
		self.cap.capture(self.frame,use_video_port='true',format='rgb')
		frame = self.frame.array
                #Perform operation on frame
		#frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		frame = self.process(frame)
		#Display frame
		self.img = QtGui.QImage(frame,frame.shape[1],frame.shape[0],QtGui.QImage.Format_RGB888)
		pix = QtGui.QPixmap.fromImage(self.img)
		self.draw_frame.videoframe.setPixmap(pix)
		self.frame.truncate(0)

	def start(self):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.nextFrame)
		self.timer.start(self.refresh_rate)

	def pause(self):
		self.timer.stop()

	def resume(self):
		self.timer.start(self.refresh_rate)
	def process(self,frame):
		gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		#detect faces
		faces = face_cascade.detectMultiScale(gray,1.3,5)
		roi_color = frame
		alpha = .5
		beta = 1 - alpha
		blend_col = (0,0,0)
		#draw rectangle around face
		for (x,y,w,h) in faces:
                        
			roi_gray = gray[y:y+h, x:x+w]
			
			eyes = eye_cascade.detectMultiScale(roi_gray)
                        #shade the frame
			#frame *= beta
			#frame += np.asarray(blend_col)*alpha
			frame = (np.asarray(blend_col)*alpha + frame * beta).astype(np.uint8)
			#Apply red rectangangle around face
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

			#Get region of interest
			roi_color = frame[y:y+h, x:x+w]
                       
			#Remove shading over region of interest
			np.copyto(roi_color,(np.asarray(blend_col)*-alpha + roi_color/beta).astype(np.uint8))
		
			for (ex,ey,ew,eh) in eyes:
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


		return frame



class VideoDisplay(QtWidgets.QWidget):
	def __init__(self,parent):
		super(VideoDisplay,self).__init__(parent)

		self.layout = QFormLayout(self)
		self.videoframe = QLabel('vidframe')
		self.layout.addRow(self.videoframe)
		self.setLayout(self.layout)




class ControlWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(ControlWindow,self).__init__()
		self.setGeometry(100,100,1024,768)
		self.setWindowTitle("FaceDetector")
		self.capture = None
	

		self.VideoDisplay = VideoDisplay(self)
		self.setCentralWidget(self.VideoDisplay)

app = QtWidgets.QApplication(sys.argv)
window = ControlWindow()
window.showMaximized()
vid = VideoCapture(window.VideoDisplay)
vid.start()
sys.exit(app.exec_())
