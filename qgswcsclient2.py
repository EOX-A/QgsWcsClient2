# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsWcsClient2
                                 A QGIS plugin
 A OGC WCS 2.0/EO-WCS Client
                             -------------------
        begin                : 2014-06-26; 2017-04-10
        copyright            : (C) 2014 by Christian Schiller / EOX IT Services GmbH, Vienna, Austria
        email                : christian dot schiller at eox dot at
 ***************************************************************************/

/*********************************************************************************/
 *  The MIT License (MIT)                                                         *
 *                                                                                *
 *  Copyright (c) 2014 EOX IT Services GmbH                                       *
 *                                                                                *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy  *
 *  of this software and associated documentation files (the "Software"), to deal *
 *  in the Software without restriction, including without limitation the rights  *
 *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     *
 *  copies of the Software, and to permit persons to whom the Software is         *
 *  furnished to do so, subject to the following conditions:                      *
 *                                                                                *
 *  The above copyright notice and this permission notice shall be included in    *
 *  all copies or substantial portions of the Software.                           *
 *                                                                                *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    *
 *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      *
 *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   *
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        *
 *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, *
 *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE *
 *  SOFTWARE.                                                                     *
 *                                                                                *
 *********************************************************************************/
 initialisation, etc.  of the QgsWcsClient2 plugin
"""
from __future__ import absolute_import
    # Import the PyQt and QGIS libraries
from builtins import object
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
    # Initialize Qt resources from file resources.py
    # Import the code for the dialog(s)
from .qgswcsclient2dialog import QgsWcsClient2Dialog
from .qgsnewhttpconnectionbase import Ui_qgsnewhttpconnectionbase
from .EOxWCSClient.wcs_client  import wcsClient
import os.path

    # global setttings and saved server list
global config
from . import config


class QgsWcsClient2(object):

    def __init__(self, iface):
        global config
            # Save reference to the QGIS interface
        self.iface = iface

            # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(config.plugin_dir, 'i18n', 'qgswcsclient2_{}.qm'.format(locale))

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
            u"WCS 2.0/EO-WCS Client", self.iface.mainWindow())
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






