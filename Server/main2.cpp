#include <QApplication>
#include "ui_server.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget server;
    ui_server ui;
    ui.setupUi(&server);
    server.show();

    return app.exec();
}
