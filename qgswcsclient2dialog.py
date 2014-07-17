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
from PyQt4.QtGui import QProgressDialog, QDialog, QMessageBox, QFileDialog
from ui_qgswcsclient2 import Ui_QgsWcsClient2
from qgsnewhttpconnectionbasedialog import qgsnewhttpconnectionbase
from display_txtdialog import display_txt
from EOxWCSClient.wcs_client  import wcsClient
#import EOxWCSClient.wcs_client
#from EOxWCSClient.cmdline_wcs_client import  _get_cmdline
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager
from qgis.core import QgsNetworkAccessManager
from PyQt4 import QtXml
#from PyQt4.QtGui import QApplication,QMessageBox
#from  test_net_3 import NetworkAccessManager
#from  test_net_4 import FileDownloader
from  downloader import download_url 
#import test_net_3
from xml.dom import minidom
from lxml import etree

import os, sys, pickle
#global setttings and saved server list
global config
import config

global namespaces
namespaces={"wcs": "http://www.opengis.net/wcs/2.0", "wcseo": "http://www.opengis.net/wcseo/1.0", "crs":  "http://www.opengis.net/wcs/service-extension/crs/1.0", "gml" : "http://www.opengis.net/gml/3.2", "gmlcov" : "http://www.opengis.net/gmlcov/1.0", "ogc" : "http://www.opengis.net/ogc", "ows" : "http://www.opengis.net/ows/2.0", "swe" : "http://www.opengis.net/swe/2.0" }
 


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)



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
        self.progress_dialog.setAutoClose(True)  # False # was set originally
        title = self.tr("WSC-2.0/EO-WCS Downloader")
        self.progress_dialog.setWindowTitle(title)

        #myWCS = wcs_client.wcsClient()
        self.myWCS = wcsClient()
        
        self.treeWidget_GCa.itemClicked.connect(self.on_GCa_clicked)
        self.treeWidget_DC.itemClicked.connect(self.on_DC_clicked)
        self.treeWidget_DCS.itemClicked.connect(self.on_DCS_clicked)
        self.treeWidget_GCov.itemClicked.connect(self.on_GCov_clicked)


    def clear_req_params(self,req_params):
        print "I'm in "+sys._getframe().f_code.co_name
        for k,v in req_params.items():
            if v is None:
                req_params.pop(k)
        return req_params

## ====== Beginning Server Tab-section ======

    def message(self):
        #self.iface.messageBar().pushMessage("Error", 
        #    "I'm sorry Dave, I'm afraid I can't do that TestDialog",
        #    level=1)
#        print "111:  I am here"
        #input = self.dlg.textEdit.toPlainText()
        #print "222: ", input
        input = self.textEdit.toPlainText()
#        print "222: ", input

        pass

    def newServer(self):
        global config
        print '444-btnNew: I am adding a New ServerName/URL'
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
        dlgNew = qgsnewhttpconnectionbase(self, flags, toEdit=False, choice='')
        dlgNew.show()

