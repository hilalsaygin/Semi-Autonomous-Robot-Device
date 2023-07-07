#ifndef QSFMLCANVAS_H
#define QSFMLCANVAS_H


#include <QWidget>
#include <QTimer>
#include <SFML/Graphics.hpp>
#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QTimer>
#include <QFrame>

class QSFMLCanvas : public QWidget, public sf::RenderWindow
{
public:
    QSFMLCanvas(QWidget* Parent, const QPoint& Position, const QSize& Size, unsigned int FrameTime = 0);

private:
    virtual void OnInit() = 0;
    virtual void OnUpdate() = 0;
    virtual QPaintEngine* paintEngine() const override;
    virtual void showEvent(QShowEvent* event) override;
    virtual void paintEvent(QPaintEvent* event) override;


    QTimer myTimer;
    bool myInitialized;
};

QSFMLCanvas::QSFMLCanvas(QWidget* Parent, const QPoint& Position, const QSize& Size, unsigned int FrameTime)
    : QWidget(Parent),
      sf::RenderWindow(),
      myInitialized(false)
{
    // Setup some states to allow direct rendering into the widget
    setAttribute(Qt::WA_PaintOnScreen);
    setAttribute(Qt::WA_OpaquePaintEvent);
    setAttribute(Qt::WA_NoSystemBackground);

    // Set strong focus to enable keyboard events to be received
    setFocusPolicy(Qt::StrongFocus);

    // Setup the widget geometry
    move(Position);
    resize(Size);

    // Setup the timer
    myTimer.setInterval(FrameTime);
}

void QSFMLCanvas::showEvent(QShowEvent*)
{
    if (!myInitialized)
    {
        printf("Girdi2\n");
#ifdef Q_WS_X11
        // Under X11, we need to flush the commands sent to the server to ensure that
        // SFML will get an updated view of the windows
        XFlush(QX11Info::display());

        // Create the SFML window with the widget handle
        sf::RenderWindow::create(static_cast<sf::WindowHandle>(winId()));
#else   

        // Create the SFML window with the widget handle
        sf::RenderWindow::create(static_cast<sf::WindowHandle>(winId()));
#endif

        // Let the derived class do its specific stuff
        OnInit();

        // Setup the timer to trigger a refresh at specified framerate
        connect(&myTimer, SIGNAL(timeout()), this, SLOT(repaint()));
        myTimer.start();

        myInitialized = true;
    }
}

QPaintEngine* QSFMLCanvas::paintEngine() const
{
    return nullptr;
}

void QSFMLCanvas::paintEvent(QPaintEvent* event)
{
    QWidget::paintEvent(event);

    // Let the derived class do its specific stuff
    OnUpdate();

    // Display on screen
    display();
}



#endif // QSFMLCANVAS_H
