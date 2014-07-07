# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsWcsClient2Dialog
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

#from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QProgressDialog, QDialog
from ui_qgswcsclient2 import Ui_QgsWcsClient2
from qgsnewhttpconnectionbasedialog import qgsnewhttpconnectionbase
from EOxWCSClient.wcs_client  import wcsClient
#from EOxWCSClient.cmdline_wcs_client import  _get_cmdline
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager
from qgis.core import QgsNetworkAccessManager
from PyQt4 import QtXml
#from PyQt4.QtGui import QApplication,QMessageBox
from  test_net_3 import NetworkAccessManager
from  test_net_4 import FileDownloader
#import test_net_3


import os, pickle
#global setttings and saved server list
global config
import config

class QgsWcsClient2Dialog(QtGui.QDialog, Ui_QgsWcsClient2):
    
    #capabilitiesRequestFinished = pyqtSignal()
    
    def __init__(self, iface):
        global config
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        
        #self.ui_newserver = qgsnewhttpconnectionbase()
        self.setupUi(self)
        self.iface=iface

            # if server information is already available, activate the Edit-Button, and the update the 
            # selectionBar
        if len(config.srv_list['servers']) > 0:
            self.btnEdit_Serv.setEnabled(True)
            self.btnDelete_Serv.setEnabled(True)
            self.updateServerListing()  
            
                # creating progress dialog for download
        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setAutoClose(False)
        title = self.tr("WSC-2.0/EO-WCS Downloader")
        self.progress_dialog.setWindowTitle(title)


    def message(self):
        #self.iface.messageBar().pushMessage("Error", 
        #    "I'm sorry Dave, I'm afraid I can't do that TestDialog",
        #    level=1)
        print "111:  I am here"
        #input = self.dlg.textEdit.toPlainText()
        #print "222: ", input
        input = self.textEdit.toPlainText()
        print "222: ", input

        pass

    def newServer(self):
        global config
        print '444-btnNew: I am adding a New ServerName/URL'
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
        dlgNew = qgsnewhttpconnectionbase(self, flags, toEdit=False, choice='')
        dlgNew.show()

##TODO -- sort the srv_list

        # check if the url exist and if we get a respond to a simple OWS request
    def testServer(self):
        global config
        global serv
        #self.updateServerListing()
        #self.cmb_connections_Serv.settext(config.srv_list)
        selected_Serv = self.cmbConnections_Serv.currentText()
        print '555-btnTest: I choose: ', selected_Serv
        idx = serv.index(selected_Serv)
        select_url = config.srv_list['servers'][idx][1]
        print "URL:", select_url
        
        #self.doc = None
        #self.messageBuffer = QByteArray()
        
        url_base = select_url
        url_ext1 = "service=wcs&request=GetCapabilities&sections=ServiceMetadata"
        myUrl = url_base + url_ext1

        my_output_path = "/home/schillerc/cs_pylib/wcs_qgis_plugin/QgsWcsClient2/1_testServer.xml"
        

        self.progress_dialog.setMaximum(100)
        self.progress_dialog.setValue(0)
        label_text = self.tr("Downloading....")
        #self.progress_dialog.setLabelText(label_text)
        self.progress_dialog.done(QDialog.Accepted)
        self.progress_dialog.cancel()
        self.progress_dialog.show()        
        
        
        
        
        #req_qgsmng = QgsNetworkAccessManager.instance()
        req_qgsmng = QNetworkAccessManager(self)
       # network_AccessManager = FileDownloader(req_qgsmng, myUrl, my_output_path, self.progress_dialog) #
        network_AccessManager = FileDownloader(req_qgsmng, myUrl, my_output_path, progress_dialog=None)
        
        #networkAccessManager = NetworkAccessManager(myUrl)
        
        #url = QUrl(myUrl)
        #networkAccessManager = NetworkAccessManager(url)

        response = network_AccessManager.download()
        print "RESPONSE: ", response