##TODO -- sort the srv_list

    def get_serv_url(self):
        global serv
        sel_serv = self.cmbConnections_Serv.currentText()
        idx = serv.index(sel_serv)
        sel_url = config.srv_list['servers'][idx][1]
        return sel_serv, sel_url
 

        # check if the url exist and if we get a respond to a simple OWS request
    def connectServer(self):
        global config
        global serv
        #response = None
        #req_qgsmng = None
        #print 'RR: ',response 
        
       #selected_serv = self.cmbConnections_Serv.currentText()
        #idx = serv.index(selected_serv)
        #selected_url = config.srv_list['servers'][idx][1]
        selected_serv, selected_url = self.get_serv_url()
        print '555-btnTest: I choose: ', selected_serv,   "URL:", selected_url
       # print type(response), type(req_qgsmng)
        #self.doc = None
        #self.messageBuffer = QByteArray()
        
        url_base = selected_url
        url_ext1 = "service=WCS&request=GetCapabilities" #&sections=ServiceMetadata"
        myUrl = url_base + url_ext1
        msg = "Your choice:    "+selected_serv.encode()+"\n"
        msg = msg+"URL:                   "+selected_url.encode()+"\n"

        srv_valid = QUrl(myUrl).isValid()
        if  srv_valid is True:
            msg = msg+"Server address is valid \n"
            msg = msg+"Now testing the connection and response.....\n "
            msg = msg+"       this may take some time (depending on the server)\n"
            self.textBrowser_Serv.setText(msg)
        
        #my_outfile = 1_testServer.xml
        #my_outfile = '1_'+selected_serv+'-xml'
        
        #my_output_path = "/home/schillerc/cs_pylib/wcs_qgis_plugin/QgsWcsClient2/"+my_outfile
       

       # self.progress_dialog.setMaximum(100)
       # self.progress_dialog.setValue(0)
        label_text = self.tr("Downloading....")
        #self.progress_dialog.setLabelText(label_text)
        self.progress_dialog.done(QDialog.Accepted)
        self.progress_dialog.cancel()
        self.progress_dialog.show()        
        
        
        
        
        #req_qgsmng = QgsNetworkAccessManager.instance()
        #del req_qgsmng
        req_qgsmng = QNetworkAccessManager(self)
       # network_AccessManager = FileDownloader(req_qgsmng, myUrl, my_output_path, self.progress_dialog) #
        #print type(req_qgsmng)
        #network_AccessManager = FileDownloader(req_qgsmng, myUrl, my_output_path, progress_dialog=None)
        
            # used with download_url 
        #response = download_url(req_qgsmng, myUrl, my_output_path, self.progress_dialog)
        #response = download_url(req_qgsmng, myUrl, my_output_path, progress_dialog=None)
        #response = download_url(req_qgsmng, myUrl, None, progress_dialog=None)
        #if response is not None:
            #response[2] =[]
            #del response
        response = download_url(req_qgsmng, myUrl, None, self.progress_dialog)
        print type(response), len(response[2])
        #print response
        print '--------'
        
        #networkAccessManager = NetworkAccessManager(myUrl)
        #url = QUrl(myUrl)
        #networkAccessManager = NetworkAccessManager(url)

        #response = network_AccessManager.download()


        if response[0] is True and ((response[2] is not None or len(response[2]) == 0)) :
            msg = msg+"Response:    Server OK\n"
            self.parse_first_xml(response[2])
            self.treeWidget_GCa.clear()
            self.treeWidget_DC.clear()
            self.treeWidget_DCS.clear()
            self.treeWidget_GCov.clear()

            self.progress_dialog.close()

                # all tabs (except Server/Help/About) are disable until server connection is OK
                # once server connection is verifyed, activate all other tabs
            if not self.tab_GCa.isEnabled():
                self.tab_GCa.setEnabled(True)
            if not self.tab_DC.isEnabled():
                self.tab_DC.setEnabled(True)
            if not self.tab_DCS.isEnabled():
                self.tab_DCS.setEnabled(True)
            if not self.tab_GCov.isEnabled():
                self.tab_GCov.setEnabled(True)

            if not self.checkBox_GCa_ActiveDate.isEnabled():
                self.checkBox_GCa_ActiveDate.setEnabled(True)

            if not self.checkBox_DCS_ActiveDate.isEnabled():
                 self.checkBox_DCS_ActiveDate.setEnabled(True)
            if not self.checkBox_DCS_ActiveCount.isEnabled():
                self.checkBox_DCS_ActiveCount.setEnabled(True)
            if self.dateTimeEdit_DCSBegin.isEnabled():
                self.dateTimeEdit_DCSBegin.setEnabled(False)
            if self.dateTimeEdit_DCSEnd.isEnabled():
                self.dateTimeEdit_DCSEnd.setEnabled(False)
            if not self.spinBox_DCSCount.isEnabled():
                self.spinBox_DCSCount.setEnabled(True)


            if self.radioButton_GCovSubCRS.isChecked():
                self.radioButton_GCovSubCRS.setChecked(False)
            if self.radioButton_GCovSubPixel.isChecked():
                self.radioButton_GCovSubPixel.setChecked(False)
            if not self.radioButton_GCovSubOrig.isChecked():
                self.radioButton_GCovSubOrig.setChecked(True)

            if self.radioButton_GCovXSize.isChecked():
                self.radioButton_GCovXSize.setChecked(False)
            if self.radioButton_GCovXRes.isChecked():
                self.radioButton_GCovXRes.setChecked(False)
            if self.radioButton_GCovYSize.isChecked():
                self.radioButton_GCovYSize.setChecked(False)
            if self.radioButton_GCovYRes.isChecked():
                self.radioButton_GCovYRes.setChecked(False)





        else:
            msg = msg+"Response:    An Error occurred: --> "+response[1]+"\n"
            self.progress_dialog.close()
        
        
        self.textBrowser_Serv.setText(msg)
