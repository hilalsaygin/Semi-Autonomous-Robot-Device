#include <iostream>
#include <thread>
#include <atomic>
#include <QApplication>
#include <QMainWindow>
#include <QPushButton>
#include <QLabel>
#include "Server.h"
#include "mainwindow.h"

class MyWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MyWindow(QWidget *parent = nullptr)
        : QMainWindow(parent)
    {
        user_ui = true;
        start_tcp = false;
        server = new Server();
        

        if (user_ui)
        {
            setupUi();
            pushButton_On_And_Off->setText("On");
            states->setText("Off");

            QObject::connect(pushButton_On_And_Off, &QPushButton::clicked, this, &MyWindow::on_and_off_server);
            on_and_off_server();
        }

        if (start_tcp)
        {
            server->turnOnServer();
            server->tcp_flag = true;
            video = std::thread(&Server::transmissionVideo, server);
            instruction = std::thread(&Server::receiveInstruction, server);

            if (user_ui)
            {
                on_on_off_button_pressed->setText("Off");
                states->setText("On");
            }
        }
    }


public slots:
    void on_and_off_server()
    {
        if (on_on_off_button_pressed->text() == "On")
        {
            pushButton_On_And_Off->setText("Off");
            states->setText("On");
            server->turnOnServer();
            server->tcp_flag = true;
            video = std::thread(&Server::transmissionVideo, server);
            instruction = std::thread(&Server::receiveInstruction, server);
        }
        else
        {
            pushButton_On_And_Off->setText("On");
            states->setText("Off");
            server->turnOffServer();
            server->tcp_flag = false;
            if (video.joinable())
                video.join();
            if (instruction.joinable())
                instruction.join();
        }
    }

private:
    Ui::MainWindow *ui;
    QPushButton *pushButton_On_And_Off;
    QLabel *states;
    QPushButton *on_on_off_button_pressed;
    Server *server;
    std::thread video;
    std::thread instruction;
    bool user_ui;
    bool start_tcp;

    void setupUi()
    {
        // UI setup logic
    }
};

int main()
{
    
    Server* server = new Server();
    server->turnOnServer();
    server->tcp_flag = true;
   
}


