#include <opencv2/opencv.hpp>

int main() {
    cv::VideoCapture cap(0);  // Use 0 for the default camera

    // Check if the camera is opened successfully
    if (!cap.isOpened()) {
        std::cout << "Failed to open the camera" << std::endl;
        return -1;
    }

    cv::namedWindow("Video", cv::WINDOW_NORMAL);

    // Read and display frames from the camera
    while (true) {
        cv::Mat frame;
        bool ret = cap.read(frame);

        // If the frame was not read successfully, exit the loop
        if (!ret) {
            break;
        }

        // Display the frame in a window named "Video"
        cv::imshow("Video", frame);

        // Wait for the 'q' key to be pressed to exit the loop
        if (cv::waitKey(1) == 'q') {
            break;
        }
    }

    // Release the VideoCapture object and close the window
    cap.release();
    cv::destroyAllWindows();

    return 0;
}
