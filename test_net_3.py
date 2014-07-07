from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtNetwork import *
import sys

#Subclass QNetworkAccessManager Here
class NetworkAccessManager(QNetworkAccessManager):
  
  #Save image data in QByteArray buffer to the disk (google_image_logo.png
  # in the same directory)
  @pyqtSlot()
  def slotFinished(self):
    print "7777: Slot finished"
    #imageFile = QFile("google_image_logo.png")
    outfile=QFile("/home/schillerc/cs_pylib/wcs_qgis_plugin/QgsWcsClient2/1_testServer.xml")
    if(outfile.open(QIODevice.WriteOnly)):
      outfile.write(self.messageBuffer)
      outfile.close()      
      QMessageBox.information(None, "Hello!","File has been saved!") 
    else:
      QMessageBox.critical(None, "Hello!","Error saving file!")

  #Append current data to the buffer every time readyRead() signal is emitted
  @pyqtSlot()
  def slotReadData(self):
    print "8888: Slot ReadData"
    self.messageBuffer += self.reply.readAll().data()
    
    
  def __init__(self, myUrl):
    QNetworkAccessManager.__init__(self)
    self.messageBuffer = QByteArray()
    #url   = QUrl("http://upload.wikimedia.org/wikipedia/commons/f/fe/Google_Images_Logo.png")
    url = QUrl(myUrl)
    print "6666:  we are in NetworkManager", url
    req   = QNetworkRequest(url)
    self.reply = self.get(req)    
    
    QObject.connect(self.reply,SIGNAL("readyRead()"),self,SLOT("slotReadData()"))
    QObject.connect(self.reply,SIGNAL("finished()"), self,SLOT("slotFinished()")) 
 
# End of NetworkAccessManager Class
###################################

