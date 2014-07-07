# -*- coding: utf-8 -*-

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

