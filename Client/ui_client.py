# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_client(object):
    def setupUi(self, client):
        client.setObjectName("client")
        client.resize(769, 551)
        font = QtGui.QFont()
        font.setFamily("Arial")
        client.setFont(font)
        client.setStyleSheet("QWidget{\n"
"background:#696969;\n"
"}\n"
"QAbstractButton{\n"
"border-style:none;\n"
"border-radius:0px;\n"
"padding:5px;\n"
"color:#DCDCDC;\n"
"background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #858585,stop:1 #383838);\n"
"}\n"
"QAbstractButton:hover{\n"
"color:#000000;\n"
"background-color:#008aff;\n"
"}\n"
"QAbstractButton:pressed{\n"
"color:#DCDCDC;\n"
"border-style:solid;\n"
"border-width:0px 0px 0px 4px;\n"
"padding:4px 4px 4px 2px;\n"
"border-color:#008aff;\n"
"background-color:#444444;\n"
"}\n"
"\n"
"QLabel{\n"
"color:#DCDCDC;\n"
"\n"
"\n"
"}\n"
"QLabel:focus{\n"
"border:1px solid #00BB9E;\n"
"\n"
"}\n"
"\n"
"QLineEdit{\n"
"border:1px solid #242424;\n"
"border-radius:3px;\n"
"padding:2px;\n"
"background:none;\n"
"selection-background-color:#484848;\n"
"selection-color:#DCDCDC;\n"
"}\n"
"QLineEdit:focus,QLineEdit:hover{\n"
"border:1px solid #242424;\n"
"}\n"
"QLineEdit{\n"
"border:1px solid #242424;\n"
"border-radius:3px;\n"
"padding:2px;\n"
"background:none;\n"
"selection-background-color:#484848;\n"
"selection-color:#DCDCDC;\n"
"}\n"
"\n"
"QLineEdit:focus,QLineEdit:hover{\n"
"border:1px solid #242424;\n"
"}\n"
"QLineEdit{\n"
"lineedit-password-character:9679;\n"
"}\n"
"QSlider::groove:horizontal,QSlider::add-page:horizontal{\n"
"height:3px;\n"
"border-radius:3px;\n"
"background:#18181a;\n"
"}\n"
"\n"
"\n"
"QSlider::sub-page:horizontal{\n"
"height:8px;\n"
"border-radius:3px;\n"
"background:#008aff;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal{\n"
"width:12px;\n"
"margin-top:-5px;\n"
"margin-bottom:-4px;\n"
"border-radius:6px;\n"
"background:qradialgradient(spread:pad,cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0.6 #DCDCDC,stop:0.8 #DCDCDC);\n"
"}\n"
"QSlider::groove:vertical,QSlider::sub-page:vertical{\n"
"width:3px;\n"
"border-radius:3px;\n"
"background:#18181a;\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:vertical{\n"
"width:8px;\n"
"border-radius:3px;\n"
"background:#008aff;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:vertical{\n"
"height:12px;\n"
"margin-left:-5px;\n"
"margin-right:-4px;\n"
"border-radius:6px;\n"
"background:qradialgradient(spread:pad,cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0.6 #DCDCDC,stop:0.8 #DCDCDC);\n"
"}\n"
"\n"
"QProgressBar {\n"
"border: 2px solid grey;\n"
"border-radius: 5px;\n"
"background-color: #FFFFFF;\n"
"}\n"
"QProgressBar::chunk {\n"
"background-color:#26fa03;\n"
"width: 20px;\n"
"}\n"
"QProgressBar {\n"
"text-align: center; \n"
"color: rgb(0,0,0);\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"pading:2px;\n"
"color:white;\n"
"subcontrol-position: top center;\n"
"border-top:0px ;\n"
"background:  transparent;} ")
        client.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.Video = QtWidgets.QLabel(client)
        self.Video.setGeometry(QtCore.QRect(300, 200, 400, 300))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Video.setFont(font)
        self.Video.setStyleSheet("font: 10pt \"Arial\";")
        self.Video.setText("")
        self.Video.setObjectName("Video")
        self.Button_Mapping = QtWidgets.QPushButton(client)
        self.Button_Mapping.setGeometry(QtCore.QRect(100, 400, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Lato")
        self.Button_Mapping.setFont(font)
        self.Button_Mapping.setStyleSheet("font: 11pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Mapping.setObjectName("Button_Mapping")
        self.Button_Cnn = QtWidgets.QPushButton(client)
        self.Button_Cnn.setGeometry(QtCore.QRect(200, 400, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Lato")
        self.Button_Cnn.setFont(font)
        self.Button_Cnn.setStyleSheet("font: 11pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Cnn.setObjectName("Button_cnn")
        self.Button_Left = QtWidgets.QPushButton(client)
        self.Button_Left.setGeometry(QtCore.QRect(360, 120, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Lato")
        self.Button_Left.setFont(font)
        self.Button_Left.setStyleSheet("font: 11pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Left.setObjectName("Button_Left")
        self.Label_Manuel = QtWidgets.QLabel(client)
        self.Label_Manuel.setGeometry(QtCore.QRect(440, 5, 220, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Label_Manuel.setFont(font)
        self.Label_Manuel.setStyleSheet("font: 15pt; color: #000000;")
        self.Label_Manuel.setObjectName("Manual_Label")
        self.Button_ForWard = QtWidgets.QPushButton(client)
        self.Button_ForWard.setGeometry(QtCore.QRect(480, 50, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_ForWard.setFont(font)
        self.Button_ForWard.setStyleSheet("font: 11pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_ForWard.setObjectName("Button_ForWard")
        self.Button_Right = QtWidgets.QPushButton(client)
        self.Button_Right.setGeometry(QtCore.QRect(600, 120, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Right.setFont(font)
        self.Button_Right.setStyleSheet("font: 11pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Right.setObjectName("Button_Right")
        self.Button_BackWard = QtWidgets.QPushButton(client)
        self.Button_BackWard.setGeometry(QtCore.QRect(480, 140, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_BackWard.setFont(font)
        self.Button_BackWard.setStyleSheet("font: 11pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_BackWard.setObjectName("Button_BackWard")
        
        self.lineEdit_IP_Adress = QtWidgets.QLineEdit(client)
        self.lineEdit_IP_Adress.setGeometry(QtCore.QRect(10, 150, 130, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.lineEdit_IP_Adress.setFont(font)
        self.lineEdit_IP_Adress.setStyleSheet("font: 12pt \"Arial\";")
        self.lineEdit_IP_Adress.setObjectName("lineEdit_IP_Adress")
        self.Button_Step_Left = QtWidgets.QPushButton(client)
        self.Button_Step_Left.setGeometry(QtCore.QRect(360, 70, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Step_Left.setFont(font)
        self.Button_Step_Left.setStyleSheet("font: 11pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Step_Left.setObjectName("Button_Step_Left")
        self.Button_Step_Right = QtWidgets.QPushButton(client)
        self.Button_Step_Right.setGeometry(QtCore.QRect(600, 70, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Step_Right.setFont(font)
        self.Button_Step_Right.setStyleSheet("font: 11pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Step_Right.setObjectName("Button_Step_Right")
        self.Button_Connect = QtWidgets.QPushButton(client)
        self.Button_Connect.setGeometry(QtCore.QRect(150, 145, 90, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Connect.setFont(font)
        self.Button_Connect.setStyleSheet("font: 10pt; border: 2px solid black; background-color: #696969;")
        self.Button_Connect.setObjectName("Button_Connect")
        
        
        
        
        self.Button_Calibration = QtWidgets.QPushButton(client)
        self.Button_Calibration.setGeometry(QtCore.QRect(45, 510, 90, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.Button_Calibration.setFont(font)
        self.Button_Calibration.setStyleSheet("font: 10pt \"Arial\";")
        self.Button_Calibration.setObjectName("Button_Calibration")
        self.Button_Otonom = QtWidgets.QPushButton(client)
        self.Button_Otonom.setGeometry(QtCore.QRect(10, 200, 120, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.Button_Otonom.setFont(font)
        self.Button_Otonom.setStyleSheet("font: 13pt \"Arial\"; background-color: #363636; border: 2px solid black")
        self.Button_Otonom.setObjectName("Button_Otonom")
        self.Button_Manuel = QtWidgets.QPushButton(client)
        self.Button_Manuel.setGeometry(QtCore.QRect(140, 200, 120, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.Button_Manuel.setFont(font)
        self.Button_Manuel.setStyleSheet("font: 13pt \"Arial\"; background-color: #363636; border: 2px solid black")
        self.Button_Manuel.setObjectName("Button_Manuel")
        self.Button_Sonic = QtWidgets.QPushButton(client)
        self.Button_Sonic.setGeometry(QtCore.QRect(555, 510, 90, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Sonic.setFont(font)
        self.Button_Sonic.setStyleSheet("font: 10pt \"Arial\";")
        self.Button_Sonic.setObjectName("Button_Sonic")
        
       
        self.label_speed = QtWidgets.QLabel(client)
        self.label_speed.setGeometry(QtCore.QRect(715, 175, 35, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_speed.setFont(font)
        self.label_speed.setStyleSheet("font: 10pt \"Arial\";")
        self.label_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_speed.setObjectName("label_speed")
        self.slider_speed = QtWidgets.QSlider(client)
        self.slider_speed.setGeometry(QtCore.QRect(720, 50, 22, 125))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.slider_speed.setFont(font)
        self.slider_speed.setStyleSheet("font: 10pt \"Arial\";")
        self.slider_speed.setOrientation(QtCore.Qt.Vertical)
        self.slider_speed.setObjectName("slider_speed")
        
        
        
        self.progress_Power = QtWidgets.QProgressBar(client)
        self.progress_Power.setEnabled(False)
        self.progress_Power.setGeometry(QtCore.QRect(60, 80, 130, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.progress_Power.setFont(font)
        self.progress_Power.setStyleSheet("font: 12pt \"Arial\";")
        self.progress_Power.setProperty("value", 24)
        self.progress_Power.setObjectName("progress_Power")
        
        '''
        self.label_sonic = QtWidgets.QLabel(client)
        self.label_sonic.setGeometry(QtCore.QRect(540, 470, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_sonic.setFont(font)
        .setStyleSheet("font: 10pt \"Arial\";")
        self.label_sonic.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sonic.setObjectName("label_sonic")
        '''
        self.Button_Relax = QtWidgets.QPushButton(client)
        self.Button_Relax.setGeometry(QtCore.QRect(440, 510, 90, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Relax.setFont(font)
        self.Button_Relax.setStyleSheet("font: 10pt \"Arial\";")
        self.Button_Relax.setObjectName("Button_Relax")
        self.retranslateUi(client)
        QtCore.QMetaObject.connectSlotsByName(client)

    def retranslateUi(self, client):
        _translate = QtCore.QCoreApplication.translate
        client.setWindowTitle(_translate("client", "Robot Dog Client Group 3"))
        self.Button_Left.setText(_translate("client", "Turn Left"))
        self.Button_ForWard.setText(_translate("client", "ForWard"))
        self.Button_Right.setText(_translate("client", "Turn Right"))
        self.Button_BackWard.setText(_translate("client", "BackWard"))
        self.lineEdit_IP_Adress.setText(_translate("client", "0"))
        self.Button_Step_Left.setText(_translate("client", "Step Left"))
        self.Button_Step_Right.setText(_translate("client", "Step Right"))
        self.Button_Connect.setText(_translate("client", "Connect"))
        self.Button_Calibration.setText(_translate("client", "Calibration"))
        self.Button_Otonom.setText(_translate("client", "Autonomous"))
        self.Button_Manuel.setText(_translate("client", "Manual"))
        self.Button_Sonic.setText(_translate("client", "Sonic"))
        self.label_speed.setText(_translate("client", "8"))
        self.Label_Manuel.setText(_translate("client", "MANUAL CONTROL"))
        self.Button_Mapping.setText(_translate("client", "Mapping"))
        #self.label_sonic.setText(_translate("client", "Obstacle:0cm"))
        self.Button_Relax.setText(_translate("client", "Relax"))
        self.Button_Cnn.setText(_translate("client", "Cnn"))
