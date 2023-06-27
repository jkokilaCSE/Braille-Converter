import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow ,QMessageBox
from PyQt5.QtGui import QIcon

from firebase import Firebase

import json

from collections import OrderedDict

from tinydb import TinyDB, where
from tinydb.operations import delete

from BrailleConverter import Ui_MainWindow

config = {  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "storageBucket": ""}

firebase = Firebase(config)
db = firebase.database()

verified=[];email=[];key=[]

dbt = TinyDB('verify.json')

with open('verify.json') as f:
    dataa = json.load(f)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(479, 234)
        self.label = QtWidgets.QLabel(Dialog)

        self.label.setGeometry(QtCore.QRect(150, 0, 201, 71))
        self.label.setMaximumSize(QtCore.QSize(201, 16777215))
        self.label.setStyleSheet("color: blue ; font-size:20pt; align:center ; padding: 0px; margin-right:0px; margin-left:0px; margin-bottom:0px")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(-10, 80, 141, 31))
        self.label_2.setStyleSheet("margin-left:30px; font-size:15px;  margin-right:0px")
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(-10, 120, 141, 31))
        self.label_3.setStyleSheet("margin-left:30px; font-size:15px;  margin-right:0px")
        self.label_3.setObjectName("label_3")
        
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(150, 90, 221, 20))
        self.lineEdit.setObjectName("lineEdit")
        
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 130, 221, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 180, 221, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.verifyWindow)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def verifyWindow(self):
    
        try:

            email_input = self.lineEdit.text()
            email = str(email_input)
            verification_input = self.lineEdit_2.text()
            key = str(verification_input)
   
            # print("Username         : ",email)
            # print("Verification Key : ",key  )

            users = db.child(email).get( )
            value = users.val()

            print(value)
            time.sleep(2)

            if (str(value) == str(key)):
                # print("Authenticated")

                dbt.update({'verified': '1', 'email': email, 'key' : key})

                self.MainWindow = QtWidgets.QMainWindow()
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self.MainWindow)
                self.MainWindow.show()
                Dialog.hide()
            else:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle("Error Authenticating")
                # self.error_dialog.setWindowIcon(QtGui.QIcon("logo.png"))
                self.error_dialog.showMessage('Login Credentials are incorrect!')
                print ("Wrong id and password")

        except:
            self.MainWindow = QtWidgets.QMainWindow()
            QMessageBox.about(self.MainWindow, "No internet connection ", "Please check your internet connection !!")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Braille Verification"))
        Dialog.setWindowIcon(QIcon("logo.png"))
        self.label.setText(_translate("Dialog", "Braille Converter"))
        self.label_2.setText(_translate("Dialog", "Email-Id"))
        self.label_3.setText(_translate("Dialog", "Verification Key"))
        self.pushButton.setText(_translate("Dialog", "Verify !"))

verified.append(dataa["_default"]["1"]["verified"])
email.append(dataa["_default"]["1"]["email"])
key.append(dataa["_default"]["1"]["key"])

a=verified[0]
# print(a)

if __name__ == "__main__":
    import sys

    if int(a)==1:

        # print("Already Verified")

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

    else:
        
        # print("Not Verified")

        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec_())