#        print "RESPONSE: ", response
        


    def parse_first_xml(self, in_xml):
        join_xml = ''.join(e.encode() for e in in_xml)
#        print "LLL: ", len(join_xml), len(in_xml)
#        print type(in_xml)
#        print in_xml

        _xml_ID_tag = ["wcs:formatSupported", "crs:crsSupported"]
        _result_tag = ["outformat", "outcrs"]

## TODO - change to use etree/xpath
#        oformats = tree.xpath("wcs:ServiceMetadata/wcs:formatSupported/text()", namespaces=namespaces)
#        ocrs = tree.xpath("wcs:ServiceMetadata/wcs:Extension/crs:crsSupported/text()", namespaces=namespaces)
#        support_outcrs=[]
#        for eleme in ocrs:
#            support_outcrs.append(os.path.basename(elem))
#

        def extractTags(join_xml, tag):
#        def extractTags(tag):
#            print join_xml, tag
            xmldoc = minidom.parseString(join_xml)
#            print type(xmldoc), xmldoc
            tagid_node = xmldoc.getElementsByTagName(tag)
            n_elem = tagid_node.length
            tag_ids = []
                # store the found items
            for n  in range(0, n_elem):
                tag_ids.append(tagid_node[n].childNodes.item(0).data)

            return tag_ids, n_elem

        outformat, oformat_num = extractTags(join_xml, _xml_ID_tag[0])
        outcrs, ocrs_num = extractTags(join_xml, _xml_ID_tag[1])
        support_outcrs=[]
        for elem in outcrs:
            support_outcrs.append(os.path.basename(elem))

#        print "OO1: ", oformat_num, outformat
#        print "OO2: ", ocrs_num, support_outcrs
        
        for elem in range (0, oformat_num):
            self.comboBox_GCOvOutFormat.addItem(_fromUtf8(""))
            self.comboBox_GCOvOutFormat.setItemText(elem, _translate("QgsWcsClient2", outformat[elem], None))
                                                             
        for elem in range (0, ocrs_num):
            self.comboBox_GCovOutCRS.addItem(_fromUtf8(""))
            self.comboBox_GCovOutCRS.setItemText(elem, _translate("QgsWcsClient2", support_outcrs[elem], None))



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


    def get_outputLoc(self):
        global req_outputLoc
        start_dir = os.getenv("HOME")
        req_outputLoc = QFileDialog.getExistingDirectory(self, "Select Output Path", start_dir)
        if len(req_outputLoc) > 0:
            if not req_outputLoc.endswith(os.sep):
                req_outputLoc = req_outputLoc+os.sep
            self.lineEdit_Serv_OutputLoc.setText(str(req_outputLoc))
        return req_outputLoc

## ====== End of Server section ======
## ====== Beginning GetCapabilities section ======
    def exeGetCapabilities(self):
        print "I'm in "+sys._getframe().f_code.co_name
        global cov_ids
        global dss_ids
        global req_outputLoc
        
        self.treeWidget_GCa.clear()
        req_sections=[]
        req_updateDate=''
        selected_serv, selected_url = self.get_serv_url()
        
        if self.checkBox_GCaAll.isChecked():
            req_sections.append("All")
        if self.checkBox_GCaDaSerSum.isChecked():
            req_sections.append("DatasetSeriesSummary")
        if self.checkBox_GCaCovSum.isChecked():
            req_sections.append("CoverageSummary")
        if self.checkBox_GCaServId.isChecked():
            req_sections.append("ServiceIdentification")
        if self.checkBox_GCaServProv.isChecked():
            req_sections.append("ServiceProvider")
        if self.checkBox_GCaServMeta.isChecked():
            req_sections.append("ServiceMetadata")
        if self.checkBox_GCaOpMeta.isChecked():
            req_sections.append("OperationsMetadata")
        if self.checkBox_GCaCont.isChecked():
            req_sections.append("Content")
        if self.checkBox_GCaLang.isChecked():
            req_sections.append("Languages")
            
        req_outputLoc = self.lineEdit_Serv_OutputLoc.text()

        if self.dateEdit_GCaDocUpdate.isEnabled():
            req_updateDate = self.dateEdit_GCaDocUpdate.text()
        else:
            req_updateDate = None

