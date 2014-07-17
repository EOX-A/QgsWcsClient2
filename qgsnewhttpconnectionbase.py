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
 a dialog to set server names and urls to be used with this plugin
"""

# Form implementation generated from reading ui file 'qgsnewhttpconnectionbase.ui'
#
# Created: Thu Jul  3 14:57:42 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_qgsnewhttpconnectionbase(object):
    def setupUi(self, qgsnewhttpconnectionbase):
        qgsnewhttpconnectionbase.setObjectName(_fromUtf8("qgsnewhttpconnectionbase"))
        qgsnewhttpconnectionbase.resize(619, 153)
        self.buttonBox = QtGui.QDialogButtonBox(qgsnewhttpconnectionbase)
        self.buttonBox.setGeometry(QtCore.QRect(260, 100, 341, 32))
        self.buttonBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label_NewSrvName = QtGui.QLabel(qgsnewhttpconnectionbase)
        self.label_NewSrvName.setGeometry(QtCore.QRect(40, 30, 66, 17))
        self.label_NewSrvName.setObjectName(_fromUtf8("label_NewSrvName"))
        self.label_NewSrvUrl = QtGui.QLabel(qgsnewhttpconnectionbase)
        self.label_NewSrvUrl.setGeometry(QtCore.QRect(40, 90, 66, 17))
        self.label_NewSrvUrl.setObjectName(_fromUtf8("label_NewSrvUrl"))
        self.txt_NewSrvName = QtGui.QLineEdit(qgsnewhttpconnectionbase)
        self.txt_NewSrvName.setEnabled(True)
        self.txt_NewSrvName.setGeometry(QtCore.QRect(100, 30, 501, 27))
        self.txt_NewSrvName.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.txt_NewSrvName.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.txt_NewSrvName.setObjectName(_fromUtf8("txt_NewSrvName"))
        self.txt_NewSrvUrl = QtGui.QLineEdit(qgsnewhttpconnectionbase)
        self.txt_NewSrvUrl.setGeometry(QtCore.QRect(100, 70, 501, 27))
        self.txt_NewSrvUrl.setObjectName(_fromUtf8("txt_NewSrvUrl"))

        self.retranslateUi(qgsnewhttpconnectionbase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), qgsnewhttpconnectionbase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), qgsnewhttpconnectionbase.reject)
        QtCore.QMetaObject.connectSlotsByName(qgsnewhttpconnectionbase)

    def retranslateUi(self, qgsnewhttpconnectionbase):
        qgsnewhttpconnectionbase.setWindowTitle(_translate("qgsnewhttpconnectionbase", "New WCS Server ", None))
        self.label_NewSrvName.setText(_translate("qgsnewhttpconnectionbase", "Name", None))
        self.label_NewSrvUrl.setText(_translate("qgsnewhttpconnectionbase", "URL", None))

