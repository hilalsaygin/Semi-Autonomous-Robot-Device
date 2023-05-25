import cv2

# Create a VideoCapture object to capture video from the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open the camera")
    exit()

# Read and display frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # If the frame was not read successfully, exit the loop
    if not ret:
        break

    # Display the frame in a window named "Video"
    cv2.imshow("Video", frame)

    # Wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()
