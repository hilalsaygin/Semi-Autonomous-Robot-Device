import cv2
import socket
import pickle
import struct

# Görüntü işleme kodunuz...

# Hedef bilgisayarın IP adresi ve port numarası
host = '192.168.0.100'
port = 5000

# Socket oluşturun ve bağlantıyı yapın
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Sonsuz bir döngü içinde görüntüyü alın, kodlayın ve gönderin
while True:
    ret, frame = cap.read()

    # Görüntüyü işleyin (isteğe bağlı)

    # Görüntüyü kodlayın
    data = pickle.dumps(frame)

    # Veri boyutunu gönderin
    client_socket.sendall(struct.pack("L", len(data)))

    # Kodlanmış görüntüyü gönderin
    client_socket.sendall(data)

# Kaynakları serbest bırakın
client_socket.close()
cap.release()
cv2.destroyAllWindows()
