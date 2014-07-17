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
"""
# Form implementation generated from reading ui file 'display_txt.ui'
#
# Created: Fri Jul 11 17:52:52 2014
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

class Ui_Dialog_Disp(object):
    def setupUi(self, Dialog_Disp):
        Dialog_Disp.setObjectName(_fromUtf8("Dialog_Disp"))
        Dialog_Disp.resize(721, 610)
        self.pushButton_DIsp_Done = QtGui.QPushButton(Dialog_Disp)
        self.pushButton_DIsp_Done.setGeometry(QtCore.QRect(610, 570, 98, 27))
        self.pushButton_DIsp_Done.setObjectName(_fromUtf8("pushButton_DIsp_Done"))
        self.textBrowser_Disp = QtGui.QTextBrowser(Dialog_Disp)
        self.textBrowser_Disp.setGeometry(QtCore.QRect(10, 10, 701, 551))
        self.textBrowser_Disp.setObjectName(_fromUtf8("textBrowser_Disp"))

        self.retranslateUi(Dialog_Disp)
        QtCore.QObject.connect(self.pushButton_DIsp_Done, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog_Disp.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Disp)

    def retranslateUi(self, Dialog_Disp):
        Dialog_Disp.setWindowTitle(_translate("Dialog_Disp", "Dialog", None))
        self.pushButton_DIsp_Done.setText(_translate("Dialog_Disp", "Done", None))

