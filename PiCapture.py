#
#
#
#
#

import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import picamera
import io

import requests
import datetime
import os
import uuid




def upload(filename,ripe='F'):
    #URL of Flask server (assuming localhost)
    #url = "http://127.0.0.1:5000/upload"
    url = "http://watermelon-flask.hp7jzffnep.ap-southeast-2.elasticbeanstalk.com/upload"
    # File array for request
    files = {'files': open(filename, 'rb')}
  
    datetime_result = datetime.datetime.now()
    unique_id = str(uuid.uuid4()) + os.path.splitext(filename)[-1]

    data = {'r': ripe, 'd': datetime_result, 'k': unique_id}
    # Add both the file image to upload, and accompanying data and POST
    r = requests.post(url, files=files, data=data)
    print(str(r.content))
class VideoCapture(QtWidgets.QWidget):
    def __init__(self,parent):
        super(QtWidgets.QWidget,self).__init__()
        self.camera = picamera.PiCamera()
        self.stream = io.BytesIO()
        self.camera.resolution = (1024,768)
        self.video_frame = QtWidgets.QLabel()
        parent.layout.addWidget(self.video_frame)
        self.refresh_rate = 1000/30

    def nextFrame(self):
        #Capture frame-by-frame
        stream = io.BytesIO()
        self.camera.capture(stream,use_video_port='true',format='rgb')
        stream.seek(0)
        #Display frame
        res = self.camera.resolution
        frame = stream.read(-1)
        self.img = QtGui.QImage(frame,res[0],res[1],QtGui.QImage.Format_RGB888)
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

        # self.startButton = QtWidgets.QPushButton('Start',parent)
        # self.startButton.clicked.connect(parent.startCapture)
        # self.startButton.setFixedWidth(50)

        self.captureButton = QtWidgets.QPushButton('ripe',parent)
        self.captureButton.clicked.connect(parent.captureRipeImg)
        self.unripebutton = QtWidgets.QPushButton('unripe',parent)
        self.unripebutton.clicked.connect(parent.captureUnripeImg)
        self.layout.addRow(self.captureButton)
        self.layout.addRow(self.unripebutton)
        self.setLayout(self.layout)
        self.ripe = 'F'



class ControlWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ControlWindow,self).__init__()
        self.setGeometry(100,100,1024,768)
        self.setWindowTitle("Capture Window")
        self.capture = None
        self.filename = 'tmp.jpg'

        self.VideoDisplay = VideoDisplay(self)
        self.setCentralWidget(self.VideoDisplay)

    @QtCore.pyqtSlot()
    def startCapture(self):
        if not self.capture:
            self.capture = VideoCapture(self.VideoDisplay)
        self.capture.start()

    @QtCore.pyqtSlot()
    def captureRipeImg(self):
        ripe = 'T'
        self.Capture(ripe)
    @QtCore.pyqtSlot()
    def captureUnripeImg(self):
        ripe = 'F'
        self.Capture(ripe)

    def Capture(self,ripe):
        if self.capture:
            self.capture.pause()
            self.capture.captureImg(self.filename)
            upload(filename,ripe=ripe)
            self.capture.resume()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ControlWindow()
    window.show()
    window.startCapture()
    sys.exit(app.exec_())
