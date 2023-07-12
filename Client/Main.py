# -*- coding: utf-8 -*-
import sys
import os
from ui_led import Ui_led
from ui_face import Ui_Face
from ui_client import Ui_client
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Client import *
from Calibration import *
#import CnnModelTest
import multiprocessing

class MyWindow(QMainWindow,Ui_client):
    def __init__(self):
        super(MyWindow,self).__init__()
        
        self.setupUi(self)
        #self.Video.setScaledContents (True)
        #self.Video.setPixmap(QPixmap('Picture/dog_client.png'))
        self.timer=QTimer(self)
        #self.timer.timeout.connect(self.refresh_image)
        self.timer.start(10)

        self.setFocusPolicy(Qt.StrongFocus)
        
        self.client=Client()
        self.client.move_speed=str(self.slider_speed.value())
        file = open('IP.txt', 'r')
        self.lineEdit_IP_Adress.setText(str(file.readline()))
        file.close()

        #ProgressBar
        self.progress_Power.setMinimum(0)
        self.progress_Power.setMaximum(100)
        self.progress_Power.setValue(90)
        
        #Button click event
        self.Button_Connect.clicked.connect(self.connect)
        self.Button_Calibration.clicked.connect(self.showCalibrationWindow)
        self.Button_Otonom.clicked.connect(self.otonom)
        self.Button_Manuel.clicked.connect(self.manuel)

        self.Button_Sonic.clicked.connect(self.sonic)
        self.Button_Relax.clicked.connect(self.relax)
        
        self.Button_ForWard.pressed.connect(self.forward)
        self.Button_ForWard.released.connect(self.stop)
        self.Button_BackWard.pressed.connect(self.backward)
        self.Button_BackWard.released.connect(self.stop)
        self.Button_Left.pressed.connect(self.left)
        self.Button_Left.released.connect(self.stop)
        self.Button_Right.pressed.connect(self.right)
        self.Button_Right.released.connect(self.stop)
        self.Button_Step_Left.pressed.connect(self.step_left)
        self.Button_Step_Left.released.connect(self.stop)
        self.Button_Step_Right.pressed.connect(self.step_right)
        self.Button_Step_Right.released.connect(self.stop)
        
        self.slider_speed.setMinimum(2)
        self.slider_speed.setMaximum(10)
        self.slider_speed.setSingleStep(1)
        self.slider_speed.setValue(8)
        self.slider_speed.valueChanged.connect(self.speed)
        self.client.move_speed=str(self.slider_speed.value())

        #Timer
        
        self.timer_power = QTimer(self)
        self.timer_power.timeout.connect(self.power)

        self.timer_sonic = QTimer(self)
        self.timer_sonic.timeout.connect(self.getSonicData)

        self.drawpoint=[585,135]
        self.initial=True
    
    def video(self):
        self.timer.start(10)
    def closeEvent(self,event):
        try:
            self.timer_power.stop()
            self.timer.stop()
            stop_thread(self.video)
            stop_thread(self.instruction)
        except Exception as e:
            print(e)
        self.client.turn_off_client()
        print("close")
        QCoreApplication.instance().quit()
        #os._exit(0)

    

    def receive_instruction(self,ip):
        try:
            self.client.client_socket1.connect((ip,5001))
            self.client.tcp_flag=True
            print ("Connecttion Successful !")
        except Exception as e:
            print ("Connect to server Faild!: Server IP is right? Server is opend?")
            self.client.tcp_flag=False
        while True:
            try:
                alldata=self.client.receive_data()
            except:
                self.client.tcp_flag=False
                break
            #print(alldata)
            if alldata=='':
                break
            else:
                cmdArray=alldata.split('\n')
                #print(cmdArray)
                if cmdArray[-1] !="":
                    cmdArray==cmdArray[:-1]
            for oneCmd in cmdArray:
                data=oneCmd.split("#")
                #print(data)
                if data=="":
                    self.client.tcp_flag=False
                    break
                elif data[0]==cmd.CMD_SONIC:
                    self.Button_Sonic.setText(data[1]+'cm')
                    #self.label_sonic.setText('Obstacle:'+data[1]+'cm')
                    #print('Obstacle:',data[1])
                elif data[0]==cmd.CMD_POWER:
                    if data[1]!="":
                        power_value=round((float(data[1]) - 7.00) / 1.40 * 100)
                        self.progress_Power.setValue(power_value)
                elif data[0]==cmd.CMD_RELAX:
                    if data[1]=="0":
                        self.Button_Relax.setText('Relax')
                    else:
                        self.Button_Relax.setText('"Too tired..."')
    """
    def refresh_image(self):
        try:
            if self.client.video_flag == False:
                height, width, bytesPerComponent=self.client.image.shape
                #print (height, width, bytesPerComponent)
                cv2.cvtColor(self.client.image, cv2.COLOR_BGR2RGB, self.client.image)
                QImg = QImage(self.client.image.data, width, height, 3 * width, QImage.Format_RGB888)
                self.Video.setPixmap(QPixmap.fromImage(QImg))
                self.client.video_flag = True
        except Exception as e:
            print(e)
    """

    #CONNECT
    def connect(self):
        file=open('IP.txt','w')
        file.write(self.lineEdit_IP_Adress.text())
        file.close()
        if self.Button_Connect.text()=='Connect':
            self.IP = self.lineEdit_IP_Adress.text()
            self.client.turn_on_client(self.IP)
            self.video=threading.Thread(target=self.client.receiving_video,args=(self.IP,))
            self.instruction=threading.Thread(target=self.receive_instruction,args=(self.IP,))
            self.video.start() 
            self.instruction.start()
            self.Button_Connect.setText('Disconnect')
            self.timer_power.start(1000)
        else:
            try:
                stop_thread(self.video)
            except:
                pass
            try:
                stop_thread(self.instruction)
            except:
                pass
            self.client.tcp_flag=False
            self.client.turn_off_client()
            self.Button_Connect.setText('Connect')
            self.timer_power.stop()

    def stand(self):
        self.initial=False
        #self.drawpoint = [585, 135]
        self.Button_IMU.setText('Balance')
        self.slider_roll.setValue(0)
        time.sleep(0.1)
        self.slider_pitch.setValue(0)
        time.sleep(0.1)
        self.slider_yaw.setValue(0)
        time.sleep(0.1)
        self.slider_horizon.setValue(0)
        time.sleep(0.1)
        self.initial = True

    #MOVE
    def stop(self):
        command=cmd.CMD_MOVE_STOP+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        #print (command)
        
    def forward(self):
        #self.stand()
        command=cmd.CMD_MOVE_FORWARD+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        #print (command)

    def backward(self):
        #self.stand()
        command=cmd.CMD_MOVE_BACKWARD+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        #print (command)
        
    def step_left(self):
        #self.stand()
        command=cmd.CMD_MOVE_LEFT+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        #print (command)

    def step_right(self):
        #self.stand()
        command=cmd.CMD_MOVE_RIGHT+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        #print (command)
        
    def left(self):
        #self.stand()
        command=cmd.CMD_TURN_LEFT+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        #print (command)

    def right(self):
        #self.stand()
        command=cmd.CMD_TURN_RIGHT+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        #print (command)

    def speed(self):
        self.client.move_speed=str(self.slider_speed.value())
        self.label_speed.setText(str(self.slider_speed.value()))
    
  
    #relax
    def relax(self):
        if self.Button_Relax.text() == 'Relax':
            command=cmd.CMD_RELAX+'\n'
            self.client.send_data(command)
            #print (command)
        else:
            pass
   

    #SNOIC
    def sonic(self):
        if self.Button_Sonic.text() == 'Sonic':
            self.timer_sonic.start(100)
            self.Button_Sonic.setText('Close')

        else:
            self.timer_sonic.stop()
            self.Button_Sonic.setText('Sonic')
            #
    def getSonicData(self):
        command=cmd.CMD_SONIC+'\n'
        self.client.send_data(command)
        #print (command)
    #HEIGHT
    def height(self):
        try:
            hei=str(self.slider_height.value())
            self.label_height.setText(hei)
            command=cmd.CMD_HEIGHT+"#"+hei+'\n'
            self.client.send_data(command)
            #print(command)
        except Exception as e:
            print(e)

    #HORIZON
    def horizon(self):
        try:
            hor=str(self.slider_horizon.value())
            self.label_horizon.setText(hor)
            command=cmd.CMD_HORIZON+"#"+hor+'\n'
            if self.initial:
                self.client.send_data(command)
            #print(command)
        except Exception as e:
            print(e)

    #HEAD
    def head(self):
        try:
            angle=str(self.slider_head.value())
            self.label_head.setText(angle)
            command=cmd.CMD_HEAD+"#"+angle+'\n'
            self.client.send_data(command)
            #print(command)
        except Exception as e:
            print(e)

    #POWER
    def power(self):
        try:
            command=cmd.CMD_POWER+'\n'
            self.client.send_data(command)
            #print (command)
            command = "CMD_WORKING_TIME" + '\n'
            self.client.send_data(command)
        except Exception as e:
            print(e)
        
    def showCalibrationWindow(self):
        self.stop()
        self.calibrationWindow=calibrationWindow(self.client)
        self.calibrationWindow.setWindowModality(Qt.ApplicationModal)
        self.calibrationWindow.show()

    def otonom(self):
        #self.stand()
        command=cmd.CMD_OTO+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        command=cmd.CMD_MOVE_STOP+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        
    def manuel(self):
        #self.stand()
        command=cmd.CMD_MANUEL+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        command=cmd.CMD_MOVE_STOP+"#"+str(self.slider_speed.value())+'\n'
        self.client.send_data(command)
        
    #def cnn(self):
      #  CnnModelTest.start()

