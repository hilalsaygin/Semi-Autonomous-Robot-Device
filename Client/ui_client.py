# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import threading
from ctypes import c_int, c_double
from queue import Queue
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget , QPushButton , QLabel , QVBoxLayout , QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint , QThread, pyqtSignal , QMutex , pyqtSlot , QMutexLocker
import math



class DataReceiverThread(QThread):

    def __init__(self, points ,robot_x ,robot_y, robot_angle):
        super().__init__()
        self.points = points
        self.mutex = QMutex()
        self.robot_x = robot_x
        self.robot_y = robot_y
        self.robot_angle = robot_angle
        self.ipAddress = "192.168.137.25"
        self.remote_port = 8250
        print("girdi3")

    def run(self):
        # Open socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Set server
            server_address = (self.ipAddress, self.remote_port)
            sock.connect(server_address)
            print("Bağlandı")
            
            # Define separate buffer for robot location bytes
            robot_location_bytes = bytearray(24)

            while True:
                # Değerleri sıfırla
                point_x_d = -1
                point_y_d = -1
                robot_location_buffer = (c_double * 3)()

                # Point sayısını al
                point_count = 0
                point_count_bytes = sock.recv(4)
                if not point_count_bytes:
                    print("Failed to receive data")
                    sock.close()
                    point_count = 0
                else:
                    point_count = int.from_bytes(point_count_bytes, byteorder='little')

                #print("point count " , point_count)

                # Eğer point sayısı valid ise
                if 0 < point_count < 20000:
                    # Robot konumunu al
                    bytesRead = sock.recv_into(robot_location_bytes)
                    if not bytesRead:
                        print("Failed to receive data")
                        sock.close()
                    else:
                        
                        robot_location_buffer = (c_double * 3).from_buffer(robot_location_bytes)
                        print(robot_location_bytes)
                        self.robot_x = float(robot_location_buffer[0])
                        self.robot_y = float(robot_location_buffer[1])
                        
                        self.robot_angle = float(robot_location_buffer[2])
                        #print("robot x : " , self.robot_x)
                        #print("robot_y : " , self.robot_y)
                        #print("robot_angle : " , robot_location_buffer[2])
                        robot_location_buffer[:] = (c_double * 3)()
                        

                    # Pointleri al
                    if robot_location_bytes:
                        point_buffer = (c_double * (point_count * 2))()

                        bytesRead = sock.recv_into(point_buffer, 8 * point_count * 2)
                        if not bytesRead:
                            print("Failed to receive data")
                            sock.close()
                        else:
                            for i in range(point_count):
                                point = (point_buffer[i * 2], point_buffer[i * 2 + 1])
                                with QMutexLocker(self.mutex):

                                    # Point'in döndürülme açısını biliyoruz , ve onu döndürülmeden önceki haline çeviriyoruz
                                    # böylece map dönmeden etkilenmiyor.
                                    """
                                    radyan = math.radians(self.robot_angle)
                                    x = float(point[0]) * math.cos(-radyan) - float(point[1] * math.sin(-radyan))
                                    y = float(point[0]) * math.sin(-radyan) + float(point[1] * math.cos(-radyan))"""

                                    # Pointi robot konumunu da dahil ederek ekle
                                    self.points.append([(point[0] + self.robot_x), (point[1] + self.robot_y)])
                                    
                                    #  print("Point x : " , float(point[0]) + self.robot_x, "Point y : " , float(point[1]) + self.robot_y)

                            with QMutexLocker(self.mutex):
                                while len(self.points) > 60000:
                                    self.points.pop(0)
                            
        finally:
            print("çıktı")
            sock.close()

