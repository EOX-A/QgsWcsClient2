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
 A donwload tool utilizing the QNetworkAccessManager instance
"""
from __future__ import print_function

from builtins import str
from qgis.PyQt.QtCore import QCoreApplication, QFile, QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply


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

    def read_data1():
        global xml_result1
        xml_result1 = []
        xml_result1.append(reply.readAll().data())
        return xml_result1


        # request the content of the url
    request = QNetworkRequest(QUrl(url))
    reply = manager.get(request)

    #print "EEE: ", reply.error(), reply.errorString(), reply.size()
    #print "AA1: ", reply.attribute(QNetworkRequest.HttpStatusCodeAttribute), type(reply.attribute(QNetworkRequest.HttpStatusCodeAttribute))
    #print "AA2: ", reply.attribute(QNetworkRequest.HttpReasonPhraseAttribute)
    #print "AA3: ", reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
    #print "=================="
    #print "1: AuthenticationRequiredError",reply.AuthenticationRequiredError
    #print "2: ConnectionRefusedError",reply.ConnectionRefusedError
    #print "3: ContentAccessDenied",reply.ContentAccessDenied
    #print "4: ContentNotFoundError",reply.ContentNotFoundError
    #print "5: ContentOperationNotPermittedError",reply.ContentOperationNotPermittedError
    #print "6: ContentReSendError",reply.ContentReSendError
    #print "7: HostNotFoundError",reply.HostNotFoundError
    #print "8: NetworkError",reply.NetworkError
    #print "9: NoError",reply.NoError
    #print "10: NotOpen",reply.NotOpen
    #print "12: OpenMode",reply.OpenMode
    #print "13: OpenModeFlag",reply.OpenModeFlag
    #print "14: OperationCanceledError",reply.OperationCanceledError
    #print "15: ProtocolFailure",reply.ProtocolFailure
    #print "16: ProtocolInvalidOperationError",reply.ProtocolInvalidOperationError
    #print "17: ProtocolUnknownError",reply.ProtocolUnknownError
    #print "18: ProxyAuthenticationRequiredError",reply.ProxyAuthenticationRequiredError
    #print "19: ProxyConnectionClosedError",reply.ProxyConnectionClosedError
    #print "20: ProxyConnectionRefusedError",reply.ProxyConnectionRefusedError
    #print "21: ProxyNotFoundError",reply.ProxyNotFoundError
    #print "22: ProxyTimeoutError",reply.ProxyTimeoutError
    #print "23: ReadOnly",reply.ReadOnly
    #print "24: ReadWrite",reply.ReadWrite
    #print "25: RemoteHostClosedError",reply.RemoteHostClosedError
    #print "26: SslHandshakeFailedError",reply.SslHandshakeFailedError
    #print "27: TemporaryNetworkFailureError",reply.TemporaryNetworkFailureError
    #print "28: Text",reply.Text
    #print "29: TimeoutError",reply.TimeoutError
    #print "30: Truncate",reply.Truncate
    #print "31: Unbuffered",reply.Unbuffered
    #print "32: UnknownContentError",reply.UnknownContentError
    #print "33: UnknownNetworkError",reply.UnknownNetworkError
    #print "34: UnknownProxyError",reply.UnknownProxyError
    # to call the manager again seems to be needed, the reply seems to get overwritten or cleared by the above calls
    #reply = manager.get(request)

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

    if reply.attribute(QNetworkRequest.RedirectionTargetAttribute):
        redir_url = reply.attribute(QNetworkRequest.RedirectionTargetAttribute).toString().split('?')[0]+'?'
        # fix_print_with_import
        # fix_print_with_import
        print('Redirection-Url:',redir_url, type(redir_url))
        return True, None, 'Redirection-URL:\t'+redir_url

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