class faceWindow(QMainWindow,Ui_Face):
    def __init__(self,client):
        super(faceWindow,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('Picture/logo_Mini.png'))
        self.label_video.setScaledContents(True)
        self.label_video.setPixmap(QPixmap('Picture/dog_client.png'))
        self.Button_Read_Face.clicked.connect(self.readFace)
        self.client = client
        self.face_image=''
        self.photoCount=0
        self.timeout=0
        self.name = ''
        self.readFaceFlag=False
        # Timer
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.faceDetection)
        self.timer1.start(10)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.facePhoto)

    def closeEvent(self, event):
        self.timer1.stop()
        self.client.face_id = False
   

    
  
class calibrationWindow(QMainWindow,Ui_calibration):
    def __init__(self,client):
        super(calibrationWindow,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('Picture/logo_Mini.png'))
        self.label_picture.setScaledContents (True)
        self.label_picture.setPixmap(QPixmap('Picture/dog_calibration.png'))
        self.point=self.Read_from_txt('point')
        self.set_point(self.point)
        self.client=client
        self.leg='one'
        self.x=0
        self.y=0
        self.z=0
        self.radioButton_one.setChecked(True)
        self.radioButton_one.toggled.connect(lambda: self.leg_point(self.radioButton_one))
        self.radioButton_two.setChecked(False)
        self.radioButton_two.toggled.connect(lambda: self.leg_point(self.radioButton_two))
        self.radioButton_three.setChecked(False)
        self.radioButton_three.toggled.connect(lambda: self.leg_point(self.radioButton_three))
        self.radioButton_four.setChecked(False)
        self.radioButton_four.toggled.connect(lambda: self.leg_point(self.radioButton_four))
        self.Button_Save.clicked.connect(self.save)
        self.Button_X1.clicked.connect(self.X1)
        self.Button_X2.clicked.connect(self.X2)
        self.Button_Y1.clicked.connect(self.Y1)
        self.Button_Y2.clicked.connect(self.Y2)
        self.Button_Z1.clicked.connect(self.Z1)
        self.Button_Z2.clicked.connect(self.Z2)
    def X1(self):
        self.get_point()
        self.x +=1
        command=cmd.CMD_CALIBRATION+'#'+self.leg+'#'+str(self.x)+'#'+str(self.y)+'#'+str(self.z)+'\n'
        self.client.send_data(command)
        #print(command)
        self.set_point()
    def X2(self):
        self.get_point()
        self.x -= 1
        command=cmd.CMD_CALIBRATION+'#'+self.leg+'#'+str(self.x)+'#'+str(self.y)+'#'+str(self.z)+'\n'
        self.client.send_data(command)
        #print(command)
        self.set_point()
    def Y1(self):
        self.get_point()
        self.y += 1
        command=cmd.CMD_CALIBRATION+'#'+self.leg+'#'+str(self.x)+'#'+str(self.y)+'#'+str(self.z)+'\n'
        self.client.send_data(command)
        #print(command)
        self.set_point()
    def Y2(self):
        self.get_point()
        self.y -= 1
        command=cmd.CMD_CALIBRATION+'#'+self.leg+'#'+str(self.x)+'#'+str(self.y)+'#'+str(self.z)+'\n'
        self.client.send_data(command)
        #print(command)
        self.set_point()
    def Z1(self):
        self.get_point()
        self.z += 1
        command=cmd.CMD_CALIBRATION+'#'+self.leg+'#'+str(self.x)+'#'+str(self.y)+'#'+str(self.z)+'\n'
        self.client.send_data(command)
        #print(command)
        self.set_point()
    def Z2(self):
        self.get_point()
        self.z -= 1
        command=cmd.CMD_CALIBRATION+'#'+self.leg+'#'+str(self.x)+'#'+str(self.y)+'#'+str(self.z)+'\n'
        self.client.send_data(command)
        #print(command)
        self.set_point()
    def set_point(self,data=None):
        if data==None:
            if self.leg== "one":
                self.one_x.setText(str(self.x))
                self.one_y.setText(str(self.y))
                self.one_z.setText(str(self.z))
                self.point[0][0]=self.x
                self.point[0][1]=self.y
                self.point[0][2]=self.z
            elif self.leg== "two":
                self.two_x.setText(str(self.x))
                self.two_y.setText(str(self.y))
                self.two_z.setText(str(self.z))
                self.point[1][0]=self.x
                self.point[1][1]=self.y
                self.point[1][2]=self.z
            elif self.leg== "three":
                self.three_x.setText(str(self.x))
                self.three_y.setText(str(self.y))
                self.three_z.setText(str(self.z))
                self.point[2][0]=self.x
                self.point[2][1]=self.y
                self.point[2][2]=self.z
            elif self.leg== "four":
                self.four_x.setText(str(self.x))
                self.four_y.setText(str(self.y))
                self.four_z.setText(str(self.z))
                self.point[3][0]=self.x
                self.point[3][1]=self.y
                self.point[3][2]=self.z
        else:
            self.one_x.setText(str(data[0][0]))
            self.one_y.setText(str(data[0][1]))
            self.one_z.setText(str(data[0][2]))
            self.two_x.setText(str(data[1][0]))
            self.two_y.setText(str(data[1][1]))
            self.two_z.setText(str(data[1][2]))
            self.three_x.setText(str(data[2][0]))
            self.three_y.setText(str(data[2][1]))
            self.three_z.setText(str(data[2][2]))
            self.four_x.setText(str(data[3][0]))
            self.four_y.setText(str(data[3][1]))
            self.four_z.setText(str(data[3][2]))
    def get_point(self):
        if self.leg== "one":
            self.x = int(self.one_x.text())
            self.y = int(self.one_y.text())
            self.z = int(self.one_z.text())
        elif self.leg== "two":
            self.x = int(self.two_x.text())
            self.y = int(self.two_y.text())
            self.z = int(self.two_z.text())
        elif self.leg== "three":
            self.x = int(self.three_x.text())
            self.y = int(self.three_y.text())
            self.z = int(self.three_z.text())
        elif self.leg== "four":
            self.x = int(self.four_x.text())
            self.y = int(self.four_y.text())
            self.z = int(self.four_z.text())
    def save(self):
        command=cmd.CMD_CALIBRATION+'#'+'save'+'\n'
        self.client.send_data(command)

        self.point[0][0] = self.one_x.text()
        self.point[0][1] = self.one_y.text()
        self.point[0][2] = self.one_z.text()

        self.point[1][0] = self.two_x.text()
        self.point[1][1] = self.two_y.text()
        self.point[1][2] = self.two_z.text()

        self.point[2][0] = self.three_x.text()
        self.point[2][1] = self.three_y.text()
        self.point[2][2] = self.three_z.text()

        self.point[3][0] = self.four_x.text()
        self.point[3][1] = self.four_y.text()
        self.point[3][2] = self.four_z.text()

        self.Save_to_txt(self.point,'point')
        reply = QMessageBox.information(self,                        
                                        "Message",  
                                        "Saved successfully",  
                                        QMessageBox.Yes)
        #print(command)
    def Read_from_txt(self,filename):
        file1 = open(filename + ".txt", "r")
        list_row = file1.readlines()
        list_source = []
        for i in range(len(list_row)):
            column_list = list_row[i].strip().split("\t")
            list_source.append(column_list)
        for i in range(len(list_source)):
            for j in range(len(list_source[i])):
                list_source[i][j] = int(list_source[i][j])
        file1.close()
        return list_source

    def Save_to_txt(self,list, filename):
        file2 = open(filename + '.txt', 'w')
        for i in range(len(list)):
            for j in range(len(list[i])):
                file2.write(str(list[i][j]))
                file2.write('\t')
            file2.write('\n')
        file2.close()
        
    def leg_point(self,leg):
        if leg.text() == "One":
            if leg.isChecked() == True:
                self.leg = "one"
        elif leg.text() == "Two":
            if leg.isChecked() == True:
                self.leg = "two"
        elif leg.text() == "Three":
            if leg.isChecked() == True:
                self.leg = "three"
        elif leg.text() == "Four":
            if leg.isChecked() == True:
                self.leg = "four"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow=MyWindow()
    myshow.show()
    sys.exit(app.exec_())
