
from PyQt4.QtCore import *
#from PyQt4.QtNetwork import *
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager  # , QUrl
from PyQt4.QtGui import QApplication,QMessageBox
from PyQt4 import QtXml
from qgis.core import QgsNetworkAccessManager
import os


#req_base = select_url
req_base="http://neso.cryoland.enveo.at/cryoland/ows?"
req_p1 = "service=wcs&request=GetCapabilities&sections=ServiceMetadata"
myRequest = req_base + req_p1



def requestCapabilities():
    """
    Request server capabilities
    """
    doc = None
    url = QUrl()
    
    #if '?' in self.baseUrl:
        #myRequest = "&Request=GetCapabilities&identifier=&Service=WPS&Version=" + self.version
    #else:    
        #myRequest = "?Request=GetCapabilities&identifier=&Service=WPS&Version=" + self.version
        
    url.setUrl(myRequest)
    myHttp = QgsNetworkAccessManager.instance()
    _theReply = myHttp.get(QNetworkRequest(url))
    _theReply.finished.connect(_capabilitiesRequestFinished)
    
    from IPython import embed
    embed()


result = requestCapabilities()
        
print 'DONE'
