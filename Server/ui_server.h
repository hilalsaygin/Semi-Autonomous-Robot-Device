#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H
#include <QtWidgets>

class ui_server
{
public:
    QLabel *states;
    QPushButton *pushButton_On_And_Off;

    void setupUi(QWidget *server)
    {
        if (server->objectName().isEmpty())
            server->setObjectName(QStringLiteral("server"));
        server->resize(400, 300);
        QFont font;
        font.setFamily(QStringLiteral("微软雅黑"));
        server->setFont(font);
        server->setStyleSheet(QStringLiteral("QWidget{\n"
            "background:#484848;\n"
            "}\n"
            "QAbstractButton{\n"
            "border-style:none;\n"
            "border-radius:0px;\n"
            "padding:5px;\n"
            "color:#DCDCDC;\n"
            "background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #858585,stop:1 #383838);\n"
            "}\n"
            "QAbstractButton:hover{\n"
            "color:#000000;\n"
            "background-color:#008aff;\n"
            "}\n"
            "QAbstractButton:pressed{\n"
            "color:#DCDCDC;\n"
            "border-style:solid;\n"
            "border-width:0px 0px 0px 4px;\n"
            "padding:4px 4px 4px 2px;\n"
            "border-color:#008aff;\n"
            "background-color:#444444;\n"
            "}\n"
            "\n"
            "QLabel{\n"
            "color:#DCDCDC;\n"
            "}\n"
            "QLabel:focus{\n"
            "border:1px solid #00BB9E;\n"
            "}\n"
            ""));
        states = new QLabel(server);
        states->setGeometry(QRect(120, 80, 160, 90));
        font.setFamily(QStringLiteral("微软雅黑"));
        font.setPointSize(72);
        states->setFont(font);
        states->setAlignment(Qt::AlignCenter);
        states->setObjectName(QStringLiteral("states"));
        pushButton_On_And_Off = new QPushButton(server);
        pushButton_On_And_Off->setGeometry(QRect(160, 220, 80, 30));
        pushButton_On_And_Off->setObjectName(QStringLiteral("pushButton_On_And_Off"));

        retranslateUi(server);
        QMetaObject::connectSlotsByName(server);
    }

    void retranslateUi(QWidget *server)
    {
        server->setWindowTitle(QCoreApplication::translate("server", "Server"));
        states->setText(QCoreApplication::translate("server", "Off"));
        pushButton_On_And_Off->setText(QCoreApplication::translate("server", "On"));
    }
};

#endif