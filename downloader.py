#noinspection PyPackageRequirements
from PyQt4 import QtCore, QtGui, Qt
#noinspection PyPackageRequirements
from PyQt4.QtCore import QCoreApplication, QFile, QUrl
#noinspection PyPackageRequirements
from PyQt4.QtNetwork import QNetworkRequest, QNetworkReply


# Source: 
# http://inasafe.org/fr/_modules/safe_qgis/utilities/utilities.html#download_url

#global xml_result
#xml_result=[]

def download_url(manager, url, output_path, progress_dialog=None):
    """Download file from url.

    :param manager: A QNetworkAccessManager instance
    :type manager: QNetworkAccessManager

    :param url: URL of file
    :type url: str

    :param output_path: Output path
    :type output_path: str

    :param progress_dialog: Progress dialog widget
## TODO 
    :returns: True if success, otherwise returns a tuple with format like this
        (QNetworkReply.NetworkError, error_message)
    :raises: IOError - when cannot create output_path
    """
    global xml_result
    xml_result=[]
    
        # prepare output path
    if output_path is not None:   
        out_file = QFile(output_path)
        if not out_file.open(QFile.WriteOnly):
            raise IOError(out_file.errorString())


    # slot to write data to file
    def write_data():
        """Write data to a file."""
        global xml_result
#        out_file.write(reply.readAll())
        xml_result = reply.readAll().data()
#        print "VVV: ", xml_result
        out_file.write(xml_result)
        out_file.flush()

    def read_data():
        """ Read data to a variable and return variable"""
        global xml_result
        xml_result.append(reply.readAll().data())


    request = QNetworkRequest(QUrl(url))
    reply = manager.get(request)

    if output_path is None:
        reply.readyRead.connect(read_data)
#        print 'UUU: ', xml_result
    else: 
        reply.readyRead.connect(write_data)



    if progress_dialog:
        # progress bar
        def progress_event(received, total):
            """Update progress.

            :param received: Data received so far.
            :type received: int
            :param total: Total expected data.
            :type total: int

            """

            # noinspection PyArgumentList
            QCoreApplication.processEvents()

            progress_dialog.setLabelText("%s / %s" % (received, total))
            progress_dialog.setMaximum(total)
            progress_dialog.setValue(received)
            


        # cancel
        def cancel_action():
            """Cancel download."""
            reply.abort()

        reply.downloadProgress.connect(progress_event)
        progress_dialog.canceled.connect(cancel_action)

    # wait until finished
    while not reply.isFinished():
        # noinspection PyArgumentList
        QCoreApplication.processEvents()


   
    

    result = reply.error()
    if result == QNetworkReply.NoError:
        if output_path is None:
            return True, None, xml_result
        else:
            out_file.close()
            return True, None, xml_result
    else:
        if output_path is not None:
            out_file.close()
        return result, str(reply.errorString())

    if  progress_dialog:
        progress_dialog.close()




