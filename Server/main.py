# -*- coding: utf-8 -*-
import sys,getopt
from ui_server import Ui_server
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Server import *
import os
#import threading
import subprocess

class MyWindow(QMainWindow,Ui_server):
    def __init__(self):
        self.user_ui=True
        self.start_tcp=False
        self.server=Server()
        self.parseOpt()
        if self.user_ui:
            self.app = QApplication(sys.argv)
            super(MyWindow,self).__init__()
            self.setupUi(self)
            self.pushButton_On_And_Off.clicked.connect(self.on_and_off_server)
            self.on_and_off_server()
        if self.start_tcp:
            self.server.turn_on_server()
            self.server.tcp_flag=True
            #self.video=threading.Thread(target=self.server.transmission_video)
            #self.video.start()
            self.instruction=threading.Thread(target=self.server.receive_instruction)
            self.instruction.start()
            
            if self.user_ui:
                self.pushButton_On_And_Off.setText('Off')
                self.states.setText('On')
                
    def parseOpt(self):
        self.opts,self.args = getopt.getopt(sys.argv[1:],"tn")
        for o,a in self.opts:
            if o in ('-t'):
                print ("Open TCP")
                self.start_tcp=True
            elif o in ('-n'):
                self.user_ui=False
                
    def on_and_off_server(self):
        if self.pushButton_On_And_Off.text() == 'On':
            self.pushButton_On_And_Off.setText('Off')
            self.states.setText('On')
            self.server.turn_on_server()
            self.server.tcp_flag=True
            #self.video=threading.Thread(target=self.server.run_raspivid)
            #self.video.start()
            #self.video.join()
            self.instruction=threading.Thread(target=self.server.receive_instruction)
            self.instruction.start()
            #self.instruction.join()
        else:
            self.pushButton_On_And_Off.setText('On')
            self.states.setText('Off')
            self.server.tcp_flag=False
            try:
                #stop_thread(self.video)
                stop_thread(self.instruction)
            except Exception as e:
                print(e)
            self.server.turn_off_server()
            print("close")
    def closeEvent(self,event):
        try:
            #stop_thread(self.video)
            stop_thread(self.instruction)
        except:
            pass
        try:
            self.server.server_socket.shutdown(2)
            self.server.server_socket1.shutdown(2)
            self.server.turn_off_server()
        except:
            pass
        if self.user_ui:
            QCoreApplication.instance().quit()
        os._exit(0)
            
def run_os(command):
    os.system(command)            
if __name__ == '__main__':
    try:
        myshow=MyWindow()
        if myshow.user_ui==True:
            myshow.show();  

            #result = subprocess.run(["./Mapping/robot/build/robot_lidar"], shell=True, capture_output=True, text=True)

            #print("robot_lidar process output")
            #print(result)
            #makeCom=threading.Thread(run_os("cd/Mapping/robot/build&&make")).start()
            command = "raspivid -o - -t 0 -n -w 640 -h 480 -fps 30 -b 1000000 -fl | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264"
            lidar=threading.Thread(run_os("./Mapping/robot/build/robot_lidar")).start()
            #detect=threading.Thread(run_os(command)).start()
            #lidar.join()
            #returned_value = subprocess.call("./Mapping/robot/build/robot_lidar", shell=True)
            #os.system("./Mapping/robot/build/robot_lidar") 
            #run_command("./Mapping/robot/build/robot_lidar")
            sys.exit(myshow.app.exec_())
            os._exit(0)

        else:
            try:
                pass
            except KeyboardInterrupt:
                myshow.close()
        while True:
            pass
    except KeyboardInterrupt:
            myshow.close()
