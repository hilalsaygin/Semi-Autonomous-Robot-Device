QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17

# The following define makes your compiler emit warnings if you use
# any Qt feature that has been marked deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    mainwindow.h

FORMS += \
    mainwindow.ui



INCLUDEPATH += /usr/include/opencv4


LIBS += -lopencv_core -lopencv_highgui -lopencv_imgcodecs -lopencv_videoio
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_calib3d470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_dnn470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_features2d470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_flann470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_gapi470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_imgcodecs470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_imgproc470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_ml470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_objdetect470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_photo470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_stitching470.dll
#LIBS += C:/Users/megas/Documents/opencv/build/bin/libopencv_video470.dll

