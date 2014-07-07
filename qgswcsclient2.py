# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsWcsClient2
                                 A QGIS plugin
 A OGC WCS 2.0/EO-WCS Client 
                              -------------------
        begin                : 2014-06-26
        copyright            : (C) 2014 by Christian Schiller / EOX IT Services GmbH, Vienna, Austria
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog(s)
from qgswcsclient2dialog import QgsWcsClient2Dialog
from qgsnewhttpconnectionbase import Ui_qgsnewhttpconnectionbase
from EOxWCSClient.wcs_client  import wcsClient
#from EOxWCSClient.cmdline_wcs_client import  _get_cmdline

import os.path

#global setttings and saved server list
global config
import config


class QgsWcsClient2:

    def __init__(self, iface):
        global config
        # Save reference to the QGIS interface
        self.iface = iface

        #print "3434: ", config.srv_list
        #print "4455: ", config.plugin_dir
        
        
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(config.plugin_dir, 'i18n', 'qgswcsclient2_{}.qm'.format(locale))
            #Initialise the environment    
        #userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+"/python/plugins/wps"  
        #systemPluginPath = QgsApplication.prefixPath()+"/share/qgis/python/plugins/wps"




        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = QgsWcsClient2Dialog(iface)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/qgswcsclient2/icon.png"),
            u"WCS 2.0/EO-WCS Clien", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&WcsClient2", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&WcsClient2", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass






