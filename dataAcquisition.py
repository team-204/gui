import os
import sys

from PyQt5 import QtCore,  QtGui, QtWidgets

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

from PyQt5.QtWidgets import QListWidget, QLineEdit, QLabel, QPushButton, QCheckBox

import matplotlib

from random import randint
import datetime
import time

starttime=time.time()
paramList = ["x","y","z","lat","lon","temp","time"]
paramLimits = [[-250, 250],[-250, 250],[-1,50],[33,34],[87,88],[0,30],["please do not click time","i mean it"]]
dictionaryLength=len(paramList)

# displayedParamList is the list that goes in xAxisList, yAxisList, zAxisList. For now the same as paramList.
displayedParamList = paramList

# commented out for testing
#dataCollected = []
#for x in range(0,dictionaryLength):
#	dataCollected.append([])			# because of code in QtMplCanvas.Time(), dataCollected is a list with the same index meaning as paramList (i.e. dataCollected[0] is the list of x values, dataCollected[1] is the list of y values, etc)

# testing
dataCollected = [[0],[0],[0],[33.2140], [87.5391], [25], [datetime.datetime.now()]]

class QtMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width = 6.5, height = 5.5, dpi = 100, sharex = None, sharey = None, fig = None):
		if fig == None:
			self.fig = Figure(figsize = (width, height), dpi=dpi, facecolor = '#FFFFFF')
			self.ax = self.fig.add_subplot(111, projection='3d')
			self.ax.set_xlim(paramLimits[0][0],paramLimits[0][1])
			self.ax.set_ylim(paramLimits[1][0],paramLimits[1][1])
			self.ax.set_zlim(paramLimits[2][0],paramLimits[2][1])
			self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
			self.ax.hold(True)
		else:
			self.fig = fig

		FigureCanvas.__init__(self, self.fig)
		FigureCanvas.setSizePolicy(self,
			QtWidgets.QSizePolicy.Expanding,
			QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		self.initUI()
		
	def initUI(self):
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.Time)
		self.timer.start(1000)

	def Time(self):
		# This is where data collection happens, currently a simulation
		# previousDict is unnecessary except for simulation
		previousDict = {"x":dataCollected[0][-1], "y":dataCollected[1][-1], "z":dataCollected[2][-1], "lat":dataCollected[3][-1], "lon":dataCollected[4][-1], "temp":dataCollected[5][-1], "time":dataCollected[6][-1]}
		currentDict = {"x":round(previousDict["x"]*1.3+1), "y":previousDict["y"]+4, "z":previousDict["z"]+randint(0,3), "lat": 33.2140, "lon": 87.5391, "temp":previousDict["temp"]+random.uniform(-0.2,0.2), "time":datetime.datetime.now()}
		print(previousDict)
		print(currentDict)
		
		for key, value in currentDict.items():
			ind = paramList.index(key)		# find the index w.r.t. paramList of the current key. This is the same index w.r.t. dataCollected
			dataCollected[ind].append(value)
			
		#print(currentDict)
		#print(dataCollected)
		#fix this next line so it's not so ugly and probably inefficient
		self.ax.scatter(currentDict[paramList[mplQt.xAxisList.currentRow()]], currentDict[paramList[mplQt.yAxisList.currentRow()]], currentDict[paramList[mplQt.zAxisList.currentRow()]], c='r', linestyle='dashed', marker='o')
		#self.ax.plot(currentDict['x'], currentDict['y'], currentDict['z'], color='r')
		self.fig.canvas.draw()
		plt.draw()                      # redraw the canvas
	
	def sizeHint(self):
		w, h = self.get_width_height()
		return QtCore.QSize(w, h)

	def minimumSizeHint(self):
		return QtCore.QSize(10, 10)

	def sizeHint(self):
		w, h = self.get_width_height()
		return QtCore.QSize(w, h)

	def minimumSizeHint(self):
		return QtCore.QSize(10, 10)


class MyNavigationToolbar(NavigationToolbar) :
	def __init__(self, parent, canvas, direction = 'h' ) :

		self.canvas = canvas
		QWidget.__init__( self, parent )

		if direction=='h' :
			self.layout = QHBoxLayout( self )
		else :
			self.layout = QVBoxLayout( self )

		self.layout.setMargin( 2 )
		self.layout.setSpacing( 0 )

		NavigationToolbar2.__init__( self, canvas )
		
	def set_message( self, s ):
		pass