#        print "Sections:", req_sections, type(req_sections)
        req_sections =','.join(req_sections)
        if len(req_sections) == 0:  
            req_sections = None
            
        req_params = {'request': 'GetCapabilities',
            'server_url': selected_url ,
            'updateSequence': req_updateDate,
            'sections' : req_sections }
        #else:
            #req_params = {'request': 'GetCapabilities',
                #'server_url': selected_url ,
                #'updateSequence': req_updateDate }

        req_params = self.clear_req_params(req_params)
        print 'P1: ',req_params

        GCa_result = self.myWCS.GetCapabilities(req_params)
        #print GCA_result

        cov_ids, dss_ids, dss_begin, dss_end = self.parse_GCa_xml(GCa_result)  # ,req_sections)  # do I need that for parsing?
        #print "Hey: ", cov_ids, dss_ids, dss_begin, dss_end
#        print len(dss_ids), len(dss_begin), len(dss_end), len(cov_ids)
        
        if len(dss_ids) > 0:
            for a,b,c in zip(dss_ids, dss_begin, dss_end):
                inlist =(a,b,c)
                item = QtGui.QTreeWidgetItem(self.treeWidget_GCa, inlist)
        
        if len(cov_ids) > 0:
            for elem in cov_ids:
                inlist = (elem, "","")
                item = QtGui.QTreeWidgetItem(self.treeWidget_GCa, inlist)

        self.treeWidget_GCa.resizeColumnToContents(0)

        #self.treeWidget_GCa.itemClicked.connect(self.on_GCa_clicked)


    def on_GCa_clicked(self):
        #aa = self.treeWidget_GCa.selectedIndexes()
        #bb = self.treeWidget_GCa.selectedItems()
        #print dir(aa), dir(bb)
        global cov_ids
        global dss_ids
        #print "DSS :", dss_ids

        sel_GCa_items = self.treeWidget_GCa.selectedItems()
        self.treeWidget_DC.clear()
        self.treeWidget_DCS.clear()
        self.treeWidget_GCov.clear()
        
        for elem in sel_GCa_items:
#            print elem.data(0,0)
#            print "CO: ", elem.data(0,0) in cov_ids
#            print "DS: ", elem.data(0,0) in dss_ids
            if elem.data(0,0) in cov_ids:
                item = QtGui.QTreeWidgetItem(self.treeWidget_DC, (elem.data(0,0),))
                item1 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, (elem.data(0,0),))
                item2 = QtGui.QTreeWidgetItem(self.treeWidget_GCov, (elem.data(0,0),))
            elif elem.data(0,0) in dss_ids:
                item1 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, (elem.data(0,0),))
                #item2 = QtGui.QTreeWidgetItem(self.treeWidget_GCov, (elem.data(0,0),))

        self.treeWidget_DC.resizeColumnToContents(0)
        self.treeWidget_DCS.resizeColumnToContents(0)
        self.treeWidget_GCov.resizeColumnToContents(0)



    def updateDateChanged(self):
        if self.dateEdit_GCaDocUpdate.isEnabled():
            self.dateEdit_GCaDocUpdate.setEnabled(False)
        else:
            self.dateEdit_GCaDocUpdate.setEnabled(True)



    def parse_GCa_xml(self, GCa_result): # ,req_sections):  # do I need that for parsing?
        print "I'm in "+sys._getframe().f_code.co_name
#        type(GCa_result)
#        p_result = 'OK'

        tree = etree.fromstring(GCa_result)
        coverage_ids = tree.xpath("wcs:Contents/wcs:CoverageSummary/wcs:CoverageId/text()", namespaces=namespaces)
        datasetseries_ids = tree.xpath("wcs:Contents/wcs:Extension/wcseo:DatasetSeriesSummary/wcseo:DatasetSeriesId/text()",                                    namespaces=namespaces)
        datasetseries_timeBegin =  tree.xpath("wcs:Contents/wcs:Extension/wcseo:DatasetSeriesSummary/gml:TimePeriod/gml:beginPosition/text()", namespaces=namespaces)

        datasetseries_timeEnd = tree.xpath("wcs:Contents/wcs:Extension/wcseo:DatasetSeriesSummary/gml:TimePeriod/gml:endPosition/text()", namespaces=namespaces)

