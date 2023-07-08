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
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QLabel *Title;
    QLabel *on_off_text;
    QPushButton *on_off_button;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(500, 650);
        MainWindow->setMaximumSize(QSize(500, 450));
        MainWindow->setStyleSheet(QString::fromUtf8("background-color: qlineargradient(spread:pad, x1:0.198, y1:0.789773, x2:0.868, y2:0.198864, stop:0 rgba(79, 79, 79, 255), stop:1 rgba(79, 79, 79, 255));\n"
""));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        Title = new QLabel(centralWidget);
        Title->setObjectName(QString::fromUtf8("Title"));
        Title->setGeometry(QRect(100, 0, 400, 50));
        Title->setStyleSheet(QString::fromUtf8("font: 20pt;\n"
"                        color: #528b8b;\n"
"                        "));
        on_off_text = new QLabel(centralWidget);
        on_off_text->setObjectName(QString::fromUtf8("on_off_text"));
        on_off_text->setGeometry(QRect(200, 140, 200, 60));
        on_off_text->setStyleSheet(QString::fromUtf8("font: 50pt;\n"
"                        color: #ffffff;\n"
"                        "));
        on_off_button = new QPushButton(centralWidget);
        on_off_button->setObjectName(QString::fromUtf8("on_off_button"));
        on_off_button->setGeometry(QRect(215, 270, 100, 40));
        on_off_button->setStyleSheet(QString::fromUtf8("font: 12pt;\n"
"                        color: #ffffff;\n"
"                        border: 2px solid #1c1c1c; \n"
"                        background-color: #363636;\n"
"                        border-radius: 2px;"));
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
        Title->setText(QCoreApplication::translate("MainWindow", "Robot Dog Server Group 3 ", nullptr));
        on_off_text->setText(QCoreApplication::translate("MainWindow", "OFF ", nullptr));
        on_off_button->setText(QCoreApplication::translate("MainWindow", "Open Server", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
