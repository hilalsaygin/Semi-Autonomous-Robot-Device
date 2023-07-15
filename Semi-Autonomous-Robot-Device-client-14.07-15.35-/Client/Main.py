# -*- coding: utf-8 -*-
import cv2
import sys
import os
from ui_led import Ui_led
from ui_face import Ui_Face
from ui_client import Ui_client
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import *
from Client import *
from Calibration import *
#import CnnModelTest
import multiprocessing
import yolov5
from keras.models import load_model

class MyWindow(QMainWindow,Ui_client):
    def __init__(self):
        super(MyWindow,self).__init__()
        
        self.setupUi(self)
        #-self.Video.setScaledContents (True)
        #self.Video.setPixmap(QPixmap('Picture/dog_client.png'))
        #self.timer=QTimer(self)
        #self.timer.timeout.connect(self.refresh_image)
        #self.timer.start(10)

        self.setFocusPolicy(Qt.StrongFocus)
        self.detection_video_label = QLabel(self)

        self.detection_video_label.setFixedSize(700, 450)     #___________ detection pencere boyutu
        self.detection_video_label.move(1000, 350)             #__________ detection pencere pozisyonu


        self.detection_video_label.setAlignment(Qt.AlignCenter)
        self.detection_video_label.setStyleSheet("background-color: black;")  # Set black background
        self.client=Client()
        self.client.move_speed=str(self.slider_speed.value())
        self.points = []
        self.robot_x = 0
        self.robot_y = 0
        self.robot_angle = 0
        self.mapping_widget = MapWidget(self.points ,self.robot_x , self.robot_y , self.robot_angle)
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
        #self.Button_Relax.clicked.connect(self.relax)
        
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
	
        # Load the YOLOv5 model
        self.model = yolov5.load('yolov5s.pt')

        # Set up webcam source
        # self.cap = cv2.VideoCapture(0)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Load class names from file
        with open('classes.names', 'r') as f:
            self.class_names = f.read().splitlines()
    
        #detection_thread = threading.Thread(target=self.display_video)
        #detection_thread.start()

    # Create a function to preprocess the input image
    def preprocess_image(self,image):
        # Convert the image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Resize the image to match the input shape of the model
        image = cv2.resize(image, (28, 28))
        # Reshape the image to match the input shape of the model
        image = np.reshape(image, (1, 28, 28, 3))
        # Normalize the image
        image = image / 255.0
        return image

    # Create a function to make predictions
    def predict_image(self,image,model):
        # Preprocess the input image
        preprocessed_image = self.preprocess_image(image)
        # Make predictions using the model
        predictions = model.predict(preprocessed_image)
        # Get the predicted class label
        predicted_label = np.argmax(predictions[0])
        return predicted_label

    def display_video(self,ip):
        # Load the trained model from the h5 file
        model = load_model('shape.h5')

        # Define the class labels
        class_labels = ['square', 'cyclinder', 'sphere']  # Add your class labels here

        stream_url = "http://192.168.137.25:8095"
        cap = cv2.VideoCapture(stream_url)
        # Check if the webcam is opened successfully
        if not cap.isOpened():
            raise Exception("Could not open the webcam")

        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0

        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    raise Exception("Failed to read frame")

                # Make predictions on the frame
                predicted_label = class_labels[self.predict_image(frame, model)]

                # Display the predicted label on the frame
                cv2.putText(frame, str(predicted_label), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                 # Convert the frame to the QImage format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_qimage = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)

                # Set the QImage directly in QLabel
                self.detection_video_label.setPixmap(QPixmap.fromImage(frame_qimage))

                #cv2.imshow('frame', frame)
                '''
                results = self.model(frame)

                # Get bounding box coordinates, class labels, and confidence scores
                bboxes = results.xyxy[0].numpy()
                scores = results.pred[0][:, 4].numpy()

                # Iterate over detected objects
                for bbox, class_label, score in zip(bboxes, self.class_names, scores):
                    if score > 0.5:  # Set a minimum confidence threshold
                        # Get coordinates
                        x1, y1, x2, y2 = bbox[:4].astype(int)

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # Write label and confidence score
                cv2.putText(frame, f'{class_label}: {score:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                # Convert the frame to QImage format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_qimage = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)

                # Create QPixmap from QImage
                pixmap = QPixmap.fromImage(frame_qimage)

                # Set QPixmap to QLabel
                self.detection_video_label.setPixmap(pixmap)
                '''
                
                # Refresh the QLabel
                app.processEvents()

            except Exception as e:
                print(f"Error display_video frame: {str(e)}")
                break
        '''
        try:
            self.client.client_socket.connect((ip,8002))
            print ("display camera socket Successful !")
        except Exception as e:
            print ("display camera socket failed", str(e))
        try:
            while True:
                # Receive the frame size
                frame_size = int.from_bytes(self.client.client_socket.recv(4), byteorder='big')
                print("frame size here")
                # Receive the frame content
                frame = b''
                while len(frame) < frame_size:
                    frame += self.client.client_socket.recv(frame_size - len(frame))
                    # Perform object detection
                    results = self.model(frame)

                    # Get bounding box coordinates, class labels, and confidence scores
                    bboxes = results.xyxy[0].numpy()
                    scores = results.pred[0][:, 4].numpy()

                    # Iterate over detected objects
                    for bbox, class_label, score in zip(bboxes, self.class_names, scores):
                        if score > 0.5:  # Set a minimum confidence threshold
                            # Get coordinates
                            x1, y1, x2, y2 = bbox[:4].astype(int)

                            # Draw bounding box
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                            # Write label and confidence score
                            cv2.putText(frame, f'{class_label}: {score:.2f}', (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                    # Convert the frame to QImage format
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_qimage = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)

                    # Create QPixmap from QImage
                    pixmap = QPixmap.fromImage(frame_qimage)

                    # Set QPixmap to QLabel
                    self.detection_video_label.setPixmap(pixmap)

                    # Refresh the QLabel
                    app.processEvents()
        except Exception as e:
            print(e)
            print("display")

        '''

    def video(self):
        self.timer.start(10)

    def closeEvent(self,event):
        try:
            self.timer_power.stop()
            self.timer.stop()
            stop_thread(self.detection_thread)
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
            print ("instruction connection Successful !")
        except Exception as e:
            print ("Connect to server Failed!: Server IP is right? Server is opened?")
            print(e)
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
                '''
                elif data[0]==cmd.CMD_RELAX:
                    if data[1]=="0":
                        self.Button_Relax.setText('Relax')
                    else:
                        self.Button_Relax.setText('"Too tired..."')
                        '''
    '''
    def refresh_image(self):
        try:
            if self.client.video_flag == False:
                height, width, bytesPerComponent=self.client.image.shape
                #print (height, width, bytesPerComponent)
                cv2.cvtColor(self.client.image, cv2.COLOR_BGR2RGB, self.client.image)
                QImg = QImage(self.client.image.data, width, height, 3 * width, QImage.Format_RGB888)
                self.detection_video_label.setPixmap(QPixmap.fromImage(QImg))
                self.client.video_flag = True
        except Exception as e:
            print(e)
    '''
    

    #CONNECT
    def connect(self):
        file=open('IP.txt','w')
        file.write(self.lineEdit_IP_Adress.text())
        file.close()
        if self.Button_Connect.text()=='Connect':
            self.IP = self.lineEdit_IP_Adress.text()
            self.client.turn_on_client(self.IP)
            #self.video=threading.Thread(target=self.client.receiving_video,args=(self.IP,))
            self.instruction=threading.Thread(target=self.receive_instruction,args=(self.IP,))
            #self.video.start() 
            self.instruction.start()
            self.Button_Connect.setText('Disconnect')
            self.timer_power.start(1000)
            detection_thread = threading.Thread(target=self.display_video,args=(self.IP,))
            detection_thread.start()

        else:
            try:
                stop_thread(self.detection_thread)
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
class MapWidget(QMainWindow):
    camera_x = 0
    camera_y = 0
    robot_x = 0
    robot_y = 0
    robot_angle = 0
    zoom = 45

    def __init__(self,points,robot_x,robot_y,robot_angle):
        super(MapWidget,self).__init__()
        self.points = points
        self.robot_x = robot_x
        self.robot_y = robot_y
        self.robot_angle = robot_angle
        
        self.clicked_coordinate_label = QLabel("fdsfds",self)
        self.clicked_coordinate_label.setGeometry(1000,900,200,50)
        
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