#        print datasetseries_ids, coverage_ids
        return coverage_ids, datasetseries_ids, datasetseries_timeBegin, datasetseries_timeEnd


## ====== End of GetCapabilities section ======
## ====== Beginning DescribeCoverage section ======
    def exeDescribeCoverage(self):
        print "I'm in "+sys._getframe().f_code.co_name
        global selected_covid
        selected_serv, selected_url = self.get_serv_url()
#        self.treeWidget_DC.itemClicked.connect(self.on_DC_clicked)
         
        print "DC CovID: ", selected_covid
        
        req_params = {'request': 'DescribeCoverage',
                'server_url':  selected_url, 
                'coverageID':  selected_covid }
#        print req_params
        DC_result = self.myWCS.DescribeCoverage(req_params)
#        print DC_result

            # open a new window to display the returned DescribeCoverage-Response XMl 
        myDisplay_txt =  display_txt(self)
        myDisplay_txt.textBrowser_Disp.setText(DC_result)
        myDisplay_txt.show()
       
        
    def on_DC_clicked(self):
        global selected_covid
        sel_DC_items = self.treeWidget_DC.selectedItems()
        selected_covid = sel_DC_items[0].data(0,0).encode()
#        print "SELECTED: ", selected_covid   #sel_DC_items[0].data(0,0)
        return 



## ====== End of DescribeCoverage section ======
## ====== Beginning DescribeEOCoverageSet section ======
    def exeDescribeEOCoverageSet(self):
        print "I'm in "+sys._getframe().f_code.co_name
        global selected_eoid
        global offered_crs
        
#        selected_eoid = []
        req_sections = []
       
        selected_serv, selected_url = self.get_serv_url()
                
        if self.checkBox_DCSAll.isChecked():
            req_sections.append("All")
        if self.checkBox_DCSDatSerSum.isChecked():
            req_sections.append("DatasetSeriesSummary")
        if self.checkBox_DCSCovSum.isChecked():
            req_sections.append("CoverageSummary")

        req_sections = ','.join(req_sections)
        if len(req_sections) == 0:  
            req_sections = None


        if self.radioButton_ContCont.isChecked():
            req_contain = "contains"        
        if self.radioButton_ContOver.isChecked():
            req_contain = "overlaps"

        if self.checkBox_DCS_ActiveCount.isChecked():
            req_count = self.spinBox_DCSCount.text().encode()
        else:
            req_count = None


        if self.checkBox_DCSIDonly.isChecked():
            req_IDs_only = True
        else: 
            req_IDs_only = False

        min_x = self.lineEdit_DCSMinLon.text()
        max_x = self.lineEdit_DCSMaxLon.text()
        min_y = self.lineEdit_DCSMinLat.text()
        max_y = self.lineEdit_DCSMaxLat.text()        
        if ( len(min_x) == 0 or len(max_x) == 0 ): 
            req_lon = None
        else:
            req_lon = str(min_x+","+max_x)
        if ( len(min_y) == 0 or len(max_y) == 0 ): 
            req_lat = None
        else:
            req_lat = str(min_y+","+max_y)
        
        if self.checkBox_DCS_ActiveDate.isChecked():
            beginTime= self.dateTimeEdit_DCSBegin.text()
            endTime= self.dateTimeEdit_DCSEnd.text()
#            print "TIME:" ,dir(beginTime), type(beginTime), beginTime ,endTime
            req_toi = str(beginTime.strip()+","+endTime.strip())
#            print "TIME:", req_toi
        else:
            req_toi = None
            
        selected_eoid = ','.join(selected_eoid)
        #print "DCS EOID: ", selected_eoid

        req_params = {'request': 'DescribeEOCoverageSet' ,
            'server_url': selected_url ,
            'eoID':  selected_eoid ,
            'subset_lon': req_lon , 
            'subset_lat': req_lat , 
            'subset_time': req_toi , 
            'containment' : req_contain ,
            'count' : req_count , 
            'section' : req_sections ,
            'IDs_only': req_IDs_only }

        req_params = self.clear_req_params(req_params)
        print "PPP: ",req_params

        if req_params.has_key('IDs_only') and req_params['IDs_only'] == True:
            DCS_result, axis_labels, offered_crs = self.myWCS.DescribeEOCoverageSet(req_params)
            #print "AXIS", axis_labels, type(axis_labels)
            self.lineEdit_GCovXAxisLabel.setText(axis_labels[0])
            self.lineEdit_GCovYAxisLabel.setText(axis_labels[1])
            combo_idx = self.comboBox_GCovOutCRS.findText(offered_crs)
            self.comboBox_GCovOutCRS.setCurrentIndex(combo_idx)
            
           
          
            
            #offered_crs = comboBox_GCovSubset      # not in use, preparation to change radioButtons of 'Type of Subsetting'
        else:
            DCS_result = self.myWCS.DescribeEOCoverageSet(req_params)
