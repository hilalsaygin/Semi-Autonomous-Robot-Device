# -*- coding: utf-8 -*-
import cv2
import io
import os
import time
import fcntl
import socket
import struct
import picamera2 as picamera
from picamera2 import Picamera2,Preview
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from picamera2.encoders import Quality
from threading import Condition
import threading
from Led import *
from Servo import *
from Thread import *
from Buzzer import *
from Control import *
from ADS7830 import *
from Ultrasonic import *
from Command import COMMAND as cmd

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class Server:
    def __init__(self):
        
        self.tcp_flag=False
        self.led=Led()
        self.servo=Servo()
        self.adc=ADS7830()
        self.buzzer=Buzzer()
        self.control=Control()
        self.sonic=Ultrasonic()
        self.control.Thread_conditiona.start()
        self.battery_voltage=[8.4,8.4,8.4,8.4,8.4]
        
    def get_interface_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                            0x8915,
                                            struct.pack('256s',b'wlan0'[:15])
                                            )[20:24])
    def turn_on_server(self):
        #ip adress
        HOST=self.get_interface_ip()
        #Port 8001 for video transmission
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        self.server_socket.bind((HOST, 8002))              
        self.server_socket.listen(1)
        
        print('Server address: '+HOST)
        
    def turn_off_server(self):
        try:
            self.connection.close()
        except :
            print ('\n'+"No client connection")
    
    def reset_server(self):
        self.turn_off_server()
        self.turn_on_server()
        self.video=threading.Thread(target=self.transmission_video)
        self.video.start()

    def transmission_video(self):
        try:
            self.connection, self.client_address = self.server_socket.accept()
            self.connection = self.connection.makefile('wb')
        except:
            pass

        self.server_socket.close()
        print("Socket video connected ...")

        cap = cv2.VideoCapture(0)  # 0 for the default camera
        if not cap.isOpened():
            print("Failed to open camera")
            return

        # Set the video size
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Failed to capture frame")
                break

            try:
                # Serialize frame to a string
                _, img_encoded = cv2.imencode('.jpg', frame)
                data = np.array(img_encoded).tobytes()

                len_frame = len(data)
                length_bin = struct.pack('<I', len_frame)

                # Send frame length and data over the connection
                self.connection.write(length_bin)
                self.connection.write(data)
            except Exception as e:
                print("Error: " + str(e))
                break

        cap.release()
        self.connection.close()
        print("End transmit...")

if __name__ == '__main__':
    pass