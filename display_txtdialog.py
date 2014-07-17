# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgsnewhttpconnectionbase
                              WCS 2.0 / EO-WCS  QGIS plugin
 
                             -------------------
        begin                : 2014-06-27
        copyright            : (C) 2014 by Christian Schiller
        email                : christian.schiller@eox.at
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os, pickle
#from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from ui_qgswcsclient2 import Ui_QgsWcsClient2
# create the dialog for zoom to point
from  display_txt import Ui_Dialog_Disp

#global setttings and saved server list
global config
import config



class display_txt(QDialog,  QObject, Ui_Dialog_Disp):
   
    def __init__(self, parent):
        QDialog.__init__(self, parent) 
        self.setupUi(self)
        self.setWindowTitle('DescribeCoverage Response')