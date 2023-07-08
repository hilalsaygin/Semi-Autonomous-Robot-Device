/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QLabel *Title;
    QLabel *Title1;
    QLineEdit *IP;
    QPushButton *openRobotCam;
    QPushButton *openMappingCam;
    QLabel *manualControl;
    QToolButton *up;
    QToolButton *right;
    QToolButton *left;
    QToolButton *down;
    QToolButton *Connect;
    QLabel *dataTitle;
    QLabel *battery;
    QLabel *obstacle;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1080, 650);
        MainWindow->setMaximumSize(QSize(1264, 739));
        MainWindow->setStyleSheet(QString::fromUtf8("background-color: qlineargradient(spread:pad, x1:0.198, y1:0.789773, x2:0.868, y2:0.198864, stop:0 rgba(79, 79, 79, 255), stop:1 rgba(79, 79, 79, 255));\n"
""));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        Title = new QLabel(centralWidget);
        Title->setObjectName(QString::fromUtf8("Title"));
        Title->setGeometry(QRect(400, 0, 400, 50));
        Title->setStyleSheet(QString::fromUtf8("font: 25pt;\n"
"                        color: #528b8b;\n"
"                        "));
        Title1 = new QLabel(centralWidget);
        Title1->setObjectName(QString::fromUtf8("Title1"));
        Title1->setGeometry(QRect(50, 80, 100, 20));
        Title1->setStyleSheet(QString::fromUtf8("font: 10pt;\n"
"                        color: #528b8b;\n"
"                        "));
        IP = new QLineEdit(centralWidget);
        IP->setObjectName(QString::fromUtf8("IP"));
        IP->setGeometry(QRect(50, 100, 150, 30));
        IP->setStyleSheet(QString::fromUtf8("font: 12pt;\n"
"                        color: #000000;\n"
"                        border: 1px solid #1c1c1c; \n"
"                        background-color: #ffffff;\n"
"                        "));
        openRobotCam = new QPushButton(centralWidget);
        openRobotCam->setObjectName(QString::fromUtf8("openRobotCam"));
        openRobotCam->setGeometry(QRect(50, 250, 150, 50));
        openRobotCam->setStyleSheet(QString::fromUtf8("font: 12pt;\n"
"                        color: #ffffff;\n"
"                        border: 2px solid #1c1c1c; \n"
"                        background-color: #363636;\n"
"                        border-radius: 2px;"));
        openMappingCam = new QPushButton(centralWidget);
        openMappingCam->setObjectName(QString::fromUtf8("openMappingCam"));
        openMappingCam->setGeometry(QRect(50, 400, 150, 50));
        openMappingCam->setStyleSheet(QString::fromUtf8("font: 12pt;\n"
"                        color: #ffffff;\n"
"                        border: 2px solid #1c1c1c; \n"
"                        background-color: #363636;\n"
"                        border-radius: 2px;"));
        manualControl = new QLabel(centralWidget);
        manualControl->setObjectName(QString::fromUtf8("manualControl"));
        manualControl->setGeometry(QRect(450, 110, 250, 20));
        manualControl->setStyleSheet(QString::fromUtf8("font: 18pt;\n"
"                        color: #363636;\n"
"                        "));
        up = new QToolButton(centralWidget);
        up->setObjectName(QString::fromUtf8("up"));
        up->setGeometry(QRect(480, 150, 140, 60));
        up->setStyleSheet(QString::fromUtf8("font: 11pt;\n"
"                        color: #ffffff;\n"
"                        border: 2px solid #696969; \n"
"                        border-radius: 5px;"));
        right = new QToolButton(centralWidget);
        right->setObjectName(QString::fromUtf8("right"));
        right->setGeometry(QRect(620, 210, 140, 60));
        right->setStyleSheet(QString::fromUtf8("font: 11pt;\n"
"                        color: #ffffff;\n"
"                        border: 2px solid #696969; \n"
"                        border-radius: 5px;"));
        left = new QToolButton(centralWidget);
        left->setObjectName(QString::fromUtf8("left"));
        left->setGeometry(QRect(340, 210, 140, 60));
        left->setStyleSheet(QString::fromUtf8("font: 11pt;\n"
"                        color: #ffffff;\n"
"                        border: 2px solid #696969; \n"
"                        border-radius: 5px;"));
        down = new QToolButton(centralWidget);
        down->setObjectName(QString::fromUtf8("down"));
        down->setGeometry(QRect(480, 270, 140, 60));
        down->setStyleSheet(QString::fromUtf8("font: 11pt;\n"
"                        color: #ffffff;\n"
"                        border: 2px solid #696969; \n"
"                        border-radius: 5px;"));
        Connect = new QToolButton(centralWidget);
        Connect->setObjectName(QString::fromUtf8("Connect"));
        Connect->setGeometry(QRect(80, 150, 100, 40));
        Connect->setStyleSheet(QString::fromUtf8("font: 11pt;\n"
"                        color: #ffffff;\n"
"                        border: 2px solid #696969; \n"
"                        border-radius: 5px;"));
        dataTitle = new QLabel(centralWidget);
        dataTitle->setObjectName(QString::fromUtf8("dataTitle"));
        dataTitle->setGeometry(QRect(880, 100, 400, 50));
        dataTitle->setStyleSheet(QString::fromUtf8("font: 18pt;\n"
"                        color: #528b8b;\n"
"                        "));
        battery = new QLabel(centralWidget);
        battery->setObjectName(QString::fromUtf8("battery"));
        battery->setGeometry(QRect(830, 150, 300, 50));
        battery->setStyleSheet(QString::fromUtf8("font: 13pt;\n"
"                        color: #1c1c1c;\n"
"                        "));
        obstacle = new QLabel(centralWidget);
        obstacle->setObjectName(QString::fromUtf8("obstacle"));
        obstacle->setGeometry(QRect(830, 200, 300, 50));
        obstacle->setStyleSheet(QString::fromUtf8("font: 13pt;\n"
"                        color: #1c1c1c;\n"
"                        "));
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1080, 26));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        Title->setText(QCoreApplication::translate("MainWindow", "Robot Dog Client Group 3 ", nullptr));
        Title1->setText(QCoreApplication::translate("MainWindow", "IP address:", nullptr));
        IP->setText(QString());
        openRobotCam->setText(QCoreApplication::translate("MainWindow", "Open Robot Video", nullptr));
        openMappingCam->setText(QCoreApplication::translate("MainWindow", "Open Mapping Cam", nullptr));
        manualControl->setText(QCoreApplication::translate("MainWindow", "- Manual Control -", nullptr));
        up->setText(QCoreApplication::translate("MainWindow", "Forward", nullptr));
        right->setText(QCoreApplication::translate("MainWindow", "Step Right", nullptr));
        left->setText(QCoreApplication::translate("MainWindow", "Step Left", nullptr));
        down->setText(QCoreApplication::translate("MainWindow", "Backward", nullptr));
        Connect->setText(QCoreApplication::translate("MainWindow", "Connect", nullptr));
        dataTitle->setText(QCoreApplication::translate("MainWindow", "Data From Robot ", nullptr));
        battery->setText(QCoreApplication::translate("MainWindow", "Battery:", nullptr));
        obstacle->setText(QCoreApplication::translate("MainWindow", "Obstacle:", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