class MPL_WIDGET_3D(QtWidgets.QWidget):
	def __init__(self, parent = None, enableAutoScale = False, enableCSV = False, enableEdit = False, fig = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.canvas = QtMplCanvas(fig)
		self.canvas.ax.mouse_init()
		#self.toolbar = NavigationToolbar(self.canvas, self.canvas)
		self.xAxisList = QListWidget()
		self.yAxisList = QListWidget()
		self.zAxisList = QListWidget()
		
		self.xAxisList.setFixedWidth(200)
		self.yAxisList.setFixedWidth(200)
		self.zAxisList.setFixedWidth(200)
		
		self.axesLimitsButton = QPushButton("Change Limits")
		self.xLimitLowLE = QLineEdit()
		self.yLimitLowLE = QLineEdit()
		self.zLimitLowLE = QLineEdit()
		self.xLimitHighLE = QLineEdit()
		self.yLimitHighLE = QLineEdit()
		self.zLimitHighLE = QLineEdit()
		
		self.xLimitLowLE.setText('-250')
		self.yLimitLowLE.setText('-250')
		self.zLimitLowLE.setText('0')
		self.xLimitHighLE.setText('250')
		self.yLimitHighLE.setText('250')
		self.zLimitHighLE.setText('50')
		
		
		self.xLimitLabel = QLabel("X Axis Limits:")
		self.yLimitLabel = QLabel("Y Axis Limits:")
		self.zLimitLabel = QLabel("Z Axis Limits:")
		self.xLimitLowLE.setFixedWidth(55)
		self.yLimitLowLE.setFixedWidth(55)
		self.zLimitLowLE.setFixedWidth(55)
		self.xLimitHighLE.setFixedWidth(55) 
		self.yLimitHighLE.setFixedWidth(55)
		self.zLimitHighLE.setFixedWidth(55)
		self.xLimitLabel.setFixedWidth(75)
		self.yLimitLabel.setFixedWidth(75)
		self.zLimitLabel.setFixedWidth(75)
		
		
		self.xAxisList.addItems(displayedParamList)
		self.yAxisList.addItems(displayedParamList)
		self.zAxisList.addItems(displayedParamList)
		self.xAxisList.setCurrentRow(0)
		self.yAxisList.setCurrentRow(1)
		self.zAxisList.setCurrentRow(2)
		
		self.axesLimitsButton.clicked.connect(self.axesLimitsButtonClicked)
		self.xAxisList.clicked.connect(self.listItemClicked)
		self.yAxisList.clicked.connect(self.listItemClicked)
		self.zAxisList.clicked.connect(self.listItemClicked)
		
		self.vbox = QtWidgets.QGridLayout()
		self.vbox.addWidget(self.canvas,0,0,6,1)
		#self.vbox.addWidget(self.toolbar,6,0,3,1)
		self.vbox.addWidget(self.xAxisList,0,1,1,3)
		self.vbox.addWidget(self.yAxisList,2,1,1,3)
		self.vbox.addWidget(self.zAxisList,4,1,1,3)
		self.vbox.addWidget(self.xLimitLabel, 1,1,1,1)
		self.vbox.addWidget(self.xLimitLowLE, 1,2,1,1)
		self.vbox.addWidget(self.xLimitHighLE, 1,3,1,1)
		self.vbox.addWidget(self.yLimitLabel, 3,1,1,1)
		self.vbox.addWidget(self.yLimitLowLE, 3,2,1,1)
		self.vbox.addWidget(self.yLimitHighLE, 3,3,1,1)
		self.vbox.addWidget(self.zLimitLabel, 5,1,1,1)
		self.vbox.addWidget(self.zLimitLowLE, 5,2,1,1)
		self.vbox.addWidget(self.zLimitHighLE, 5,3,1,1)
		self.vbox.addWidget(self.axesLimitsButton,6,2,1,2)
		self.setLayout(self.vbox)
	
	def listItemClicked(self):
		mplQt.canvas.ax.cla()
		xrow = mplQt.xAxisList.currentRow()
		yrow = mplQt.yAxisList.currentRow()
		zrow = mplQt.zAxisList.currentRow()
		self.xLimitLowLE.setText(str(paramLimits[xrow][0]))
		self.xLimitHighLE.setText(str(paramLimits[xrow][1]))
		self.yLimitLowLE.setText(str(paramLimits[yrow][0]))
		self.yLimitHighLE.setText(str(paramLimits[yrow][1]))
		self.zLimitLowLE.setText(str(paramLimits[zrow][0]))
		self.zLimitHighLE.setText(str(paramLimits[zrow][1]))
		mplQt.canvas.ax.scatter(dataCollected[xrow], dataCollected[yrow], dataCollected[zrow], c='r', linestyle='dashed', marker='o')
		mplQt.canvas.ax.set_xlim(paramLimits[xrow][0],paramLimits[xrow][1])
		mplQt.canvas.ax.set_ylim(paramLimits[yrow][0],paramLimits[yrow][1])
		mplQt.canvas.ax.set_zlim(paramLimits[zrow][0],paramLimits[zrow][1])
		mplQt.canvas.ax.set_xlabel(displayedParamList[xrow])
		mplQt.canvas.ax.set_ylabel(displayedParamList[yrow])
		mplQt.canvas.ax.set_zlabel(displayedParamList[zrow])
		mplQt.canvas.fig.canvas.draw()
		plt.draw()                      # redraw the canvas
		
	def axesLimitsButtonClicked(self):
		xrow = mplQt.xAxisList.currentRow()
		yrow = mplQt.yAxisList.currentRow()
		zrow = mplQt.zAxisList.currentRow()
		paramLimits[xrow][0] = int(self.xLimitLowLE.text())
		paramLimits[xrow][1] = int(self.xLimitHighLE.text())
		paramLimits[yrow][0] = int(self.yLimitLowLE.text())
		paramLimits[yrow][1] = int(self.yLimitHighLE.text())
		paramLimits[zrow][0] = int(self.zLimitLowLE.text())
		paramLimits[zrow][1] = int(self.zLimitHighLE.text())
		
		mplQt.canvas.ax.set_xlim(paramLimits[xrow][0],paramLimits[xrow][1])
		mplQt.canvas.ax.set_ylim(paramLimits[yrow][0],paramLimits[yrow][1])
		mplQt.canvas.ax.set_zlim(paramLimits[zrow][0],paramLimits[zrow][1])

		

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mplQt = MPL_WIDGET_3D()
	mplQt.show()
	sys.exit(app.exec_())