#include <opencv2/opencv.hpp>
#include <iostream>
#include <filesystem>

int main() {
    cv::VideoCapture cam("video.mp4");
    try {
        if (!std::filesystem::exists("data")) {
            std::filesystem::create_directory("data");
        }
    } catch (std::filesystem::filesystem_error& e) {
        std::cout << "Error: Creating directory of data" << std::endl;
    }

    int currentframe = 0;
    while (true) {
        cv::Mat frame;
        bool ret = cam.read(frame);
        if (ret) {
            std::string name = "./data/frame" + std::to_string(currentframe) + ".jpg";
            std::cout << "Creating..." << name << std::endl;
            cv::imwrite(name, frame);
            currentframe++;
        } else {
            break;
        }
    }

    cam.release();
    cv::destroyAllWindows();

    return 0;
}
