#
#
#
#
#

import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QPushButton,QLabel,QSlider,QGridLayout

import picamera
import picamera.array

import time
import requests
import datetime
import os
import uuid

save_path = './'


def upload(filename,ripe='F'):
        #URL of Flask server (assuming localhost)
        #url = "http://127.0.0.1:5000/upload"
        url = "http://watermelon-flask.hp7jzffnep.ap-southeast-2.elasticbeanstalk.com/upload"
        # # File array for request
        files = {'files': open(filename, 'rb')}

        datetime_result = datetime.datetime.now()
        unique_id = filename

        data = {'r': ripe, 'd': datetime_result, 'k': unique_id}
        # Add both the file image to upload, and accompanying data and POST
        r = requests.post(url, files=files, data=data)
        print(str(r.content))

class VideoCapture(QtWidgets.QWidget):
        def __init__(self,parent):
                super(QtWidgets.QWidget,self).__init__()
                self.camera = picamera.PiCamera()
                self.stream = picamera.array.PiRGBArray(self.camera)
                self.parent = parent
                self.vid_res = (512,389)
                self.camera.resolution = self.vid_res
                self.hq_res = (1920,1080)
                self.refresh_rate = 1000/30

        def nextFrame(self):
                #Capture frame-by-frames
                self.camera.resolution = self.vid_res
                self.camera.capture(self.stream,use_video_port='true',format='rgb')
                self.stream.seek(0)
                #Display frame
                frame = self.stream.array
                pix = QtGui.QPixmap.fromImage(QtGui.QImage(frame,frame.shape[1],frame.shape[0],QtGui.QImage.Format_RGB888))
                self.parent.videoframe.setPixmap(pix)
                self.stream.truncate(0)
        def start(self):
                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self.nextFrame)
                self.timer.start(self.refresh_rate)

        def pause(self):
                self.timer.stop()

        def resume(self):
                self.timer.start(self.refresh_rate)

        def captureImg(self,filename):
                start_time = time.time()
                self.camera.resolution = self.hq_res
                self.camera.capture(self.stream,use_video_port='false',format='rgb')
                print(time.time()-start_time)

                frame = self.stream.array
                img = QtGui.QImage(frame,frame.shape[1],frame.shape[0],QtGui.QImage.Format_RGB888)
                img.save(save_path+filename)
                self.stream.truncate(0)



class VideoDisplay(QtWidgets.QWidget):
        def __init__(self,parent):
                super(VideoDisplay,self).__init__(parent)
                self.parent = parent
                self.layout = QGridLayout(self)


                self.ripebutton = QPushButton('ripe',parent)
                self.unripebutton = QPushButton('unripe',parent)

                self.countlabel = QLabel('count')
                self.count = QLabel()

                self.countslider = QSlider(QtCore.Qt.Vertical)
                self.countslider.setMaximum(100)
                self.countslider.setMinimum(1)
                self.countslider.setValue(1)
                self.count.setNum(self.countslider.value())

                self.intervallabel = QLabel('interval (ms)')
                self.interval = QLabel()
                self.interval.setNum(0)

                self.intervalslider = QSlider(QtCore.Qt.Vertical)
                self.intervalslider.setMaximum(1000)
                self.intervalslider.setMinimum(1)
                self.intervalslider.setValue(30)
                self.interval.setNum(self.intervalslider.value())

                self.videoframe = QLabel('vidframe')

                self.layout.addWidget(self.ripebutton,0,0)
                self.layout.addWidget(self.unripebutton,6,0)
                self.layout.addWidget(self.countlabel,0,5)
                self.layout.addWidget(self.count,1,5)
                self.layout.addWidget(self.countslider,2,5,5,1)
                self.layout.addWidget(self.intervallabel,0,6)
                self.layout.addWidget(self.interval,1,6)
                self.layout.addWidget(self.intervalslider,2,6,5,1)
                self.layout.addWidget(self.videoframe,0,1,6,3)
                self.setLayout(self.layout)


                self.countslider.valueChanged.connect(self.updateCount)
                self.intervalslider.valueChanged.connect(self.updateInterval)

                self.ripebutton.clicked.connect(parent.captureRipeImg)
                self.unripebutton.clicked.connect(parent.captureUnripeImg)

                self.capture_count = 0;
        @QtCore.pyqtSlot()
        def updateCount(self):
                self.count.setNum(self.countslider.value())

        @QtCore.pyqtSlot()
        def updateInterval(self):
                self.interval.setNum(self.intervalslider.value())

        def start(self):
                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self.capture)
                self.timer.start(self.intervalslider.value())

        def stop(self):
                self.timer.stop()

        @QtCore.pyqtSlot()
        def capture(self):
                self.parent.Capture()
                self.capture_count += 1
                if self.capture_count >= self.countslider.value():
                        self.stop()
                        self.capture_count = 0

class ControlWindow(QtWidgets.QMainWindow):
        def __init__(self):
                super(ControlWindow,self).__init__()
                self.setGeometry(100,100,1024,768)
                self.setWindowTitle("Capture Window")
                self.capture = None
                self.VideoDisplay = VideoDisplay(self)
                self.setCentralWidget(self.VideoDisplay)
                self.ripe = 'F'
        def start(self):
                if not self.capture:
                        self.capture = VideoCapture(self.VideoDisplay)
                self.capture.start()

        @QtCore.pyqtSlot()
        def startCapture(self):
                self.capture.start()

        @QtCore.pyqtSlot()
        def captureRipeImg(self):
                self.ripe = 'T'
                self.VideoDisplay.start()
        @QtCore.pyqtSlot()
        def captureUnripeImg(self):
                ripe = 'F'
                self.VideoDisplay.start()

                

        def Capture(self):
                if self.capture:
                        self.capture.pause()
                        unique_id = str(uuid.uuid4()) + os.path.splitext('tmp.jpg')[-1]
                        self.capture.captureImg(unique_id)
                        upload(unique_id,ripe=self.ripe)
                        self.capture.resume()

if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = ControlWindow()
        window.show()
        window.start()
        sys.exit(app.exec_())
