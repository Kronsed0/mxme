# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:30:05 2022

@author: Kronseder Bernhard
"""

#importieren der Systembibliotheken
import sys

#importieren der Einzelprogramme
from Device import *
#from GUI import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myGui = Device("mxme")
    app.exec_() # Start der Event-Loop