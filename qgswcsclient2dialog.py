# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgsWcsClient2
                                 A QGIS plugin
 A OGC WCS 2.0/EO-WCS Client 
                             -------------------
        begin                : 2014-06-26
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
 The main QgsWcsClient2 Plugin Application -- an OGC WCS 2.0/EO-WCS Client
 """

#         print "I'm in "+sys._getframe().f_code.co_name



import os, sys, pickle
#from xml.dom import minidom
from lxml import etree
from glob import glob

from qgis.core import *
from qgis.gui import *

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QProgressDialog, QDialog, QMessageBox, QFileDialog, QApplication, QCursor
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt4 import QtXml

from ui_qgswcsclient2 import Ui_QgsWcsClient2
from qgsnewhttpconnectionbasedialog import qgsnewhttpconnectionbase
from display_txtdialog import display_txt
from downloader import download_url 
from EOxWCSClient.wcs_client  import wcsClient



#global setttings and saved server list
global config
import config

global namespacemap
namespacemap = {"wcs": "http://www.opengis.net/wcs/2.0", "wcseo": "http://www.opengis.net/wcseo/1.0", "crs":  "http://www.opengis.net/wcs/service-extension/crs/1.0", "gml" : "http://www.opengis.net/gml/3.2", "gmlcov" : "http://www.opengis.net/gmlcov/1.0", "ogc" : "http://www.opengis.net/ogc", "ows" : "http://www.opengis.net/ows/2.0", "swe" : "http://www.opengis.net/swe/2.0", "int" : "http://www.opengis.net/WCS_service-extension_interpolation/1.0", "eop" : "http://www.opengis.net/eop/2.0", "om" : "http://www.opengis.net/om/2.0"  }
 


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


#---------------
def mouse_busy(function):
    def new_function(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        function(self)
        QApplication.restoreOverrideCursor()
    return new_function

#---------------

    # provide a pop-up warning message
def warning_msg(msg):
    msgBox = QtGui.QMessageBox()
    msgBox.setText(msg)
    msgBox.addButton(QtGui.QPushButton('OK'), QtGui.QMessageBox.YesRole)
    msgBox.exec_()
        
#---------------



class QgsWcsClient2Dialog(QtGui.QDialog, Ui_QgsWcsClient2):
    
    def __init__(self, iface):
        global config
        QtGui.QDialog.__init__(self)
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

            # instantiate the wcsClient 
        self.myWCS = wcsClient()
        
        self.treeWidget_GCa.itemClicked.connect(self.on_GCa_clicked)
        self.treeWidget_DC.itemClicked.connect(self.on_DC_clicked)
        self.treeWidget_DCS.itemClicked.connect(self.on_DCS_clicked)
        self.treeWidget_GCov.itemClicked.connect(self.on_GCov_clicked)

#---------------
        # remove all 'keys' which are set to 'None' from the request-parameter dictionary
    def clear_req_params(self,req_params):
        print "I'm in "+sys._getframe().f_code.co_name
        for k,v in req_params.items():
            if v is None:
                req_params.pop(k)
        return req_params

## ====== Beginning Server Tab-section ======


#---------------
        # add a new server to the list
    def newServer(self):
        global config
        print '444-btnNew: I am adding a New ServerName/URL'
#  not sure what to do with those flags 
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint  
        dlgNew = qgsnewhttpconnectionbase(self, flags, toEdit=False, choice='')
        dlgNew.show()
        self.btnConnectServer_Serv.setFocus(True)
        
##TODO -- sort the srv_list

#---------------
        # read the selected server/url params
    def get_serv_url(self):
        global serv
        sel_serv = self.cmbConnections_Serv.currentText()
        idx = serv.index(sel_serv)
        sel_url = config.srv_list['servers'][idx][1]
        return sel_serv, sel_url
 
#---------------
        # check if the url exist and if we get a respond to a simple OWS request
    @mouse_busy
    def connectServer(self):
        global config
        global serv

        selected_serv, selected_url = self.get_serv_url()
        print '555-btnTest: You choose: ', selected_serv,   "URL:", selected_url
        
        url_base = selected_url
            # &sections=ServiceMetadata  -- makes if faster, but some Servers don't provide/accept it
        url_ext1 = "service=WCS&request=GetCapabilities" #&sections=ServiceMetadata"
        myUrl = url_base + url_ext1
        msg = "Your choice:    "+selected_serv.encode()+"\n"
        msg = msg+"URL:                   "+selected_url.encode()+"\n"

        srv_valid = QUrl(myUrl).isValid()
        if  srv_valid is True:
            msg = msg+"Server address is valid \n"
            msg = msg+"Now testing the connection and response.....\n "
            msg = msg+"       this may take some time (depending on the server and the volume of its offering)\n"
            self.textBrowser_Serv.setText(msg)
        
        label_text = self.tr("Downloading....")
        self.progress_dialog.done(QDialog.Accepted)
        self.progress_dialog.cancel()
        self.progress_dialog.show()        
        
        req_qgsmng = QNetworkAccessManager(self)

        response = download_url(req_qgsmng, myUrl, None, self.progress_dialog)

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

        QApplication.restoreOverrideCursor()
        
#---------------
        # parse the response issued during "Server Connect" and set some parameters
    def parse_first_xml(self, in_xml):
        #join_xml = ''.join(e.encode() for e in in_xml)
        join_xml = ''.join(in_xml)

#        _xml_ID_tag = ["wcs:formatSupported", "crs:crsSupported"]
#        _result_tag = ["outformat", "outcrs"]

## TODO - maybe change to use etree/xpath
#        tree.etree.parse(join_xml)
        tree1 = etree.fromstring(join_xml)
        outformat = tree1.xpath("wcs:ServiceMetadata/wcs:formatSupported/text()", namespaces=namespacemap)
        outcrs = tree1.xpath("wcs:ServiceMetadata/wcs:Extension/crs:crsSupported/text()", namespaces=namespacemap)
        interpol = tree1.xpath("wcs:ServiceMetadata/wcs:Extension/int:interpolationSupported/text()", namespaces=namespacemap)
        oformat_num = len(outformat)
        ocrs_num = len(outcrs)
        interpol_num = len(interpol)
        support_outcrs = []
        support_interpol = []

        for elem in outcrs:
            support_outcrs.append(os.path.basename(elem))

        for elem in interpol:
            support_interpol.append(os.path.basename(elem))

        for elem in range (0, oformat_num):
            self.comboBox_GCOvOutFormat.addItem(_fromUtf8(""))
            self.comboBox_GCOvOutFormat.setItemText(elem, _translate("QgsWcsClient2", outformat[elem], None))
                                                             
        for elem in range (0, ocrs_num):
            self.comboBox_GCovOutCRS.addItem(_fromUtf8(""))
            self.comboBox_GCovOutCRS.setItemText(elem, _translate("QgsWcsClient2", support_outcrs[elem], None))

        for elem in range (0, interpol_num):
            self.comboBox_GCovInterpol.addItem(_fromUtf8(""))
            self.comboBox_GCovInterpol.setItemText(elem, _translate("QgsWcsClient2", support_interpol[elem], None))
        
        

#---------------
        # modify a server entry
    def editServer(self):
        global config
        #print "444-btnEdit:  here we are editing... "
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint

        idx = self.cmbConnections_Serv.currentIndex()
        select_serv = config.srv_list['servers'][idx]

        print "Selection: ", idx, " -- ", select_serv, " -- Check: ", serv[idx]

        dlgEdit = qgsnewhttpconnectionbase(self, flags, toEdit=True, choice=idx )  
        dlgEdit.txt_NewSrvName.setText(select_serv[0])
        dlgEdit.txt_NewSrvUrl.setText(select_serv[1])
        dlgEdit.show()
        self.btnConnectServer_Serv.setFocus(True)
        
#---------------
        # dele a server entry
    def deleteServer(self):
        global config
        #print "444-btnDelete:  here we are deleting...."
        idx = self.cmbConnections_Serv.currentIndex()
        config.srv_list['servers'].pop(idx)
        
        self.write_srv_list()        
        self.updateServerListing()
        self.btnConnectServer_Serv.setFocus(True)
        
#---------------
        # update the server-listing shown in the selectionBar
    def updateServerListing(self):
        global serv
        global config
        serv = []
        config.srv_list = config.read_srv_list()
        for ii in range(len(config.srv_list['servers'])):
            serv.append(config.srv_list['servers'][ii][0][:])
            
        self.cmbConnections_Serv.clear()
        self.cmbConnections_Serv.addItems(serv)

#---------------
       # write the sever names/urls to a file
    @mouse_busy
    def write_srv_list(self):
        plugin_dir = os.path.dirname(os.path.realpath(__file__))
        outsrvlst = os.path.join(plugin_dir,'config_srvlist.pkl')
        fo = open(outsrvlst, 'wb')
        p = pickle.dump(config.srv_list, fo, 0)
        fo.close()

#---------------
        # get the path where the downloaded datasets shall be stored
    @mouse_busy
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
        # read-out params from the GetCapabilities Tab, execute the request and show results
    @mouse_busy
    def exeGetCapabilities(self):
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

        req_sections =','.join(req_sections)
        if len(req_sections) == 0:  
            req_sections = None
            
        req_params = {'request': 'GetCapabilities',
            'server_url': selected_url ,
            'updateSequence': req_updateDate,
            'sections' : req_sections }

        req_params = self.clear_req_params(req_params)
        print 'GCa: ',req_params


        GCa_result = self.myWCS.GetCapabilities(req_params)

        cov_ids, dss_ids, dss_begin, dss_end = self.parse_GCa_xml(GCa_result) 
        
        if len(dss_ids) > 0:
            for a,b,c in zip(dss_ids, dss_begin, dss_end):
                inlist =(a,b,c,"S")
                item = QtGui.QTreeWidgetItem(self.treeWidget_GCa, inlist)
        
        if len(cov_ids) > 0:
            for elem in cov_ids:
                inlist = (elem, "","","C")
                item = QtGui.QTreeWidgetItem(self.treeWidget_GCa, inlist)

        self.treeWidget_GCa.resizeColumnToContents(0)

        QApplication.restoreOverrideCursor()

#---------------
        # GetCapabilities button
    def on_GCa_clicked(self):
        global cov_ids
        global dss_ids

        sel_GCa_items = self.treeWidget_GCa.selectedItems()
        self.treeWidget_DC.clear()
        self.treeWidget_DCS.clear()
        self.treeWidget_GCov.clear()
        

        
        for elem in sel_GCa_items:
          #     @@@                    covID          BeginTime       EndTime          [C]/[S]   
            print 'Selected Item: ',elem.data(0,0), elem.data(1,0), elem.data(2,0), elem.data(3,0)
            if elem.data(0,0) in cov_ids:
                item = QtGui.QTreeWidgetItem(self.treeWidget_DC, (elem.data(0,0),))
                #item1 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, (elem.data(0,0),))
                item2 = QtGui.QTreeWidgetItem(self.treeWidget_GCov, (elem.data(0,0),))
            elif elem.data(0,0) in dss_ids:
                item1 = QtGui.QTreeWidgetItem(self.treeWidget_DCS, (elem.data(0,0),elem.data(1,0),elem.data(2,0)))
 
        self.treeWidget_DC.resizeColumnToContents(0)
        self.treeWidget_DCS.resizeColumnToContents(0)
        self.treeWidget_GCov.resizeColumnToContents(0)


#---------------
        # updateDate field
    def updateDateChanged(self):
        if self.dateEdit_GCaDocUpdate.isEnabled():
            self.dateEdit_GCaDocUpdate.setEnabled(False)
        else:
            self.dateEdit_GCaDocUpdate.setEnabled(True)


#---------------
        # parse GetCapabilities XML-response 
    def parse_GCa_xml(self, GCa_result): 
        #print "I'm in "+sys._getframe().f_code.co_name
        join_xml = ''.join(GCa_result)
#        tree = etree.parse(GCa_result)
        tree = etree.fromstring(join_xml)
        coverage_ids = tree.xpath("wcs:Contents/wcs:CoverageSummary/wcs:CoverageId/text()", namespaces=namespacemap)
        datasetseries_ids = tree.xpath("wcs:Contents/wcs:Extension/wcseo:DatasetSeriesSummary/wcseo:DatasetSeriesId/text()",                                    namespaces=namespacemap)
        datasetseries_timeBegin = tree.xpath("wcs:Contents/wcs:Extension/wcseo:DatasetSeriesSummary/gml:TimePeriod/gml:beginPosition/text()", namespaces=namespacemap)

        datasetseries_timeEnd = tree.xpath("wcs:Contents/wcs:Extension/wcseo:DatasetSeriesSummary/gml:TimePeriod/gml:endPosition/text()", namespaces=namespacemap)

        return coverage_ids, datasetseries_ids, datasetseries_timeBegin, datasetseries_timeEnd


## ====== End of GetCapabilities section ======

## ====== Beginning DescribeCoverage section ======
        # read-out the DescribeCoverage Tab, execute a DescribeCoverage request and display response
        # in a general purpose window
    @mouse_busy
    def exeDescribeCoverage(self):
        global selected_covid
        global offered_crs
        selected_serv, selected_url = self.get_serv_url()
        
        try:
            req_params = {'request': 'DescribeCoverage',
                'server_url':  selected_url, 
                'coverageID':  selected_covid }
        except NameError:
            msg = "Error,    You need to select a CoverageID first!\n   (see also GetCapabilities TAB)"
            warning_msg(msg)
            #self.tabWidget_EOWcsClient2.setCurrentIndex(1)
            return
        
        
        req_params = self.clear_req_params(req_params)
        print "DC: ", req_params
        
        DC_result = self.myWCS.DescribeCoverage(req_params)

            # also read out the gml:Envelope axisLabels - use only first returned entry
        join_xml = ''.join(DC_result)
        tree = etree.fromstring(join_xml)
        #axis_labels = tree.xpath("wcs:CoverageDescription/gml:boundedBy/gml:Envelope/@axisLabels", namespaces=namespacemap)
        axis_labels = tree.xpath("wcs:CoverageDescription/gml:boundedBy/gml:Envelope/@axisLabels|wcs:CoverageDescription/gml:boundedBy/gml:EnvelopeWithTimePeriod/@axisLabels", namespaces=namespacemap)
        axis_labels = axis_labels[0].encode().split(" ")
        print axis_labels
        #offered_crs = tree.xpath("wcs:CoverageDescription/gml:boundedBy/gml:Envelope/@srsName", namespaces=namespacemap)
        offered_crs = tree.xpath("wcs:CoverageDescription/gml:boundedBy/gml:Envelope/@srsName|wcs:CoverageDescription/gml:boundedBy/gml:EnvelopeWithTimePeriod/@srsName", namespaces=namespacemap)
        offered_crs = os.path.basename(offered_crs[0])
        print offered_crs
        if len(axis_labels) == 0:
            axis_labels = ["",""]
        if len(offered_crs) == 0:
            offered_crs = '4326'

            # now set the parameters in the GetCoverage Tab
        self.lineEdit_GCovXAxisLabel.setText(axis_labels[0])
        self.lineEdit_GCovYAxisLabel.setText(axis_labels[1])
        combo_idx = self.comboBox_GCovOutCRS.findText(offered_crs)
        self.comboBox_GCovOutCRS.setCurrentIndex(combo_idx)
        

            # open a new window to display the returned DescribeCoverage-Response XMl 
        myDisplay_txt =  display_txt(self)
        myDisplay_txt.textBrowser_Disp.setText(DC_result)
        myDisplay_txt.show()

        QApplication.restoreOverrideCursor()
      
#---------------
        # the DescribeCoverage Button
    def on_DC_clicked(self):
        global selected_covid
        sel_DC_items = self.treeWidget_DC.selectedItems()
        selected_covid = sel_DC_items[0].data(0,0).encode()
#        return 

#---------------
        # parse DescribeCoverage XML-response 
    def parse_DC_xml(self, DC_result): 
        #print "I'm in "+sys._getframe().f_code.co_name
        join_xml = ''.join(DC_result)



## ====== End of DescribeCoverage section ======

## ====== Beginning DescribeEOCoverageSet section ======
        # read-out the DescribeEOCoverageSet Tab, execute a DescribeEOCoverageSet request and display response
        # in the GetCoverage Tab (for further selection and execution)
    @mouse_busy
    def exeDescribeEOCoverageSet(self):
        global selected_eoid
        global offered_crs
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
            req_toi = str(beginTime.strip()+","+endTime.strip())
        else:
            req_toi = None
            

        try:
            selected_eoid = ','.join(selected_eoid)
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
        except NameError:
            msg = "Error,    You need to select an DatasetSeriesID (eoID) first!\n   (see also GetCapabilities TAB)"
            warning_msg(msg)
            #self.tabWidget_EOWcsClient2.setCurrentIndex(1)
            return


        req_params = self.clear_req_params(req_params)
        print "DCS: ",req_params

        if req_params.has_key('IDs_only') and req_params['IDs_only'] == True:
            DCS_result, axis_labels, offered_crs = self.myWCS.DescribeEOCoverageSet(req_params)
            self.lineEdit_GCovXAxisLabel.setText(axis_labels[0])
            self.lineEdit_GCovYAxisLabel.setText(axis_labels[1])
            combo_idx = self.comboBox_GCovOutCRS.findText(offered_crs)
            self.comboBox_GCovOutCRS.setCurrentIndex(combo_idx)
        else:
            DCS_result = self.myWCS.DescribeEOCoverageSet(req_params)


##TODO add Button to also allow to view the full XML-Response file (=> Getcapabilities, DescribeEOCoverageSet)        
        #myDisplay_txt =  display_txt(self)
        #myDisplay_txt.textBrowser_Disp.setText(DCS_result)
        #myDisplay_txt.show()


        if req_params['IDs_only'] == True:
            #self.treeWidget_DCS.clear()
            self.treeWidget_GCov.clear()
            for elem in DCS_result:
                item = QtGui.QTreeWidgetItem(self.treeWidget_GCov, [elem])
                
                # once results are available - put 'Focus' on --> tab_GCov
            self.tabWidget_EOWcsClient2.setCurrentIndex(4)
            self.treeWidget_GCov.resizeColumnToContents(0)    
        else:
                # just display full result with a text-viewer
            myDisplay_txt =  display_txt(self)
            myDisplay_txt.textBrowser_Disp.setText(DCS_result)
            myDisplay_txt.show()


        self.treeWidget_DCS.resizeColumnToContents(0)

        QApplication.restoreOverrideCursor()

#---------------
        # activate the 2 Date-Subsetting selection fields
    def enableDCS_ActiveDate(self):
        if self.dateTimeEdit_DCSBegin.isEnabled():
            self.dateTimeEdit_DCSBegin.setEnabled(False)
            self.dateTimeEdit_DCSEnd.setEnabled(False)
        else:
            self.dateTimeEdit_DCSBegin.setEnabled(True)
            self.dateTimeEdit_DCSEnd.setEnabled(True)

#---------------
        # activate the Count field
    def enableDCS_ActiveCount(self):
        if self.spinBox_DCSCount.isEnabled():
            self.spinBox_DCSCount.setEnabled(False)
        else:
            self.spinBox_DCSCount.setEnabled(True)

#---------------
        # DescribeEOCoverageSet Button
    def on_DCS_clicked(self):
        global selected_eoid
        selected_eoid = []
        sel_DCS_items = self.treeWidget_DCS.selectedItems()
        for elem in sel_DCS_items:
            selected_eoid.append(elem.data(0,0).encode())
            print "SELECTED: ", selected_eoid, type(selected_eoid)   #sel_DC_items[0].data(0,0)
            item2 = QtGui.QTreeWidgetItem(self.treeWidget_GCov, elem)
#       return 



## ====== End of DescribeEOCoverageSet section ======

## ====== Beginning GetCoverage section ======
        # read-out the GetCoverage Tab and execute the GetCoverage request
    @mouse_busy
    def exeGetCoverage(self):
        global selected_gcovid
        global req_outputLoc
        global offered_crs
        
        selected_serv, selected_url = self.get_serv_url()

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
            req_lon = req_subsetCRS+" "+req_x_label+" "+str(min_x+","+max_x)

        if ( len(min_y) == 0 or len(max_y) == 0 ): 
            req_lat = None
        else:
            req_lat = req_subsetCRS+" "+req_y_label+" "+str(min_y+","+max_y)


        if req_outputcrs == offered_crs:
            req_outputcrs = None

        if not "req_outputLoc" in globals(): 
            msg = "Error: For downloading coverages you need to supply a Local Storage Path --> see TAB Server / Storage"
            QMessageBox.critical(self, "Error",  msg, QMessageBox.Ok )
                # put focus on Server/STorage Tab to allow provision of Output Location
            self.tabWidget_EOWcsClient2.setCurrentIndex(0)
            req_outputLoc = self.get_outputLoc()
        elif len(req_outputLoc) == 0:
            self.tabWidget_EOWcsClient2.setCurrentIndex(0)
            req_outputLoc = self.get_outputLoc()
        else:
            req_outputLoc = self.lineEdit_Serv_OutputLoc.text()


        try: 
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
 
                # print 'GCov: ',req_params
                req_params = self.clear_req_params(req_params)
                # print 'GCov: ',req_params
                GCov_result = self.myWCS.GetCoverage(req_params)
                print "GCov_result: ", GCov_result

                self.add_to_map(req_params) 
                
        except NameError:
            msg = "Error,    You need to select one or more CoverageIDs first!\n "
            warning_msg(msg)
            #self.tabWidget_EOWcsClient2.setCurrentIndex(1)
            return



## TODO -- mediatype & mask --> not yet implemented
                    # 'mask': '&mask=polygon,'+crs_url, 
                    # 'mediatype': '&mediatype=',  # multipart/mixed' (default = parameter not provided)

                #req_params = self.clear_req_params(req_params)
                #print 'GCov: ',req_params

                #GCov_result = self.myWCS.GetCoverage(req_params)
        

## TODO -- Register the downloaded datsets with QGis MapCanvas -> load and show
#            self.add_to_map(req_params)

        QApplication.restoreOverrideCursor()




#---------------
        # GetCoverage Button
    def on_GCov_clicked(self):
        global selected_gcovid
        selected_gcovid = []
        sel_GCov_items = self.treeWidget_GCov.selectedItems()
        for elem in sel_GCov_items:
            selected_gcovid.append(elem.data(0,0).encode())
            print "SELECTED: ", selected_gcovid   #sel_DC_items[0].data(0,0)
            item = QtGui.QTreeWidgetItem(self.treeWidget_DC, (elem.data(0,0).encode(),))
            #item = QtGui.QTreeWidgetItem(self.treeWidget_GCov, (elem.data(0,0).encode(),))
#        return 

 
#---------------
        # activate the SubsetCRS setting and field
    def enableGCov_SubCRS(self):
        if self.radioButton_GCovSubCRS.isChecked():
            self.radioButton_GCovSubOrig.setChecked(False)
            self.radioButton_GCovSubPixel.setChecked(False)
            self.lineEdit_GCovSubEPSG.setEnabled(True)

#---------------
        # activate the SubsetPixel setting
    def enableGCov_SubPixel(self):
       if self.radioButton_GCovSubPixel.isChecked():
            self.radioButton_GCovSubCRS.setChecked(False)
            self.radioButton_GCovSubOrig.setChecked(False)
            self.lineEdit_GCovSubEPSG.setEnabled(False)

#---------------            
        # activate the OriginalCRS setting
    def enableGCov_SubOrig(self):
       if self.radioButton_GCovSubOrig.isChecked():
            self.radioButton_GCovSubCRS.setChecked(False)
            self.radioButton_GCovSubPixel.setChecked(False)
            self.lineEdit_GCovSubEPSG.setEnabled(False)

#---------------
        # enabele scaling X-Size 
    def enableGCov_XSize(self):
        if self.radioButton_GCovXSize.isChecked():
            self.radioButton_GCov_OutSizeOrig.setChecked(False)
            self.lineEdit_GCovXAxisLabel.setEnabled(True)
            self.lineEdit_GCovXSize.setEnabled(True)
            self.radioButton_GCovXRes.setChecked(False)

#---------------
        # enabele scaling X-Resolution 
    def enableGCov_XResolution(self):
        if self.radioButton_GCovXRes.isChecked():
            self.radioButton_GCov_OutSizeOrig.setChecked(False)
            self.radioButton_GCovXSize.setChecked(False)
            self.lineEdit_GCovXAxisLabel.setEnabled(True)
            self.lineEdit_GCovXSize.setEnabled(True)

#---------------
        # enabele scaling Y-Size             
    def enableGCov_YSize(self):
        if self.radioButton_GCovYSize.isChecked():
            self.radioButton_GCov_OutSizeOrig.setChecked(False)
            self.lineEdit_GCovYAxisLabel.setEnabled(True)
            self.lineEdit_GCovYSize.setEnabled(True)
            self.radioButton_GCovYRes.setChecked(False)

#---------------
        # enabele scaling Y-Resolution
    def enableGCov_YResolution(self):
        if self.radioButton_GCovYRes.isChecked():
            self.radioButton_GCov_OutSizeOrig.setChecked(False)
            self.radioButton_GCovYSize.setChecked(False)
            self.lineEdit_GCovYAxisLabel.setEnabled(True)
            self.lineEdit_GCovYSize.setEnabled(True)

#---------------
        # reset scaling to original size/resolution
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
## ====== Add data to Map Canvas ======
        # read the the downloaded datasets, register them and show them in the QGis MapCanvas
    def add_to_map(self, req_params):

        self.canvas = self.iface.mapCanvas()

        coverageID = req_params['output']+os.sep+req_params['coverageID']+'*'
        disp_coverage = glob(coverageID)
        covInfo = QFileInfo(disp_coverage[-1])
        cov_baseName = covInfo.baseName()
        cov_layer = QgsRasterLayer(disp_coverage[-1], cov_baseName.encode())

        if not cov_layer.isValid():
            print "Layer failed to load!"

        QgsMapLayerRegistry.instance().addMapLayer(cov_layer)


## ====== End of Add data to Map Canvas ======