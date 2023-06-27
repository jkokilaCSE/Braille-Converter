
from PyQt5 import QtCore, QtGui, QtWidgets

import sys

# PYQT5 importing stuff
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QWidget, QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot ,QFile

#Other Screen Files of PYQT5
# from database_historyscreen import TableView
# from ConversionTable import TableView
from historytable import Ui_Dialog
from alphabetTable import Ui_Dialog1

#Database Importing libraries of TinyDb
from tinydb import TinyDB, where
from tinydb.operations import delete

#The library to read pdf's
import PyPDF2 

#Importing Date and time for the History screens 
import datetime
import json

#Importing the Pdf's Reading library
from fpdf import FPDF

#Importing the encoding library to write the file 
import codecs

#Importing time module 
import time

asciicodes = [' ','!','"','#','$','%','&','','(',')','*','+',',','-','.','/','0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','@','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','[','\\',']','^','_']
brailles   = ['⠀','⠮','⠐','⠼','⠫','⠩','⠯','⠄','⠷','⠾','⠡','⠬','⠠','⠤','⠨','⠌','⠴','⠂','⠆','⠒','⠲','⠢','⠖','⠶','⠦','⠔','⠱','⠰','⠣','⠿','⠜','⠹','⠈','⠁','⠃','⠉','⠙','⠑','⠋','⠛','⠓','⠊','⠚','⠅','⠇','⠍','⠝','⠕','⠏','⠟','⠗','⠎','⠞','⠥','⠧','⠺','⠭','⠽','⠵','⠪','⠳','⠻','⠘','⠸']
dictonary = dict(zip(asciicodes,brailles))

caps = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L","M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

uploadarray=[];savearray=[];datearray=[];timearray=[]

x = datetime.datetime.now()

db = TinyDB('db.json')

with open('db.json') as f:
    data = json.load(f)

for i in range (len(db)):
    i+=1
    uploadarray.append(data["_default"][str(i)]["Upload"])
    savearray.append(data["_default"][str(i)]["Saved"])
    datearray.append(data["_default"][str(i)]["Date"])
    timearray.append(data["_default"][str(i)]["Time"])

data = {'Uploaded File Name':uploadarray,
        'Saved File Name':savearray,
        'Date Saved On':datearray,
        'Time Saved On':timearray}

data1 = {'English':asciicodes,
        'Braille':brailles}

