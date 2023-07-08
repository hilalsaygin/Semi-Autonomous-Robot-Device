#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>
#include <opencv2/videoio/videoio.hpp>

#include <opencv2/core/mat.hpp>
#include <opencv2/highgui.hpp>

#include <iostream>
using namespace std;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:

    void on_up_pressed();
    void on_openRobotCam_clicked();
    void on_openMappingCam_clicked();
    void on_Connect_clicked();
    void recv_instruction();

private:
    Ui::MainWindow *ui;

};

#endif // MAINWINDOW_H
