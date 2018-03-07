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
face_cascade = cv2.CascadeClassifier(cv2.__path__[0] + '\data\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.__path__[0] + '\data\haarcascade_eye.xml')


class VideoCapture():
	def __init__(self,draw_frame):
		self.cap = cv2.VideoCapture(0)#webcam
		self.draw_frame=draw_frame
		self.refresh_rate = 1000.0/30
	def nextFrame(self):
		#Capture frame-by-frame
		ret,frame = self.cap.read()
		#Perform operation on fram
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		frame = self.process(frame)
		#Display frame
		self.img = QtGui.QImage(frame,frame.shape[1],frame.shape[0],QtGui.QImage.Format_RGB888)
		pix = QtGui.QPixmap.fromImage(self.img)
		self.draw_frame.videoframe.setPixmap(pix)

	def start(self):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.nextFrame)
		self.timer.start(self.refresh_rate)

	def pause(self):
		self.timer.stop()

	def resume(self):
		self.timer.start(self.refresh_rate)
	def process(self,frame):
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

		#detect faces
		faces = face_cascade.detectMultiScale(gray,1.3,5)

		#draw rectangle around face
		for (x,y,w,h) in faces:
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
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
		self.setWindowTitle("Capture Window")
		self.capture = None
		self.filename = 'tmp.jpg'

		self.VideoDisplay = VideoDisplay(self)
		self.setCentralWidget(self.VideoDisplay)

app = QtWidgets.QApplication(sys.argv)
window = ControlWindow()
window.show()
vid = VideoCapture(window.VideoDisplay)
vid.start()
sys.exit(app.exec_())
