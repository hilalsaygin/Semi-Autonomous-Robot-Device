#include "mainwindow.h"
#include "ui_mainwindow.h"


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

void MainWindow::on_openRobotCam_clicked()
{

    cv::VideoCapture cap("");

    if(!cap.isOpened()){
        cout << "Error opening video stream or file" << endl;
        return;
    }

    while (1) {
        cv::Mat frame;
        cap >> frame;

//      To change the size of the video
//      cv::resize(frame, frame, cv::Size(640, 480), cv::INTER_LINEAR);

        if(frame.empty()) {
            cout << "Empty Frame" << endl;
            //cap.open("http://192.168.1.106:4747/video");
            break;
        }
        else
            imshow("RobotCam",frame);

        if(cv::waitKey(30) == 27)
            break;
    }

    cap.release();
    cv::destroyWindow("RobotCam");
}
