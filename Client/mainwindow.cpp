#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "Command.h"
#include "Client.cpp"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>
#include <opencv2/videoio/videoio.hpp>
#include <iostream>
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>
#include <thread>
#include <vector>
#include <sstream>
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_openMappingCam_clicked(){
    cout << "basildi" << endl;
}

void MainWindow::on_up_pressed(){
    std::cout << "up pressed" << std::endl;
    std::string command = "CMD_MOVE_FORWARD#" + std::to_string(2) + '\n';
    Client client;
    client.send_data(command);
    std::cout << command << std::endl;
    

}
void MainWindow::recv_instruction(){
    int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock == -1) {
            std::cerr << "Failed to create socket" << std::endl;
        }
        std::string ipAddress = "127.0.0.1";
        //Set server
        sockaddr_in serverAddr{};
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(5000);
        if (inet_pton(AF_INET, ipAddress.c_str(), &(serverAddr.sin_addr)) <= 0) {
            std::cerr << "Invalid address or address not supported" << std::endl;
            ::close(sock);
        }

        // Connect
        if (::connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
            std::cerr << "Connection failed" << std::endl;
            ::close(sock);
        }


        printf("Bağlandı\n");
        while(1){
            std::string data;
            ssize_t bytesRead_pc = recv(sock, &data, sizeof(data), 0);
            if (bytesRead_pc <= 0) {
                std::cerr << "Failed to receive data" << std::endl;
                ::close(sock);
            }
        }
}
void MainWindow::on_Connect_clicked(){
    cout << "connect clicked" << endl;
    Client client;
    client.turn_on_client("0.0.0.0");
    recv_instruction();
}

void MainWindow::on_openRobotCam_clicked()
{
    std::string ipCameraUrl = "http://192.168.1.105:80";

    cv::VideoCapture cap(ipCameraUrl);

    if(!cap.isOpened()){
        std::cout << "Error opening video stream or file" << std::endl;
        return;
    }

    while (1) {
        cv::Mat frame;
        cap >> frame;

        if(frame.empty()) {
            std::cout << "Empty Frame" << std::endl;
            break;
        }
        else
            cv::imshow("RobotCam", frame);

        if(cv::waitKey(30) == 27)
            break;
    }

    cap.release();
    cv::destroyWindow("RobotCam");
}
