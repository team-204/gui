from __future__ import unicode_literals
import sys
import os
import csv
import random, numbers
import re
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
	from PySide import QtWidgets, QtCore
else:
	from PyQt5 import QtWidgets, QtCore
	from PyQt5.QtWidgets import QListWidget, QLineEdit, QLabel, QPushButton, QCheckBox, QInputDialog
	from PyQt5.QtGui import QFont
	
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

# format is [[x], [y], [alt]]
dataPoints = [[0.0],[0.0],[0.0]]
#exampleData = [[0, 3.5, 6.5, 10.5, 14.5, 19, 21.5, 23, 25, 26.5, 29, 30],[0, 6, 12.5, 18.5, 25, 33.5, 42, 49.5, 56, 62.5, 73, 81], [5.0, 5.8, 6.8, 7.9, 9.0, 10.0, 12.2, 14.0, 16.1, 17.9, 19.1, 20.1], [20.2, 20.1, 20.1, 20.0, 20.0, 19.9, 19.9, 20.0, 19.8, 19.6, 19.6, 19.5]]


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
		aw.setFocus()
		
		print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
		   ('double' if event.dblclick else 'single', event.button,
		   event.x, event.y, event.xdata, event.ydata))
		
		#rounding. Rounds to 1 decimal place, but this can be changed
		roundedX = round(event.xdata,1)
		roundedY = round(event.ydata,1)
		roundedAlt = round(float(aw.altitudeEdit.text()),1)
		
		if roundedX > 250:
			roundedX = 250
		elif roundedX < -250:
			roundedX = -250
		
		if roundedY > 250:
			roundedY = 250
		elif roundedY < -250:
			roundedY = -250
		
		self.addPoint(roundedX, roundedY, roundedAlt)
	
	def addPoint(self, xPoint, yPoint, altitude):
		lenCoords = len(dataPoints[0])
		coordExists = False
		
		for i in range(0,lenCoords):
			if xPoint == dataPoints[0][i] and yPoint == dataPoints[1][i] and altitude == dataPoints[2][i]:
				coordExists = True
		
		# Checks if the current coordinate exists (including altitude). Currently disabled, but if we want it back uncomment the next line and fix the indentation accordingly
		#if coordExists == False:
		dataPoints[0].append(xPoint)
		dataPoints[1].append(yPoint)
		dataPoints[2].append(altitude)
		print("added a point at (" + str(dataPoints[0][lenCoords]) + ", " + str(dataPoints[1][lenCoords]) + ")  Alt: " + str(dataPoints[2][lenCoords]))
		aw.list.addItem(str(lenCoords + 1) + ".  " + "(" + str(dataPoints[0][lenCoords]) + ", " + str(dataPoints[1][lenCoords]) + ")  Alt: " + str(dataPoints[2][lenCoords]))
		
		

		self.axes.cla()
		self.axes.plot(dataPoints[0],dataPoints[1],c='c',linestyle='dashed',marker='o')
		self.axes.set_xlabel('Relative Position, West/East (m)')
		self.axes.set_ylabel('Relative Position, South/North (m)')
		self.axes.set_title('Flight Path Definition')
		self.axes.set_xlim(-270,270)
		self.axes.set_ylim(-270,270)
		
		# Annotation happens here, see what the rest of the group thinks
		
		#if(altitudeCheckBox
		
		for i in range(0, len(dataPoints[0])):
			if aw.altitudeCheckBox.isChecked():
				self.axes.annotate(str(dataPoints[2][i]) + ' m', (dataPoints[0][i] - 10, dataPoints[1][i] + 20))
			
			self.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3*len(str(i+1)), dataPoints[1][i] - 8),  size=8)
			
		self.draw()
	
	# Edit a point
	#def listItemDoubleClicked(self):
		
	
	def removePoint(self, indexToRemove):
		del dataPoints[0][indexToRemove]
		del dataPoints[1][indexToRemove]
		del dataPoints[2][indexToRemove]
		self.axes.cla()
		self.axes.plot(dataPoints[0],dataPoints[1],c='c',linestyle='dashed',marker='o')
		self.axes.set_xlabel('Relative Position, West/East (m)')
		self.axes.set_ylabel('Relative Position, South/North (m)')
		self.axes.set_title('Flight Path Definition')
		self.axes.set_xlim(-270,270)
		self.axes.set_ylim(-270,270)
		
		aw.list.clear()
		
		for i in range(0, len(dataPoints[0])):
			if aw.altitudeCheckBox.isChecked():
				self.axes.annotate(str(dataPoints[2][i]) + ' m', (dataPoints[0][i] - 10, dataPoints[1][i] + 20))
			
			self.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3*len(str(i+1)), dataPoints[1][i] - 8),  size=8)

			aw.list.addItem(str(i + 1) + ".  " + "(" + str(dataPoints[0][i]) + ", " + str(dataPoints[1][i]) + ")  Alt: " + str(dataPoints[2][i]))

		
		
		self.draw()

	def compute_initial_figure(self):
		self.axes.plot(dataPoints[0],dataPoints[1],c='c',linestyle='dashed',marker='o')
		#self.axes.plot(exampleData[0],exampleData[1],c='b',marker='o')
		self.axes.set_xlim(-270,270)
		self.axes.set_ylim(-270,270)
		self.axes.set_xlabel('Relative Position, West/East (m)')
		self.axes.set_ylabel('Relative Position, South/North (m)')
		self.axes.set_title('Flight Path Definition')
	


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
		self.dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
		self.list = QListWidget(self)
		self.list.setFont(QFont('Courier'))
		self.list.doubleClicked.connect(self.listItemDoubleClicked)
		#l.addWidget(sc)
		self.xEdit = QLineEdit()
		self.yEdit = QLineEdit()
		self.altitudeEdit = QLineEdit()
		
		self.xEdit.setText('0')
		self.yEdit.setText('0')
		self.altitudeEdit.setText('0')
		
		self.xLabel = QLabel('X Coordinate')
		self.yLabel = QLabel('Y Coordinate')
		self.altitudeLabel = QLabel('Altitude (meters)')
		self.gpsLabel = QLabel('      Use GPS as position')
	
		self.addButton = QPushButton("Add Point")
		self.addButton.clicked.connect(self.addPointButtonClicked)
		self.startButton = QPushButton("Begin")
		self.startButton.clicked.connect(self.beginButtonClicked)
		self.threeDButton = QPushButton("3D Plot")
		self.threeDButton.clicked.connect(self.threeDButtonClicked)		
		self.gpsCheckBox = QCheckBox()
		
		self.altitudeCheckBox = QCheckBox()
		self.altitudeCheckBoxLabel = QLabel('      Show altitude annotations')
		self.altitudeCheckBox.stateChanged.connect(self.altitudeCheckBoxClicked)
		self.altitudeCheckBox.toggle()
		
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
		l.addWidget(self.threeDButton, 3, 0, 1, 1)
		l.addWidget(self.altitudeCheckBoxLabel, 0, 4, 1, 1)
		l.addWidget(self.altitudeCheckBox, 0, 4, 1, 1)

		
		l.addWidget(self.dc, 2, 0, 1, 3)
		l.addWidget(self.list, 2, 3, 1, 2)
		
		#self.addButton.clicked.connect(dc.addPoint(str(self.xEdit.text()), str(self.yEdit.text()), str(self.altitudeEdit.text())))
		
		lenCoords = len(dataPoints[0])
		for i in range(0,lenCoords):
			self.list.addItem(str(i + 1) + ".  " + "(" + str(dataPoints[0][i]) + ", " + str(dataPoints[1][i]) + ")  Alt: " + str(dataPoints[2][i]))

		#lenCoords = len(exampleData[0])
		#for i in range(0,lenCoords):
			#self.list.addItem("(" + str(exampleData[0][i]) + ", " + str(exampleData[1][i]) + ")  Altitude: " + str(exampleData[2][i]) + "   Temp: " + str(exampleData[3][i]) + " °C")
		#	self.list.addItem('{:16s} {:18s} {:18s}'.format("(" + str(exampleData[0][i]) + ", " + str(exampleData[1][i]) + ")", "Altitude: " + str(exampleData[2][i]), "Temp: " + str(exampleData[3][i]) + " °C"))
		
		self.main_widget.setFocus()
		self.setCentralWidget(self.main_widget)


		self.statusBar().showMessage("All hail matplotlib!", 2000)
	
	#def buttonClicked(self, dc):
	#	dc.addPoint(self, str(self.xEdit.text()), str(self.yEdit.text()), str(self.altitudeEdit.text()))
	
	def fileQuit(self):
		self.close()

	def closeEvent(self, ce):
		self.fileQuit()
	
	def altitudeCheckBoxClicked(self):
		self.dc.axes.cla()
		self.dc.axes.plot(dataPoints[0],dataPoints[1],c='c',linestyle='dashed',marker='o')
		self.dc.axes.set_xlabel('Relative Position, West/East (m)')
		self.dc.axes.set_ylabel('Relative Position, South/North (m)')
		self.dc.axes.set_title('Flight Path Definition')
		self.dc.axes.set_xlim(-270,270)
		self.dc.axes.set_ylim(-270,270)
		
		if self.altitudeCheckBox.isChecked():
			
			for i in range(0, len(dataPoints[0])):
				self.dc.axes.annotate(str(dataPoints[2][i]) + ' m', (dataPoints[0][i] - 10, dataPoints[1][i] + 20))
			
				self.dc.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3*len(str(i+1)), dataPoints[1][i] - 8),  size=8)
			
			self.dc.draw()
		else:
			for i in range(0, len(dataPoints[0])):
				self.dc.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3*len(str(i+1)), dataPoints[1][i] - 8),  size=8)
			
			self.dc.draw()
	
	def listItemDoubleClicked(self):
		editedRow = self.list.currentRow()
		s = str(dataPoints[0][editedRow]) + ', ' + str(dataPoints[1][editedRow]) + ', ' + str(dataPoints[2][editedRow])
		t, okPressed = QInputDialog.getText(self, "Edit waypoint", "Format: X, Y, Alt", QLineEdit.Normal, s)
		if okPressed:
			if re.match('[-+]?[0-9]*\.?[0-9]+, [-+]?[0-9]*\.?[0-9]+, [-+]?[0-9]*\.?[0-9]+', t):
				editX, editY, editAlt = t.split(', ')
				dataPoints[0][editedRow] = float(editX)
				dataPoints[1][editedRow] = float(editY)
				dataPoints[2][editedRow] = float(editAlt)
				self.list.currentItem().setText(str(editedRow + 1) + ".  " + "(" + str(dataPoints[0][editedRow]) + ", " + str(dataPoints[1][editedRow]) + ")  Alt: " + str(dataPoints[2][editedRow]))
			else:
				QtWidgets.QMessageBox.about(self, "Unsaved edit", "Invalid format")
	
	def addPointButtonClicked(self):
		lenCoords = len(dataPoints[0])
		
		newX = self.xEdit.text()
		newY = self.yEdit.text()
		newAlt = self.altitudeEdit.text()
		
		if isinstance(float(newX), numbers.Number) and isinstance(float(newY), numbers.Number) and isinstance(float(newAlt), numbers.Number):
			dataPoints[0].append(float(newX))
			dataPoints[1].append(float(newY))
			dataPoints[2].append(float(newAlt))
			print("added a point at (" + str(dataPoints[0][lenCoords]) + ", " + str(dataPoints[1][lenCoords]) + ")  Alt: " + str(dataPoints[2][lenCoords]))
			self.list.addItem(str(lenCoords + 1) + ".  " + "(" + str(dataPoints[0][lenCoords]) + ", " + str(dataPoints[1][lenCoords]) + ")  Alt: " + str(dataPoints[2][lenCoords]))
		
			self.dc.axes.cla()
			self.dc.axes.plot(dataPoints[0],dataPoints[1],c='c',linestyle='dashed',marker='o')
			self.dc.axes.set_xlabel('Relative Position, West/East (m)')
			self.dc.axes.set_ylabel('Relative Position, South/North (m)')
			self.dc.axes.set_title('Flight Path Definition')
			self.dc.axes.set_xlim(-270,270)
			self.dc.axes.set_ylim(-270,270)
			
			if self.altitudeCheckBox.isChecked():	
				
				for i in range(0, len(dataPoints[0])):
					self.dc.axes.annotate(str(dataPoints[2][i]) + ' m', (dataPoints[0][i] - 10, dataPoints[1][i] + 20))
			
					self.dc.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3*len(str(i+1)), dataPoints[1][i] - 8),  size=8)

			else:
				for i in range(0, len(dataPoints[0])):
					self.dc.axes.annotate(str(i + 1), (dataPoints[0][i] - 2.5 - 3*len(str(i+1)), dataPoints[1][i] - 8),  size=8)
				
			
			self.dc.draw()
	
	def beginButtonClicked(self):
		lenCoords = len(dataPoints[0])
		with open('data.csv', 'w') as csvfile:
			fieldnames = ['xVal','yVal','altitude']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			
			writer.writeheader()
			for i in range(0, lenCoords):
				writer.writerow({'xVal': str(dataPoints[0][i]), 'yVal': str(dataPoints[1][i]), 'altitude': str(dataPoints[2][i])})
		
		msg = QtWidgets.QMessageBox()
		reply = msg.question(self, 'Begin Flight?', "Flight path saved to data.csv. Are you sure you want to begin flight?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
		msg.exec_()
		
	def threeDButtonClicked(self):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		ax.scatter(dataPoints[0], dataPoints[1], dataPoints[2], c='r', linestyle='dashed', marker='o')
		ax.plot(dataPoints[0],dataPoints[1],dataPoints[2], color='r')

		ax.set_xlabel('Relative Position, West/East (m)')
		ax.set_ylabel('Relative Position, South/North (m)')
		ax.set_zlabel('Relative Altitude (m)')

		ax.set_xlim(-270,270)
		ax.set_ylim(-270,270)
		ax.set_zlim(0, 25)

		plt.show()
		
	# Make sure to check if any row is selected here to avoid crash
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Delete:
			deletedRow = self.list.currentRow()
			if deletedRow >= 0:
				print('deleted ' + str(deletedRow))
				self.list.takeItem(deletedRow)
				self.dc.removePoint(deletedRow)
		
		# Left and Right key to increase or decrease altitude
		if event.key() == QtCore.Qt.Key_Right:
			self.altitudeEdit.setText(str(int(self.altitudeEdit.text()) + 1))
		elif event.key() == QtCore.Qt.Key_Left:
			self.altitudeEdit.setText(str(int(self.altitudeEdit.text()) - 1))
			
		if event.modifiers() & QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Z:
			rowToDelete = len(dataPoints[0])-1 
			if rowToDelete != 0:
				print('deleted ' + str(rowToDelete))
				self.list.takeItem(rowToDelete)
				self.dc.removePoint(rowToDelete)
			
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