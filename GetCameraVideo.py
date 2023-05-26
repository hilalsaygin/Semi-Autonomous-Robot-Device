import cv2
import numpy as np
stream_url = "http://192.168.137.246:8090"  # Replace <raspberry_pi_ip_address> with the IP address of your Raspberry Pi

cap = cv2.VideoCapture(stream_url)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Process the frame (e.g., display it, perform image processing)

    cv2.imshow("Video Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()