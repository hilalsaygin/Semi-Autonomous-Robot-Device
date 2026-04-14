import socket
import pygame
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Sunucu adresi ve port numarası
HOST = '192.168.137.12'
PORT = 8024

# TCP soketini oluşturma ve sunucuya bağlanma
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

data = b''

while True:
    print("hello")
    packet = client_socket.recv(4096)
    print("packet")
    if not packet:
        break
    
    data += packet

    # Convert the received data to a NumPy array
    img_array = np.frombuffer(data, dtype=np.uint8)

    # Decode the NumPy array to an image
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Display the image
    cv2.imshow('Video', image)
    cv2.waitKey(1)  # Wait for a key press to update the display

cv2.destroyAllWindows()
client_socket.close()