opencheck=0
savecheck=0

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(779, 368)
        # MainWindow.setFixedSize(780,370)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 301, 301))
        self.textEdit.setObjectName("textEdit")

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(460, 20, 301, 301))
        self.textEdit_2.setObjectName("textEdit_2")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 220, 101, 31))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 270, 101, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(340, 170, 101, 31))
        self.pushButton_3.setObjectName("pushButton_3")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 779, 21))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuHistory = QtWidgets.QMenu(self.menubar)
        self.menuHistory.setObjectName("menuHistory")

        self.menuConversion_Table = QtWidgets.QMenu(self.menubar)
        self.menuConversion_Table.setObjectName("menuConversion_Table")

        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen_Text_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_Text_File.setObjectName("actionOpen_Text_File")
        self.actionOpen_Text_File.setShortcut('Ctrl+T')
        self.actionOpen_Text_File.triggered.connect(self.file_text)

        self.actionOpen_Pdf_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_Pdf_File.setObjectName("actionOpen_Pdf_File")
        self.actionOpen_Pdf_File.setShortcut('Ctrl+P')
        self.actionOpen_Pdf_File.triggered.connect(self.file_pdf)

        self.actionExit = QtWidgets.QAction(QIcon('exit24.png'),'Exit',MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.setStatusTip('Exit application')
        self.actionExit.triggered.connect(qApp.quit)

        self.actionOpen_History = QtWidgets.QAction(MainWindow)
        self.actionOpen_History.setObjectName("actionOpen_History")
        self.actionOpen_History.setShortcut('Ctrl+H')
        self.actionOpen_History.triggered.connect(self.openHistory)

        self.actionOpen_Conversion_Table = QtWidgets.QAction(MainWindow)
        self.actionOpen_Conversion_Table.setObjectName("actionOpen_Conversion_Table")
        self.actionOpen_Conversion_Table.setShortcut('Ctrl+B')
        self.actionOpen_Conversion_Table.triggered.connect(self.openConversion)


        self.menuFile.addAction(self.actionOpen_Text_File)
        self.menuFile.addAction(self.actionOpen_Pdf_File)
        self.menuFile.addAction(self.actionExit)

        self.menuHistory.addAction(self.actionOpen_History)

        self.menuConversion_Table.addAction(self.actionOpen_Conversion_Table)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHistory.menuAction())
        self.menubar.addAction(self.menuConversion_Table.menuAction())

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "Braille Converter"))
        MainWindow.setWindowIcon(QIcon("logo.png"))

        self.pushButton.setText(_translate("MainWindow", "Convert →"))
        self.pushButton.clicked.connect(self.convertMethod)

        self.pushButton_2.setText(_translate("MainWindow", "Save ↓"))
        self.pushButton_2.clicked.connect(self.saveEvent)
        
        self.pushButton_3.setText(_translate("MainWindow", "Clear ⌂"))
        self.pushButton_3.clicked.connect(self.clearMethod)

        self.menuFile.setTitle(_translate("MainWindow", "File"))

        self.menuHistory.setTitle(_translate("MainWindow", "History"))

        self.menuConversion_Table.setTitle(_translate("MainWindow", "Conversion Table"))

        self.actionOpen_Text_File.setText(_translate("MainWindow", "Open Text File"))

        self.actionOpen_Pdf_File.setText(_translate("MainWindow", "Open Pdf File"))

        self.actionExit.setText(_translate("MainWindow", "Exit"))

        self.actionOpen_History.setText(_translate("MainWindow", "Open History"))

        self.actionOpen_Conversion_Table.setText(_translate("MainWindow", "Open Conversion Table"))

    def clearMethod(self):
        self.textEdit.setText("") 
        self.textEdit_2.setText("")

    def openHistory(self):
        # self.table = TableView(data,len(db) + 10,4)
        # self.table.show()
        self.Dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        self.Dialog.show()

    def openConversion(self):
        # self.table1 = TableView(data1, 64, 2)
        # self.table1.resize(400, 200)
        # self.table1.show()
        self.Dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog1()
        self.ui.setupUi(self.Dialog)
        self.Dialog.show()

    def file_text(self):
        MainWindow = QtWidgets.QMainWindow()
        
        try:
            global fileName
            global uploadfileName

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(MainWindow,"Open Text File", "","Text Files (*.txt)", options=options)

            uploadfileName = fileName
            filee = open(uploadfileName, "r",errors='ignore')

            print(uploadfileName)

            #Code to extract fielname form the file locations

            uploadfileName=uploadfileName[::-1]
            result = uploadfileName.find('/')
            uploadfileName=uploadfileName[(result-1)::-1]
            
            print (uploadfileName)

            with filee:
                global content 
                content = filee.read()
                # print (content)

            self.textEdit.setText(content) 

            global opencheck
            opencheck=1
            print("Open check value - ",opencheck)
        
            self.convertMethod()

        except:
            QMessageBox.about(MainWindow, "Failed to Detect Text File", "No Text File was Selected")

    def file_pdf(self):
        MainWindow = QtWidgets.QMainWindow()
        
        try:
            global fileName
            global uploadfileName

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(MainWindow,"Open Pdf File", "","PDF's (*.pdf)", options=options)

            uploadfileName = fileName
            # filee = open(fileName, "r",errors='ignore')
            print(uploadfileName)

            pdf_file = open(str(fileName), 'rb')
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            # number_of_pages = read_pdf.getNumPages()
            page = read_pdf.getPage(0)
            page_content = page.extractText()

            uploadfileName=uploadfileName[::-1]
            result = uploadfileName.find('/')
            uploadfileName=uploadfileName[(result-1)::-1]

            # print (page_content)

            self.textEdit.setText(page_content) 
        
            global opencheck
            opencheck=1
            print("Open check value - ",opencheck)
        
            self.convertMethod()

        except:
            print("Unable to get the file ")
            QMessageBox.about(MainWindow, "Failed to Detect Pdf File", "No Pdf File was Selected")

    def convertMethod(self):

        textboxValue = self.textEdit.toPlainText()
        global b
        b=""
        
        for i in textboxValue :

            if i.isnumeric() or i.isalpha():
                wasnumber = 0
            else:
                wasnumber = 1

            wasalphabet = 0
            # print("wasnumber : ",wasnumber)
            break

        for i in textboxValue:

            if wasnumber==0 and i.isnumeric():
                b+=dictonary["#"]

            if wasnumber==1 and i.isalpha():
                b+=dictonary[";"]               

            if i.isalpha():
                wasalphabet = 1
            else:
                wasalphabet = 0

            if i.isnumeric():
                wasnumber = 1
            else:
                wasnumber = 0

            if i in caps:
                i=i.lower()
                b+=dictonary[","]+dictonary[i]

            elif i in dictonary:
                b+=dictonary[i]

            elif i not in dictonary and i not in caps:
                b+=i
                
            # print(b)
            self.textEdit_2.setText(b)
    
    def saveEvent(self):

        MainWindow = QtWidgets.QMainWindow() 
        # QMessageBox.about(MainWindow, 'Message', 'This part is under construction !!')

        try :
            
            global savefileName

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(MainWindow,"QFileDialog.getSaveFileName()","","Text Files (*.txt)", options=options)

            savefileName=fileName

            if savefileName:
                print(savefileName)

            savefileName+=".txt"

            fn = open(str(savefileName), "a", encoding="utf-8")

            print("Done Creating")
            
            fn.write(b)
            print("Done writing ")

            fn.close()
            print("Closed the document ")

            savefileName=savefileName[::-1]
            result = savefileName.find('/')
            savefileName=savefileName[(result-1)::-1]

            print(savefileName)
            savecheck=1
            print("Save Check Value ",savecheck)
            print("Open Check Value ",opencheck)
            
            if (opencheck==1 and savecheck==1):
                print("Inside the loop")

                db.insert({'Upload': uploadfileName, 'Saved': savefileName, 'Date' : x.strftime("%x"), 'Time' : x.strftime("%X")})

                uploadarray.append(uploadfileName)
                savearray.append(savefileName)
                datearray.append( x.strftime("%x"))
                timearray.append(x.strftime("%X"))

                # time.sleep(1)

                # opencheck=0
                # savecheck=0

                # print ("Opencheck value : ",opencheck )
                # print ("Savecheck value : ",savecheck)

        except:

            QMessageBox.about(MainWindow, "Failed to Detect Pdf File", "No Pdf File was Selected")

        # savecheck=1
        # print("Save check value ",savecheck)

        # if (opencheck==1 and savecheck==1):
        #     print("Inside the loop")

        #     db.insert({'Upload': fileName, 'Saved': savefileName, 'Date' : x.strftime("%x"), 'Time' : x.strftime("%X")})
        #     # opencheck=0
        #     # savecheck=0
        #     uploadarray.append(fileName)
        #     savearray.append(savefileName)
        #     datearray.append( x.strftime("%x"))
        #     timearray.append(x.strftime("%X"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