#        print "DCS_result", DCS_result
        #print len(DCS_result)


##TODO add Button to also allow to view the full XML-Response file (=> Getcapabilities, DescribeEOCoverageSet)        
        #myDisplay_txt =  display_txt(self)
        #myDisplay_txt.textBrowser_Disp.setText(DCS_result)
        #myDisplay_txt.show()


## TODO !!!!! -- read out the axis labes from the DescribeEOCoverageSet or the DescribeCoverage and 
#        set the the AXIS-Fields in the GetCapabilities Tab accordingly (even if they are inactive)


        if req_params['IDs_only'] == True:
            #self.treeWidget_DCS.clear()
            self.treeWidget_GCov.clear()
            #item1 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, DCS_result)
            #item2 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, "")
            #item3 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, "")
            for elem in DCS_result:
                #print "TTT: ", type(DCS_result), type(elem), len(elem), elem, elem.encode()
                item = QtGui.QTreeWidgetItem(self.treeWidget_GCov, [elem])
                #item = QtGui.QTreeWidgetItem(self.treeWidget_DCS, [elem])
                #item1 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, "")
                #item2 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, "")
                
                # once results are available - put 'Focus' on --> tab_GCov
            self.tabWidget_EOWcsClient2.setCurrentIndex(4)
            self.treeWidget_GCov.resizeColumnToContents(0)    
            
        else:
            #self.treeWidget_DCS.clear()
            #self.treeWidget_GCov.clear()
                # run resutls throught the xml parser

                # just display full result with a text-viewer
            myDisplay_txt =  display_txt(self)
            myDisplay_txt.textBrowser_Disp.setText(DCS_result)
            myDisplay_txt.show()


        self.treeWidget_DCS.resizeColumnToContents(0)

    def enableDCS_ActiveDate(self):
        if self.dateTimeEdit_DCSBegin.isEnabled():
            self.dateTimeEdit_DCSBegin.setEnabled(False)
            self.dateTimeEdit_DCSEnd.setEnabled(False)
        else:
            self.dateTimeEdit_DCSBegin.setEnabled(True)
            self.dateTimeEdit_DCSEnd.setEnabled(True)


    def enableDCS_ActiveCount(self):
        if self.spinBox_DCSCount.isEnabled():
            self.spinBox_DCSCount.setEnabled(False)
        else:
            self.spinBox_DCSCount.setEnabled(True)


    def on_DCS_clicked(self):
        global selected_eoid
        selected_eoid = []
        sel_DCS_items = self.treeWidget_DCS.selectedItems()
        for elem in sel_DCS_items:
            selected_eoid.append(elem.data(0,0).encode())
            print "SELECTED: ", selected_eoid, type(selected_eoid)   #sel_DC_items[0].data(0,0)
            item2 = QtGui.QTreeWidgetItem(self.treeWidget_GCov, elem)
        
        #for elem in selected_eoid:
##            print elem.data(0,0)
##            print "CO: ", elem.data(0,0) in cov_ids
##            print "DS: ", elem.data(0,0) in dss_ids
            #if elem in cov_ids:
                #item = QtGui.QTreeWidgetItem(self.treeWidget_DC, elem)
                ##item1 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, elem)
                #item2 = QtGui.QTreeWidgetItem(self.treeWidget_GCov, elem)
            #elif elem in dss_ids:
                #item1 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, elem)
                #item2 = QtGui.QTreeWidgetItem(self.treeWidget_GCov, elem)

        
        
        return 



