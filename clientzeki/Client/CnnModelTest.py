import cv2
import numpy as np
from keras.models import load_model


# Create a function to preprocess the input image
def preprocess_image(image):
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
def predict_image(image,model):
    # Preprocess the input image
    preprocessed_image = preprocess_image(image)
    # Make predictions using the model
    predictions = model.predict(preprocessed_image)
    # Get the predicted class label
    predicted_label = np.argmax(predictions[0])
    return predicted_label

def start():
	# Load the trained model from the h5 file
	model = load_model('shape.h5')
	# Define the class labels
	class_labels = ['square', 'cyclinder', 'sphere']  # Add your class labels here
	# Read video from the webcam
	camera_url = 'http://192.168.165.221:8090'
	video = cv2.VideoCapture(0)

	# Check if the webcam is opened successfully
	if not video.isOpened():
		raise Exception("Could not open the webcam")

	# Loop over frames from the video stream
	while True:
		# Read the current frame from the video stream
		ret, frame = video.read()

		# Check if the frame was successfully read
		if not ret:
		    break

		# Make predictions on the frame
		predicted_label = class_labels[predict_image(frame,model)] 

		# Display the predicted label on the frame
		cv2.putText(frame, str(predicted_label), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

		# Display the frame in a window called "Webcam"
		cv2.imshow('Webcam', frame)

		# Check for the 'q' key to exit the loop
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break

	# Release the video capture object and close the window
	video.release()
	cv2.destroyAllWindows()
	