class MapWidget(QWidget):
    camera_x = 0
    camera_y = 0
    robot_x = 0
    robot_y = 0
    robot_angle = 0
    zoom = 45

    def __init__(self,points,robot_x,robot_y,robot_angle , clicked_coordinate_label):
        super().__init__()
        print("girdi2")
        self.points = points
        self.robot_x = robot_x
        self.robot_y = robot_y
        self.robot_angle = robot_angle
        
        self.clicked_coordinate_label = clicked_coordinate_label
        
    def paintEvent(self, event):
        #print(self.points)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Ekranı temizle
        painter.eraseRect(self.rect())

        # Pointleri çiz
        for point in self.points:
            painter.setPen(QPen(Qt.red, 3))
            painter.drawPoint(QPoint(int((point[0] * self.zoom) + self.camera_x), int((point[1] * self.zoom) + self.camera_y)))

        # Robotu çiz
        painter.setPen(QPen(Qt.green, self.zoom / 10))
        painter.drawPoint(QPoint(int((self.robot_x * self.zoom) + self.camera_x), int((self.robot_y * self.zoom) + self.camera_y)))
        #print("robot_x : ",self.robot_x , "\n")
        #print("robot_y : ",self.robot_y , "\n")
    
    # Mouse tıklandığında koordinatı yaz
    def mouseReleaseEvent(self,event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            relative_pos = self.mapFromGlobal(pos)
            clicked_x = (relative_pos.x() - self.camera_x) / self.zoom
            clicked_y = (relative_pos.y() - self.camera_y) / self.zoom
            self.clicked_coordinate_label.setText("Clicked Coordinates \nX : " + str(format(clicked_x,".2f")) + " Y : " + str(format(clicked_y,".2f")))
            self.clicked_coordinate_label.update()
            self.send_move_instruction(clicked_x, clicked_y)
            print("Clicked Coordinates \nX : " + str(format(clicked_x,".2f")) + " Y : " + str(format(clicked_y,".2f")) )
    
    # TODO
    # Tıklanan yerin ve robotun konumu kullanılarak gidilecek yön ve mesafe hesaplanıp,
    # robota hareket instruction u gönderilecek
    def send_move_instruction(self,clicked_x,clicked_y):
        pass

class MapMainWindow(QWidget):

    def __init__(self , client):
        super().__init__(client)
        self.points = []
        self.robot_x = 0
        self.robot_y = 0
        self.robot_angle = 0
        
        # Set the background color using a CSS style
        self.setStyleSheet("background-color: black;")

        main_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()

        self.setLayout(main_layout)

        self.clicked_coordinate_label = QLabel("",self)
        self.mapping_widget = MapWidget(self.points ,self.robot_x , self.robot_y , self.robot_angle , self.clicked_coordinate_label)
        
        self.init_data()
        self.update_timer = self.startTimer(int(1000 / 5))  # Update every second

        space = 30

        main_layout.addLayout(buttons_layout , stretch = 1)
        main_layout.addWidget(self.mapping_widget , stretch = 7)
        self.zoom_in_button = QPushButton("Zoom In", self)
        self.zoom_in_button.move(10, 10)
        self.zoom_in_button.setStyleSheet("font: 14pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        buttons_layout.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton("Zoom Out", self)
        self.zoom_out_button.move(10, 40)
        self.zoom_out_button.setStyleSheet("font: 14pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        buttons_layout.addWidget(self.zoom_out_button)

        self.camera_left_button = QPushButton("Camera Left", self)
        self.camera_left_button.move(10, 70 + space)
        self.camera_left_button.setStyleSheet("font: 14pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.camera_left_button.clicked.connect(self.camera_left)
        buttons_layout.addWidget(self.camera_left_button)

        self.camera_right_button = QPushButton("Camera Right", self)
        self.camera_right_button.move(10, 100 + space)
        self.camera_right_button.setStyleSheet("font: 14pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.camera_right_button.clicked.connect(self.camera_right)
        buttons_layout.addWidget(self.camera_right_button)

        self.camera_up_button = QPushButton("Camera Up", self)
        self.camera_up_button.move(10, 130 + space)
        self.camera_up_button.setStyleSheet("font: 14pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.camera_up_button.clicked.connect(self.camera_up)
        buttons_layout.addWidget(self.camera_up_button)

        self.camera_down_button = QPushButton("Camera Down", self)
        self.camera_down_button.move(10, 160 + space)
        self.camera_down_button.setStyleSheet("font: 14pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.camera_down_button.clicked.connect(self.camera_down)
        buttons_layout.addWidget(self.camera_down_button)

        self.clear_map_button = QPushButton("Clear", self)
        self.clear_map_button.move(10, 210 + space)
        self.clear_map_button.setStyleSheet("font: 14pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.clear_map_button.clicked.connect(self.clear_map)
        buttons_layout.addWidget(self.clear_map_button)

        self.clicked_coordinate_label.move(10,240 + space)
        self.clicked_coordinate_label.setStyleSheet("font: 14pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        buttons_layout.addWidget(self.clicked_coordinate_label)

    def init_data(self):
        self.receiver_thread = DataReceiverThread(self.points,self.robot_x,self.robot_y,self.robot_angle)
        self.receiver_thread.start()

    def update(self):
        # Update data and repaint the widget
        self.mapping_widget.update()
    
    def timerEvent(self, event):
        if event.timerId() == self.update_timer:
            self.update()
        else:
            super().timerEvent(event)
    
    def zoom_in(self):
        print("zoom in")
        self.mapping_widget.zoom += 5
        
    def zoom_out(self):
        if MapWidget.zoom > 5:
            self.mapping_widget.zoom -= 5
    
    def camera_left(self):
        self.mapping_widget.camera_x += 100
        
    def camera_right(self):
        self.mapping_widget.camera_x -= 100
    
    def camera_up(self):
        self.mapping_widget.camera_y += 100
    
    def camera_down(self):
        self.mapping_widget.camera_y -= 100
    
    def clear_map(self):
        with QMutexLocker(self.receiver_thread.mutex):
            self.points.clear()

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Add widgets and layout here
        layout = QVBoxLayout()
        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def setLabelText(self, text):
        self.label.setText(text)

# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_client(object):
    def setupUi(self, client):
        client.setObjectName("client")
        client.resize(1920, 1080)
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
"width:5px;\n"
"height:175px;\n"
"border-radius:15px;\n"
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
"height:15px;\n"
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
        """
        self.Video = QtWidgets.QLabel(client)
        self.Video.setGeometry(QtCore.QRect(300, 200, 400, 300))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Video.setFont(font)
        self.Video.setStyleSheet("font: 10pt \"Arial\";")
        self.Video.setText("")
        self.Video.setObjectName("Video")
        """
        self.mappingWidget = MapMainWindow(client)
        self.mappingWidget.setGeometry(QtCore.QRect(0, 350, 1000, 600))
        self.mappingWidget.setObjectName("MappingWidget")
        self.Button_Left = QtWidgets.QPushButton(client)
        self.Button_Left.setGeometry(QtCore.QRect(830, 250, 140, 50))
        font = QtGui.QFont()
        font.setFamily("Lato")
        self.Button_Left.setFont(font)
        self.Button_Left.setStyleSheet("font: 20pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Left.setObjectName("Button_Left")
        self.Label_Manuel = QtWidgets.QLabel(client)
        self.Label_Manuel.setGeometry(QtCore.QRect(870, 60, 420, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Label_Manuel.setFont(font)
        self.Label_Manuel.setStyleSheet("font: 31pt; color: #000000;")
        self.Label_Manuel.setObjectName("Manual_Label")
        self.Label_Speed = QtWidgets.QLabel(client)
        self.Label_Speed.setGeometry(QtCore.QRect(1698, 40, 420, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Label_Speed.setFont(font)
        self.Label_Speed.setStyleSheet("font: 15pt; color: #000000;")
        self.Label_Speed.setObjectName("Speed_Label")
        self.Label_Sonic = QtWidgets.QLabel(client)
        self.Label_Sonic.setGeometry(QtCore.QRect(1480, 40, 220, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Label_Sonic.setFont(font)
        self.Label_Sonic.setStyleSheet("font: 15pt; color: #000000;")
        self.Label_Sonic.setObjectName("Sonic_Label")
        
        self.Button_ForWard = QtWidgets.QPushButton(client)
        self.Button_ForWard.setGeometry(QtCore.QRect(990, 140, 140, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_ForWard.setFont(font)
        self.Button_ForWard.setStyleSheet("font: 20pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_ForWard.setObjectName("Button_ForWard")
        self.Button_Right = QtWidgets.QPushButton(client)
        self.Button_Right.setGeometry(QtCore.QRect(1150, 250, 140, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Right.setFont(font)
        self.Button_Right.setStyleSheet("font: 20pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Right.setObjectName("Button_Right")
        self.Button_BackWard = QtWidgets.QPushButton(client)
        self.Button_BackWard.setGeometry(QtCore.QRect(990, 280, 140, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_BackWard.setFont(font)
        self.Button_BackWard.setStyleSheet("font: 20pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_BackWard.setObjectName("Button_BackWard")
        
        self.lineEdit_IP_Adress = QtWidgets.QLineEdit(client)
        self.lineEdit_IP_Adress.setGeometry(QtCore.QRect(100, 160, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.lineEdit_IP_Adress.setFont(font)
        self.lineEdit_IP_Adress.setStyleSheet("font: 20pt \"Arial\";")
        self.lineEdit_IP_Adress.setObjectName("lineEdit_IP_Adress")
        self.Button_Step_Left = QtWidgets.QPushButton(client)
        self.Button_Step_Left.setGeometry(QtCore.QRect(830, 170, 140, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Step_Left.setFont(font)
        self.Button_Step_Left.setStyleSheet("font: 20pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Step_Left.setObjectName("Button_Step_Left")
        self.Button_Step_Right = QtWidgets.QPushButton(client)
        self.Button_Step_Right.setGeometry(QtCore.QRect(1150, 170, 140, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Step_Right.setFont(font)
        self.Button_Step_Right.setStyleSheet("font: 20pt; border: 2px solid white; background-color: #696969; border-radius: 5px")
        self.Button_Step_Right.setObjectName("Button_Step_Right")
        self.Button_Connect = QtWidgets.QPushButton(client)
        self.Button_Connect.setGeometry(QtCore.QRect(360, 155, 130, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Connect.setFont(font)
        self.Button_Connect.setStyleSheet("font: 20pt; border: 2px solid black; background-color: #696969;")
        self.Button_Connect.setObjectName("Button_Connect")
        
        
        
        
        self.Button_Calibration = QtWidgets.QPushButton(client)
        self.Button_Calibration.setGeometry(QtCore.QRect(45, 960, 90, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.Button_Calibration.setFont(font)
        self.Button_Calibration.setStyleSheet("font: 10pt \"Arial\";")
        self.Button_Calibration.setObjectName("Button_Calibration")
        self.Button_Otonom = QtWidgets.QPushButton(client)
        self.Button_Otonom.setGeometry(QtCore.QRect(100, 260, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.Button_Otonom.setFont(font)
        self.Button_Otonom.setStyleSheet("font: 22pt \"Arial\"; background-color: #363636; border: 2px solid black")
        self.Button_Otonom.setObjectName("Button_Otonom")
        self.Button_Manuel = QtWidgets.QPushButton(client)
        self.Button_Manuel.setGeometry(QtCore.QRect(320, 260, 120, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.Button_Manuel.setFont(font)
        self.Button_Manuel.setStyleSheet("font: 20pt \"Arial\"; background-color: #363636; border: 2px solid black")
        self.Button_Manuel.setObjectName("Button_Manuel")
        self.Button_Sonic = QtWidgets.QPushButton(client)
        self.Button_Sonic.setGeometry(QtCore.QRect(1450, 80, 120, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Sonic.setFont(font)
        self.Button_Sonic.setStyleSheet("font: 20pt \"Arial\"; background-color: #363636; border: 2px solid black")
        self.Button_Sonic.setObjectName("Button_Sonic")
        
       
        self.label_speed = QtWidgets.QLabel(client)
        self.label_speed.setGeometry(QtCore.QRect(1714, 260, 35, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_speed.setFont(font)
        self.label_speed.setStyleSheet("font: 15pt \"Arial\";")
        self.label_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_speed.setObjectName("label_speed")
        self.slider_speed = QtWidgets.QSlider(client)
        self.slider_speed.setGeometry(QtCore.QRect(1720, 80, 22, 175))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.slider_speed.setFont(font)
        self.slider_speed.setOrientation(QtCore.Qt.Vertical)
        self.slider_speed.setObjectName("slider_speed")
        
        
        
        self.progress_Power = QtWidgets.QProgressBar(client)
        self.progress_Power.setEnabled(False)
        self.progress_Power.setGeometry(QtCore.QRect(150, 60, 220, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.progress_Power.setFont(font)
        self.progress_Power.setStyleSheet("font: 20pt \"Arial\";")
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
        '''
        self.Button_Relax = QtWidgets.QPushButton(client)
        self.Button_Relax.setGeometry(QtCore.QRect(440, 510, 90, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Button_Relax.setFont(font)
        self.Button_Relax.setStyleSheet("font: 10pt \"Arial\";")
        self.Button_Relax.setObjectName("Button_Relax")
        '''
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
        self.Button_Sonic.setText(_translate("client", ""))
        self.label_speed.setText(_translate("client", "8"))
        self.Label_Manuel.setText(_translate("client", "MANUAL CONTROL"))
        self.Label_Speed.setText(_translate("client", "SPEED"))
        self.Label_Sonic.setText(_translate("client", "SONİC"))
        #self.label_sonic.setText(_translate("client", "Obstacle:0cm"))
        #self.Button_Relax.setText(_translate("client", "Relax"))
