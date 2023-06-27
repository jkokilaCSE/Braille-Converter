from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon

from tinydb import TinyDB, where
from tinydb.operations import delete

import datetime
import json

class Ui_Dialog(object):

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(503, 302)
        # Dialog.resize(600, 400)

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 471, 281))
        self.widget.setObjectName("widget")

        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 451, 261))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 449, 259))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 431, 241))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        # self.tableWidget.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.DBConnection()

    def retranslateUi(self, Dialog):

        _translate = QtCore.QCoreApplication.translate

        Dialog.setWindowTitle(_translate("Dialog", "Conversion History Table"))
        Dialog.setWindowIcon(QIcon("logo.png"))
        # Dialog.setWindowFlag(Qt::WindowContextHelpButtonHint,false)

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Upload File Name"))

        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Saved File Name"))

        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Date Saved On"))

        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Time Saved On"))

    def DBConnection(self):
        try:
            print ("Inside the try")
            uploadarray=[];savearray=[];datearray=[];timearray=[]

            db = TinyDB('db.json')
            out = db.all()

            with open('db.json') as f:
                data = json.load(f)

            x=len(db)
            print(x)

            for i in range (len(db)):
                i+=1
                uploadarray.append(data["_default"][str(i)]["Upload"])
                savearray.append(data["_default"][str(i)]["Saved"])
                datearray.append(data["_default"][str(i)]["Date"])
                timearray.append(data["_default"][str(i)]["Time"])

            for j in range (x):
                # print(j)

                self.tableWidget.insertRow(j)

                self.tableWidget.setItem(j, 0, QTableWidgetItem(str(uploadarray[j])))
                self.tableWidget.setItem(j, 1, QTableWidgetItem(str(savearray[j])))
                self.tableWidget.setItem(j, 2, QTableWidgetItem(str(datearray[j])))
                self.tableWidget.setItem(j, 3, QTableWidgetItem(str(timearray[j])))

        except:
            print("Failed")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
