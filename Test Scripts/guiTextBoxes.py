#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we create a bit
more complicated window layout using
the QGridLayout manager. 

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QPushButton, QMessageBox)

	
class Example(QWidget):
	
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        xLabel = QLabel('X Coordinate')
        yLabel = QLabel('Y Coordinate')
        altLabel = QLabel('Altitude')

        self.xEdit = QLineEdit()
        yEdit = QLineEdit()
        altEdit = QLineEdit()
        self.button = QPushButton("Go")
		

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(xLabel, 1, 0)
        grid.addWidget(self.xEdit, 1, 1)

        grid.addWidget(yLabel, 2, 0)
        grid.addWidget(yEdit, 2, 1)

        grid.addWidget(altLabel, 3, 0)
        grid.addWidget(altEdit, 3, 1)

        grid.addWidget(self.button, 8, 0)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Review')    
        self.show()
        
        self.button.clicked.connect(self.handleButton)

    def handleButton(self):
        xVal = self.xEdit.text()
        QMessageBox.question(self, 'PyQt5 message', "Your x coordinate is " + str(xVal), QMessageBox.Ok, QMessageBox.Ok)
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())