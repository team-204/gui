from __future__ import unicode_literals
import sys
import os
import random
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
	from PySide import QtWidgets, QtCore
else:
	from PyQt5 import QtWidgets, QtCore
	from PyQt5.QtWidgets import QListWidget, QLineEdit, QLabel, QPushButton, QCheckBox
	from PyQt5.QtGui import QFont
	
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

dataPoints = [[0,20,30,80,150],[0,40,80,20,200],[5, 10, 20, 20, 25]]
exampleData = [[0, 3.5, 6.5, 10.5, 14.5, 19, 21.5, 23, 25, 26.5, 29, 30],[0, 6, 12.5, 18.5, 25, 33.5, 42, 49.5, 56, 62.5, 73, 81], [5.0, 5.8, 6.8, 7.9, 9.0, 10.0, 12.2, 14.0, 16.1, 17.9, 19.1, 20.1], [20.2, 20.1, 20.1, 20.0, 20.0, 19.9, 19.9, 20.0, 19.8, 19.6, 19.6, 19.5]]
#dataPoints = [[0], [1], [50]]

class MyMplCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		self.compute_initial_figure()

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
								   QtWidgets.QSizePolicy.Expanding,
								   QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def compute_initial_figure(self):
		pass


class MyStaticMplCanvas(MyMplCanvas):
	"""Simple canvas with a sine plot."""

	def compute_initial_figure(self):
		t = arange(0.0, 3.0, 0.01)
		s = sin(2*pi*t)
		self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
	"""A canvas that updates itself every second with a new plot."""
	
	def __init__(self, *args, **kwargs):
		MyMplCanvas.__init__(self, *args, **kwargs)
		#timer = QtCore.QTimer(self)
		#timer.timeout.connect(self.update_figure)
		#timer.start(1000)
		cid = self.mpl_connect('button_press_event', self.onclick)

	def onclick(self, event):
		print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
		   ('double' if event.dblclick else 'single', event.button,
		   event.x, event.y, event.xdata, event.ydata))
		
		#rounding, can be commented out. Rounds to two decimal places
		roundedX = round(event.xdata,2)
		roundedY = round(event.ydata,2)
		
		self.addPoint(roundedX, roundedY, 0)
	
	def addPoint(self, xPoint, yPoint, altitude):
		lenCoords = len(dataPoints[0])
		coordExists = False
		
		for i in range(0,lenCoords):
			if xPoint == dataPoints[0][i] and yPoint == dataPoints[1][i]:
				coordExists = True
		
		if coordExists == False:
			dataPoints[0].append(xPoint)
			dataPoints[1].append(yPoint)
			dataPoints[2].append(altitude)
			print("added a point at (" + str(dataPoints[0][lenCoords]) + ", " + str(dataPoints[1][lenCoords]) + ")  Altitude: " + str(dataPoints[2][lenCoords]))
			aw.list.addItem("(" + str(dataPoints[0][lenCoords]) + ", " + str(dataPoints[1][lenCoords]) + ")  Altitude: " + str(dataPoints[2][lenCoords]))
		
			#dataPoints[0].append(event.xdata)
			#dataPoints[1].append(event.ydata)
			#print(dataPoints)
			self.axes.cla()
			self.axes.plot(dataPoints[0],dataPoints[1],linestyle='dashed',marker='o')
			self.draw()

	def compute_initial_figure(self):
		#self.axes.plot(dataPoints[0],dataPoints[1],linestyle='dashed',marker='o')
		self.axes.plot(exampleData[0],exampleData[1],c='b',marker='o')
		self.axes.set_xlim(-250,250)
		self.axes.set_ylim(-250,250)
		self.axes.set_xlabel('Relative Position, West/East (m)')
		self.axes.set_ylabel('Relative Position, South/North (m)')
		self.axes.set_title('Data Acquisition')

	def update_figure(self):
		# Build a list of 4 random integers between 0 and 10 (both inclusive)
		#l = [random.randint(0, 10) for i in range(4)]
		self.axes.cla()
		self.axes.plot([0, 1, 2, 3], l, 'r.')
		self.draw()	
	


class ApplicationWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setWindowTitle("application main window")

		self.file_menu = QtWidgets.QMenu('&File', self)
		self.file_menu.addAction('&Quit', self.fileQuit,
								 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
		self.menuBar().addMenu(self.file_menu)

		self.help_menu = QtWidgets.QMenu('&Help', self)
		self.menuBar().addSeparator()
		self.menuBar().addMenu(self.help_menu)

		self.help_menu.addAction('&About', self.about)

		self.main_widget = QtWidgets.QWidget(self)

		l = QtWidgets.QGridLayout(self.main_widget)
		#sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
		dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
		self.list = QListWidget(self)
		self.list.setFont(QFont('Courier'))
		self.list.setMinimumWidth(self.list.sizeHintForColumn(0))
		#l.addWidget(sc)
		self.xEdit = QLineEdit()
		self.yEdit = QLineEdit()
		self.altitudeEdit = QLineEdit()
		
		self.xLabel = QLabel('X Coordinate')
		self.yLabel = QLabel('Y Coordinate')
		self.altitudeLabel = QLabel('Altitude (meters)')
		self.gpsLabel = QLabel('      Use GPS as position')
		
		self.addButton = QPushButton("Add Point")
		self.startButton = QPushButton("Begin")
		self.gpsCheckBox = QCheckBox()
		
		l.addWidget(self.xLabel, 0, 0, 1, 1)
		l.addWidget(self.yLabel, 0, 1, 1, 1)
		l.addWidget(self.altitudeLabel, 0, 2, 1, 1)
		l.addWidget(self.gpsLabel, 1, 4, 1, 1)
		
		l.addWidget(self.xEdit, 1, 0, 1, 1)
		l.addWidget(self.yEdit, 1, 1, 1, 1)
		l.addWidget(self.altitudeEdit, 1, 2, 1, 1)
		l.addWidget(self.addButton, 1, 3, 1, 1)
		l.addWidget(self.gpsCheckBox, 1, 4, 1, 1)
		l.addWidget(self.startButton, 3, 4, 1, 1)
		
		l.addWidget(dc, 2, 0, 1, 3)
		l.addWidget(self.list, 2, 3, 1, 10)
		
		#self.addButton.clicked.connect(dc.addPoint(str(self.xEdit.text()), str(self.yEdit.text()), str(self.altitudeEdit.text())))
		
		#lenCoords = len(dataPoints[0])
		#for i in range(0,lenCoords):
		#	self.list.addItem("(" + str(dataPoints[0][i]) + ", " + str(dataPoints[1][i]) + ")  Altitude: " + str(dataPoints[2][i]))

		lenCoords = len(exampleData[0])
		for i in range(0,lenCoords):
			#self.list.addItem("(" + str(exampleData[0][i]) + ", " + str(exampleData[1][i]) + ")  Altitude: " + str(exampleData[2][i]) + "   Temp: " + str(exampleData[3][i]) + " °C")
			self.list.addItem('{:12s} {:10s} {:12s}'.format("(" + str(exampleData[0][i]) + ", " + str(exampleData[1][i]) + ")", "Alt: " + str(exampleData[2][i]), "Temp: " + str(exampleData[3][i]) + " °C"))
		
		self.main_widget.setFocus()
		self.setCentralWidget(self.main_widget)


		self.statusBar().showMessage("All hail matplotlib!", 2000)
	
	#def buttonClicked(self, dc):
	#	dc.addPoint(self, str(self.xEdit.text()), str(self.yEdit.text()), str(self.altitudeEdit.text()))
	
	def fileQuit(self):
		self.close()

	def closeEvent(self, ce):
		self.fileQuit()

	def about(self):
		QtWidgets.QMessageBox.about(self, "About",
								"""embedding_in_qt4.py example
Copyright 2005 Florent Rougon, 2006 Darren Dale

This program is a simple example of a Qt4 application embedding matplotlib
canvases.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation."""
								)


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()