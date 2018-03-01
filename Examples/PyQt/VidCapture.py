#
#
#
#
#
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import cv2


class VideoCapture(QtWidgets.QWidget):
	def __init__(self,parent):
		super(QtWidgets.QWidget,self).__init__()
		self.cap = cv2.VideoCapture(0)#webcam
		self.video_frame = QtWidgets.QLabel()
		parent.layout.addWidget(self.video_frame)
		self.refresh_rate = 1000.0/30
	def nextFrame(self):
		#Capture frame-by-frame
		ret,frame = self.cap.read()
		#Perform operation on fram
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		#Display frame
		self.img = QtGui.QImage(frame,frame.shape[1],frame.shape[0],QtGui.QImage.Format_RGB888)
		pix = QtGui.QPixmap.fromImage(self.img)
		self.video_frame.setPixmap(pix)

	def start(self):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.nextFrame)
		self.timer.start(self.refresh_rate)

	def pause(self):
		self.timer.stop()

	def resume(self):
		self.timer.start(self.refresh_rate)

	def captureImg(self,filename):
		print(filename)
		self.img.save(filename)


class VideoDisplay(QtWidgets.QWidget):
	def __init__(self,parent):
		super(VideoDisplay,self).__init__(parent)

		self.layout = QtWidgets.QFormLayout(self)

		self.startButton = QtWidgets.QPushButton('Start',parent)
		self.startButton.clicked.connect(parent.startCapture)
		self.startButton.setFixedWidth(50)

		self.captureButton = QtWidgets.QPushButton('Capture',parent)
		self.captureButton.clicked.connect(parent.captureImg)
		self.layout.addRow(self.startButton,self.captureButton)
		self.setLayout(self.layout)



class ControlWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(ControlWindow,self).__init__()
		self.setGeometry(100,100,1024,768)
		self.setWindowTitle("Capture Window")
		self.capture = None

		self.VideoDisplay = VideoDisplay(self)
		self.setCentralWidget(self.VideoDisplay)

	@QtCore.pyqtSlot()
	def startCapture(self):
		if not self.capture:
			self.capture = VideoCapture(self.VideoDisplay)
		self.capture.start()

	@QtCore.pyqtSlot()
	def captureImg(self):
		if self.capture:
			self.capture.pause()
			filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save image as","","Images (*.png)")
			self.capture.captureImg(filename)
			self.capture.resume()
	
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ControlWindow()
    window.show()
    window.startCapture()
    sys.exit(app.exec_())