## ====== End of DescribeEOCoverageSet section ======
## ====== Beginning GetCoverage section ======
    def exeGetCoverage(self):
        print "I'm in "+sys._getframe().f_code.co_name
        global selected_gcovid
        global req_outputLoc
        global offered_crs
        
        selected_serv, selected_url = self.get_serv_url()

        print 'GCov covID: ', selected_gcovid

        req_format = self.comboBox_GCOvOutFormat.currentText()
        req_interpolation = self.comboBox_GCovInterpol.currentText()
        req_outputcrs = self.comboBox_GCovOutCRS.currentText()

        if req_interpolation.encode().startswith("nearest"):
            req_interpolation = None

        req_rangesubset = self.lineEdit_GCovBands.text()
        if len(req_rangesubset) == 0:
            req_rangesubset = None

        req_x_label = self.lineEdit_GCovXAxisLabel.text().strip()
        req_y_label = self.lineEdit_GCovYAxisLabel.text().strip()
 
        if self.radioButton_GCovXSize.isChecked():
            req_xsize = self.lineEdit_GCovXSize.text()
            req_size_x = "size "+str(req_x_label)+" "+str(req_xsize)
            
        if self.radioButton_GCovXRes.isChecked():
            req_xsize = self.lineEdit_GCovXSize.text()
            req_size_x = "resolution "+str(req_x_label)+" "+str(req_xsize)

        if self.radioButton_GCovYSize.isChecked():
            req_ysize = self.lineEdit_GCovYSize.text()
            req_size_y = "size "+str(req_y_label)+" "+str(req_ysize)
            
        if self.radioButton_GCovYRes.isChecked():
            req_ysize = self.lineEdit_GCovYSize.text()
            req_size_y = "resolution "+str(req_y_label)+" "+str(req_ysize)

        if self.radioButton_GCov_OutSizeOrig.isChecked():
            req_size_x = None
            req_size_y = None



        if self.radioButton_GCovSubOrig.isChecked():
            #req_subsetCRS = offered_crs
            req_subsetCRS = "epsg:"+offered_crs
        if self.radioButton_GCovSubCRS.isChecked():
            epsg_no = self.lineEdit_GCovSubEPSG.text()
            req_subsetCRS = "epsg:"+str(epsg_no).strip()
        if self.radioButton_GCovSubPixel.isChecked():
            req_subsetCRS = "pix"

        min_x = self.lineEdit_GCovMinLon.text()
        max_x = self.lineEdit_GCovMaxLon.text()
        min_y = self.lineEdit_GCovMinLat.text()
        max_y = self.lineEdit_GCovMaxLat.text()        

        if ( len(min_x) == 0 or len(max_x) == 0 ): 
            req_lon = None
        else:
            #if req_outputcrs == offered_crs:
                #req_lon = req_x_label+" "+str(min_x+","+max_x)
                #req_lon = str(min_x+","+max_x)
            #else:
                req_lon = req_subsetCRS+" "+req_x_label+" "+str(min_x+","+max_x)

        if ( len(min_y) == 0 or len(max_y) == 0 ): 
            req_lat = None
        else:
            #if req_outputcrs == offered_crs:
                #req_lat = req_y_label+" "+str(min_y+","+max_y)
                #req_lat = str(min_y+","+max_y)
            #else:   
                req_lat = req_subsetCRS+" "+req_y_label+" "+str(min_y+","+max_y)



        if req_outputcrs == offered_crs:
            req_outputcrs = None


        if not "req_outputLoc" in globals(): 
            msg = "Error: For downloading coverages you need to supply a Local Storage Path --> see TAB Server / Storage"
            QMessageBox.critical(self, "Error",  msg, QMessageBox.Ok )
            req_outputLoc = self.get_outputLoc()
        else:
            req_outputLoc = self.lineEdit_Serv_OutputLoc.text()
 
 #req_params = {'request': '&request=',
            #'server_url': '',
            #'coverageID': '&coverageid=',
            #'format': '&format=image/',
            #'subset_x': '&subset=',
            #'subset_y': '&subset=',
            #'rangesubset': '&rangesubset=',
            #'outputcrs': '&outputcrs='+crs_url,
            #'interpolation': '&interpolation=',
            #'mediatype': '&mediatype=',
            #'mask': '&mask=polygon,'+crs_url,
            #'size_x': '&',
            #'size_y': '&',
            #'output': None}


        
        for gcov_elem in selected_gcovid:
      
            req_params = {'request': 'GetCoverage',
                'server_url': selected_url ,
                'coverageID': gcov_elem ,
                'format':  req_format , 
                'subset_x': req_lat ,
                'subset_y': req_lon ,
                'rangesubset': req_rangesubset ,
                'outputcrs': req_outputcrs ,
                'interpolation': req_interpolation ,
                'size_x': req_size_x ,
                'size_y': req_size_y ,
                'output': req_outputLoc}
