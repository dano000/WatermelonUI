#
#
#
#
#

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):
	
	def __init__(self):
		super.__init__()
		self.title = 'Small window example'
		self.left = 100
		self.top = 100
		self.width = 400
		self.height = 140
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		# Create label
		self.label = QLabel(self)
		self.label.setText("OldText")
		self.label.move(20, 20)
		self.label.resize(280,40)

		# Create a button in the window
		self.button = QPushButton('Show text', self)
		self.button.move(20,80)

		# connect button to function on_click
		self.button.clicked.connect(self.on_click)
		self.show()

	@pyqtSlot()
	def on_click(self):
		textboxValue = self.label.setText("New text")

 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())