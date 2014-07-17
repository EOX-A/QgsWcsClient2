# -*- coding: utf-8 -*-

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

