import cv2
import socket
import pickle
import struct

# Hedef bilgisayarın IP adresi ve port numarası
host = '192.168.0.100'
port = 5000

# Socket oluşturun ve bağlantıyı yapın
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

# Bağlantıyı kabul edin
conn, addr = server_socket.accept()

# Sonsuz bir döngü içinde veriyi alın, çözümleyin ve görüntüyü gösterin
data = b""
payload_size = struct.calcsize("L")
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)

    # Veri boyutunu çözümleyin
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    # Görüntüyü alın
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Kodlanmış görüntüyü çözümleyin
    frame = pickle.loads(frame_data)

    # Görüntüyü gösterin
    cv2.imshow('Alınan Görüntü', frame)

    # 'q' tuşuna basıldığında döngüyü sonlandırın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakın
conn.close()
cv2.destroyAllWindows()
