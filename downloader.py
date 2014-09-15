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
 A donwload tool utilizing the QNetworkAccessManager instance
"""

from PyQt4.QtCore import QCoreApplication, QFile, QUrl
from PyQt4.QtNetwork import QNetworkRequest, QNetworkReply


def download_url(manager, url, output_path, progress_dialog=None):
    global xml_result
    xml_result = []

        # set up the  output path
    if output_path is not None:
        out_file = QFile(output_path)
        if not out_file.open(QFile.WriteOnly):
            raise IOError(out_file.errorString())


        # write data to file
    def write_data():
        global xml_result
        xml_result = reply.readAll().data()
        out_file.write(xml_result)
        out_file.flush()

        # read data from response
    def read_data():
        global xml_result
        xml_result.append(reply.readAll().data())

        # request the content of the url
    request = QNetworkRequest(QUrl(url))
    reply = manager.get(request)

    if output_path is None:
        reply.readyRead.connect(read_data)
    else:
        reply.readyRead.connect(write_data)



    if progress_dialog:
        def progress_event(received, total):
            QCoreApplication.processEvents()

            progress_dialog.setLabelText("%s / %s" % (received, total))
            progress_dialog.setMaximum(total)
            progress_dialog.setValue(received)

            # cancel the download
        def cancel_action():
            reply.abort()

        reply.downloadProgress.connect(progress_event)
        progress_dialog.canceled.connect(cancel_action)


        # wait until donwload is finished
    while not reply.isFinished():
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




