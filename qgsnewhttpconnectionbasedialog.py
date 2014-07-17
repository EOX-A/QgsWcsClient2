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
from qgsnewhttpconnectionbase import Ui_qgsnewhttpconnectionbase

#global setttings and saved server list
global config
import config
srvlst = []

class qgsnewhttpconnectionbase(QDialog,  QObject, Ui_qgsnewhttpconnectionbase):
    MSG_BOX_TITLE = "WCS2.0/EO-WCS Client"
    
    def __init__(self, parent, fl, toEdit, choice):
        QDialog.__init__(self, parent, fl) 
        self.toEdit = toEdit
        self.idx_sel = choice
        self.parent = parent
        self.flags = fl
        self.setupUi(self)
        self.txt_NewSrvName.setFocus(True)
        self.setWindowTitle('WCS2.0/EO-WCS Client') # +version())


    def accept(self):
        global config
        print 'IDX: ',self.idx_sel
        srvlst = config.srv_list['servers']
        srv_name = self.txt_NewSrvName.text()
        srv_url = self.txt_NewSrvUrl.text()
        
            # verify that URL start with http://
        while not srv_url.startswith("http://"):
            info = "Sorry, but the 'Server URL' has to start with http://.\n"
            self.warning_msg(info)
            srv_name = self.txt_NewSrvName.text()

        
        if self.toEdit is False:
            try:
                idx = zip(*config.srv_list['servers'])[0].index(srv_name)
                while idx is not None:
                    self.txt_NewSrvName.setText(srv_name+'_1')
                    self.txt_NewSrvUrl.setText(srv_url)
                    info = "Sorry, but the 'Server Name' has to be unique.\n      A   '_1'   has been added to the name."
                    self.warning_msg(info)
                    srv_name = self.txt_NewSrvName.text()
                    idx = zip(*config.srv_list['servers'])[0].index(srv_name)
                    
                    
            except ValueError:
                srvlst.append([srv_name, srv_url])
                
        if self.toEdit is True:
            try:
                idx = zip(*config.srv_list['servers'])[0].index(srv_name)
            except ValueError:
                idx = self.idx_sel
                srvlst.pop(idx)
                srvlst.insert(idx,[srv_name,srv_url])

        config.srv_list = {'servers': srvlst }
        self.parent.write_srv_list()
        self.parent.updateServerListing()
        self.close()


    def warning_msg(self, msg):
        msgBox = QtGui.QMessageBox()
        #msgBox.setText("Sorry, but the 'Server Name' has to be unique.\n      A   '_1'   has been added to the name.")
        msgBox.setText(msg)
        msgBox.addButton(QtGui.QPushButton('OK'), QtGui.QMessageBox.YesRole)
        msgBox.exec_()


