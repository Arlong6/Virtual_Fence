# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_video = QtWidgets.QLabel(self.centralwidget)
        self.label_video.setGeometry(QtCore.QRect(100, 296, 688, 401))
        self.label_video.setObjectName("label_video")
        self.pushButton_camera = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_camera.setGeometry(QtCore.QRect(1090, 590, 111, 31))
        self.pushButton_camera.setObjectName("pushButton_camera")
        self.pushButton_drawfence = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_drawfence.setGeometry(QtCore.QRect(1090, 540, 111, 31))
        self.pushButton_drawfence.setObjectName("pushButton_drawfence")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(790, 400, 101, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(790, 450, 101, 21))
        self.label_5.setObjectName("label_5")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(1000, 400, 83, 16))
        self.radioButton.setObjectName("radioButton")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(900, 400, 83, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.buttonGroup.addButton(self.radioButton_2)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(890, 440, 181, 31))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_scan = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_scan.setGeometry(QtCore.QRect(1090, 440, 111, 31))
        self.pushButton_scan.setObjectName("pushButton_scan")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(1090, 490, 111, 31))
        self.pushButton_start.setObjectName("pushButton_start")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 40, 1104, 250))
        self.label.setObjectName("label")
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(900, 550, 101, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(820, 550, 71, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(810, 600, 101, 21))
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(830, 600, 101, 21))
        self.label_9.setObjectName("label_9")
        self.pushButton_logout = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_logout.setGeometry(QtCore.QRect(900, 640, 111, 31))
        self.pushButton_logout.setObjectName("pushButton_logout")
        self.pushButton_leave = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_leave.setGeometry(QtCore.QRect(1090, 640, 111, 31))
        self.pushButton_leave.setObjectName("pushButton_leave")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(790, 300, 431, 91))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1080, 290, 121, 101))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.label_4.setBuddy(self.radioButton)
        self.label_5.setBuddy(self.pushButton_scan)
        self.label_6.setBuddy(self.radioButton)
        self.label_7.setBuddy(self.radioButton)
        self.label_9.setBuddy(self.radioButton)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton_camera, self.pushButton_drawfence)
        MainWindow.setTabOrder(self.pushButton_drawfence, self.radioButton)
        MainWindow.setTabOrder(self.radioButton, self.radioButton_2)
        MainWindow.setTabOrder(self.radioButton_2, self.textEdit)
        MainWindow.setTabOrder(self.textEdit, self.pushButton_scan)
        MainWindow.setTabOrder(self.pushButton_scan, self.pushButton_start)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_video.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_camera.setText(_translate("MainWindow", "調閱影像"))
        self.pushButton_drawfence.setText(_translate("MainWindow", "繪製圍籬"))
        self.label_4.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:28pt;\">智慧型海上箱網防盜系統</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">輸入影像模式：<br/></span></p></body></html>"))
        self.label_5.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:28pt;\">智慧型海上箱網防盜系統</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">輸入影像路徑：</span></p><p align=\"center\"><br/></p><p align=\"center\"><span style=\" font-size:10pt;\"><br/></span></p></body></html>"))
        self.radioButton.setText(_translate("MainWindow", "輸入影像"))
        self.radioButton_2.setText(_translate("MainWindow", "即時影像"))
        self.pushButton_scan.setText(_translate("MainWindow", "瀏覽"))
        self.pushButton_start.setText(_translate("MainWindow", "開始"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.radioButton_3.setText(_translate("MainWindow", "啟用圍籬"))
        self.label_6.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:28pt;\">智慧型海上箱網防盜系統</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">警戒功能：</span></p></body></html>"))
        self.label_7.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:28pt;\">智慧型海上箱網防盜系統</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">調閱</span></p></body></html>"))
        self.label_9.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:28pt;\">智慧型海上箱網防盜系統</span></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">：<br/></span></p></body></html>"))
        self.pushButton_logout.setText(_translate("MainWindow", "登出"))
        self.pushButton_leave.setText(_translate("MainWindow", "離開"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