#        print "NAM: ", network_AccessManager
        
        ##url.setUrl(myRequest)

        #toRequest = QNetworkRequest(url)
        #req_qgsmng = QgsNetworkAccessManager.instance()

        #srv_valid = url.isValid()
        #if srv_valid is True:

            #self.req_reply = req_qgsmng.get(toRequest)
            #print 'OOOOO: ', self.req_reply.readAll().data()
            ##help(req_qgsmng.get(QNetworkRequest(url)))
            #self.req_reply.finished.connect(self._capabilitiesRequestFinished)

        #else:
            #info = "Sorry, the provided 'Server URL' is not valid."
            #qgsnewhttpconnectionbase.warning_msg(info)

        #QObject.connect(self.req_reply,SIGNAL("readyRead()"),self,SLOT("slotReadData()"))
        #QObject.connect(self.req_reply,SIGNAL("finished()"), self,SLOT("slotFinished()"))  


    
    #@pyqtSlot()
    #def _capabilitiesRequestFinished(self):
        ## Receive the server capabilities XML
        #if self.req_reply.error() == 1:
            #QMessageBox.information(None, '', QApplication.translate("QgsWpsGui","Connection Refused. Please check your Proxy-Settings"))
            #pass

        #xmlString = self.req_reply.readAll().data()
        #self.doc = QtXml.QDomDocument()
        #self.doc.setContent(xmlString,  True)

        #root = self.doc.documentElement()  
        #version = root.attribute("version")
        #if version != "1.0.0":
            #QtGui.QMessageBox.information(None, QtGui.QApplication.translate("QgsWps","Only WPS Version 1.0.0 is supported"), xmlString)
            #pass
        
        #print xmlString
        #fo = open("/home/schillerc/cs_pylib/wcs_qgis_plugin/QgsWcsClient2/1_xml_response.xml","wb")
        #fo.write(xmlString)
        #fo.close()

        #self._capabilitiesRequestFinished.emit()


        ##Append current data to the buffer every time readyRead() signal is emitted
    #@pyqtSlot()
    #def slotReadData(self):
        #self.messageBuffer += self.req_reply.readAll().data()

        

    def editServer(self):
        global config
        print "444-btnEdit:  here we are editing... "
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint
        idx = self.cmbConnections_Serv.currentIndex()
        select_serv = config.srv_list['servers'][idx]

        print "Selection: ", idx, " -- ", select_serv, " -- Check: ", serv[idx]

        dlgEdit = qgsnewhttpconnectionbase(self, flags, toEdit=True, choice=idx )  
        dlgEdit.txt_NewSrvName.setText(select_serv[0])
        dlgEdit.txt_NewSrvUrl.setText(select_serv[1])
        dlgEdit.show()

        #self.updateServerListing()

        

    def deleteServer(self):
        global config
        print "444-btnDelete:  here we are deleting...."
        idx = self.cmbConnections_Serv.currentIndex()
        #select_serv = config.srv_list['servers'][idx]
        config.srv_list['servers'].pop(idx)
        
        self.write_srv_list()        
        self.updateServerListing()




        # update the server-listing shown in the selectionBar
    def updateServerListing(self):
        global serv
        global config
        serv = []
        config.srv_list = config.read_srv_list()
        for ii in range(len(config.srv_list['servers'])):
           # print "Config Server: ", config.srv_list['servers'][ii][0][:]
            serv.append(config.srv_list['servers'][ii][0][:])
            
        self.cmbConnections_Serv.clear()
        self.cmbConnections_Serv.addItems(serv)
        #self.cmbConnections_Serv.settext(config.srv_list['servers'])

#def updateServerListing():
    #global serv
    #serv = []
    #for ii in range(len(config.srv_list['servers'])):
        #print config.srv_list['servers'][ii][0][:]
        #serv.append(config.srv_list['servers'][ii][0][:])
        
    #cmbConnections_Serv.addItems(serv)


       # write the sever names/urls to a file
    def write_srv_list(self):
        #plugloc = os.path.realpath(os.path.curdir)
        plugin_dir = os.path.dirname(os.path.realpath(__file__))
        outsrvlst = os.path.join(plugin_dir,'config_srvlist.pkl')
        fo = open(outsrvlst, 'wb')
        p = pickle.dump(config.srv_list, fo, 0)
        fo.close()
