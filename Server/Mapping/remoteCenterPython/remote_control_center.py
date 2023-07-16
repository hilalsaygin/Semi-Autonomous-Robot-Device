import socket
import threading
from ctypes import c_int, c_double
from queue import Queue
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget , QPushButton , QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint , QThread, pyqtSignal , QMutex , pyqtSlot , QMutexLocker



class DataReceiverThread(QThread):

    def __init__(self, points ,robot_x ,robot_y):
        super().__init__()
        self.points = points
        self.mutex = QMutex()
        self.robot_x = robot_x
        self.robot_y = robot_y
        self.ipAddress = "192.168.2.221"
        self.remote_port = 8085

    def run(self):
        # Open socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Set server
            server_address = (self.ipAddress, self.remote_port)
            sock.connect(server_address)
            print("Bağlandı")
            
            # Define separate buffer for robot location bytes
            robot_location_bytes = bytearray(16)

            while True:
                # Değerleri sıfırla
                point_x_d = -1
                point_y_d = -1
                robot_location_buffer = (c_double * 2)()

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
                        robot_location_buffer = (c_double * 2).from_buffer(robot_location_bytes)
                        self.robot_x = float(robot_location_buffer[0])
                        self.robot_y = float(robot_location_buffer[1])
                        robot_location_buffer[:] = (c_double * 2)()
                        #print("robot x : " , self.robot_x)
                        #print("robot_y : " , self.robot_y)

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
                                    self.points.append((float(point[0]) + self.robot_x, float(point[1]) + self.robot_y))
                                    #  print("Point x : " , float(point[0]) + self.robot_x, "Point y : " , float(point[1]) + self.robot_y)

                            with QMutexLocker(self.mutex):
                                while len(self.points) > 75000:
                                    self.points.pop(0)
                            
        finally:
            sock.close()

class MapWidget(QWidget):
    camera_x = 0
    camera_y = 0
    robot_x = 0
    robot_y = 0
    zoom = 45

    def __init__(self,points,robot_x,robot_y):
        super().__init__()
        self.points = points
        self.robot_x = robot_x
        self.robot_y = robot_y
        
        self.clicked_coordinate_label = QLabel("",self)
        self.clicked_coordinate_label.setGeometry(10,self.geometry().height(),200,50)
        
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
    
    # TODO
    # Tıklanan yerin ve robotun konumu kullanılarak gidilecek yön ve mesafe hesaplanıp,
    # robota hareket instruction u gönderilecek
    def send_move_instruction(self,clicked_x,clicked_y):
        pass


class MainWindow(QMainWindow):
    window_width = 1920
    window_height = 1080

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Example")
        self.setGeometry(0, 0, self.window_width, self.window_height)

        self.points = []
        self.robot_x = 0
        self.robot_y = 0
        self.mapping_widget = MapWidget(self.points ,self.robot_x , self.robot_y)
        self.setCentralWidget(self.mapping_widget)

        self.init_data()
        self.update_timer = self.startTimer(int(1000 / 5))  # Update every second

        space = 30

        self.zoom_in_button = QPushButton("Zoom In", self)
        self.zoom_in_button.move(10, 10)
        self.zoom_in_button.clicked.connect(self.zoom_in)

        self.zoom_out_button = QPushButton("Zoom Out", self)
        self.zoom_out_button.move(10, 40)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        self.camera_left_button = QPushButton("Camera Left", self)
        self.camera_left_button.move(10, 70 + space)
        self.camera_left_button.clicked.connect(self.camera_left)

        self.camera_left_button = QPushButton("Camera Right", self)
        self.camera_left_button.move(10, 100 + space)
        self.camera_left_button.clicked.connect(self.camera_right)

        self.camera_left_button = QPushButton("Camera Up", self)
        self.camera_left_button.move(10, 130 + space)
        self.camera_left_button.clicked.connect(self.camera_up)

        self.camera_left_button = QPushButton("Camera Down", self)
        self.camera_left_button.move(10, 160 + space)
        self.camera_left_button.clicked.connect(self.camera_down)

        self.clear_map_button = QPushButton("Clear", self)
        self.clear_map_button.move(10, 210 + space)
        self.clear_map_button.clicked.connect(self.clear_map)

    def init_data(self):
        self.receiver_thread = DataReceiverThread(self.points,self.robot_x,self.robot_y)
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
        


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    """
    points = []
    data_receiver = DataReceiverThread(points)
    data_receiver.start()
    """