## TODO -- mediatype & mask --> not yet implemented
               # 'mask': '&mask=polygon,'+crs_url, 
               # 'mediatype': '&mediatype=',  # multipart/mixed' (default = parameter not provided)


#            print 'R1: ',req_params
            
            req_params = self.clear_req_params(req_params)
            
            print 'R2: ',req_params
            GCov_result = self.myWCS.GetCoverage(req_params)
        

## TODO -- Register the downloaded datsets with QGis MapCanvas -> load and show


    def on_GCov_clicked(self):
        global selected_gcovid
        selected_gcovid = []
        sel_GCov_items = self.treeWidget_GCov.selectedItems()
        for elem in sel_GCov_items:
            selected_gcovid.append(elem.data(0,0).encode())
            print "SELECTED: ", selected_gcovid   #sel_DC_items[0].data(0,0)
            item = QtGui.QTreeWidgetItem(self.treeWidget_DC, (elem.data(0,0).encode(),))
        return 

 

    def enableGCov_SubCRS(self):
        if self.radioButton_GCovSubCRS.isChecked():
            self.radioButton_GCovSubOrig.setChecked(False)
            self.radioButton_GCovSubPixel.setChecked(False)
            self.lineEdit_GCovSubEPSG.setEnabled(True)

    def enableGCov_SubPixel(self):
       if self.radioButton_GCovSubPixel.isChecked():
            self.radioButton_GCovSubCRS.setChecked(False)
            self.radioButton_GCovSubOrig.setChecked(False)
            self.lineEdit_GCovSubEPSG.setEnabled(False)
            
    def enableGCov_SubOrig(self):
       if self.radioButton_GCovSubOrig.isChecked():
            self.radioButton_GCovSubCRS.setChecked(False)
            self.radioButton_GCovSubPixel.setChecked(False)
            self.lineEdit_GCovSubEPSG.setEnabled(False)



    def enableGCov_XSize(self):
        if self.radioButton_GCovXSize.isChecked():
            self.radioButton_GCov_OutSizeOrig.setChecked(False)
            self.lineEdit_GCovXAxisLabel.setEnabled(True)
            self.lineEdit_GCovXSize.setEnabled(True)
            self.radioButton_GCovXRes.setChecked(False)

    def enableGCov_XResolution(self):
        if self.radioButton_GCovXRes.isChecked():
            self.radioButton_GCov_OutSizeOrig.setChecked(False)
            self.radioButton_GCovXSize.setChecked(False)
            self.lineEdit_GCovXAxisLabel.setEnabled(True)
            self.lineEdit_GCovXSize.setEnabled(True)

            
    def enableGCov_YSize(self):
        if self.radioButton_GCovYSize.isChecked():
            self.radioButton_GCov_OutSizeOrig.setChecked(False)
            self.lineEdit_GCovYAxisLabel.setEnabled(True)
            self.lineEdit_GCovYSize.setEnabled(True)
            self.radioButton_GCovYRes.setChecked(False)

    def enableGCov_YResolution(self):
        if self.radioButton_GCovYRes.isChecked():
            self.radioButton_GCov_OutSizeOrig.setChecked(False)
            self.radioButton_GCovYSize.setChecked(False)
            self.lineEdit_GCovYAxisLabel.setEnabled(True)
            self.lineEdit_GCovYSize.setEnabled(True)
            
    def disableGCov_OutSize(self):
        if self.radioButton_GCov_OutSizeOrig.isChecked():
            self.lineEdit_GCovXAxisLabel.setEnabled(False)
            self.lineEdit_GCovXSize.setEnabled(False)
            self.radioButton_GCovXSize.setChecked(False)
            self.radioButton_GCovXRes.setChecked(False)
            self.lineEdit_GCovYAxisLabel.setEnabled(False)
            self.lineEdit_GCovYSize.setEnabled(False)
            self.radioButton_GCovYSize.setChecked(False)
            self.radioButton_GCovYRes.setChecked(False)
 




## ====== End of GetCoverage section ======
