#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <SFML/Graphics.hpp>
#include <string>
#include <algorithm>
#include <cctype>
#include <core/base/timer.h>
#include <cmath>
#include <sstream>
#include <vector>
#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QTimer>
#include <QFrame>
#include <QSFMLCanvas.h>
#include <QLabel>
#include <QMouseEvent>
#include <QThread>
#include <QMutex>
#include <QLineEdit>
#include <QPushButton>

using namespace std;

std::string ipAddress = "10.1.233.208";
int remote_port = 8086;

typedef struct  {
    double x;
    double y;
} point_c;

// Lidardan pointleri ve robot konumunu alan thread
class DataReceiverThread : public QThread {
public:
    vector<point_c> &points;
    QMutex mutex;
    int robot_x = 0;
    int robot_y = 0;

    DataReceiverThread(vector<point_c> &points) : points(points){}

    void run() override {
        
        //Open socket
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock == -1) {
            std::cerr << "Failed to create socket" << std::endl;
        }

        //Set server
        sockaddr_in serverAddr{};
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(remote_port);
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

        while(true){
            // Değerleri sıfırla
            int point_x_d = -1;
            int point_y_d = -1;
            double robot_location_buffer[2];

            // Point sayısını al
            int point_count = 0;
            ssize_t bytesRead_pc = recv(sock, &point_count, sizeof(point_count), 0);
            if (bytesRead_pc <= 0) {
                std::cerr << "Failed to receive data" << std::endl;
                ::close(sock);
                point_count = 0;
            }

            // Eğer point sayısı valid ise
            if (point_count > 0 && point_count < 20000) {

                // Robot konumunu al
                ssize_t bytesRead_rl = recv(sock, robot_location_buffer, sizeof(robot_location_buffer), 0);
                if (bytesRead_rl <= 0) {
                    std::cerr << "Failed to receive data" << std::endl;
                    ::close(sock);
                } else {
                    robot_x = robot_location_buffer[0];
                    robot_y = robot_location_buffer[1];
                    memset(robot_location_buffer, 0, sizeof(robot_location_buffer));
                }

                // Pointleri al
                ssize_t bytesRead = 0;
                if (bytesRead_rl > 0) {
                    double point_buffer[point_count][2];

                    bytesRead = recv(sock, point_buffer, sizeof(point_buffer), 0);
                    if (bytesRead <= 0) {
                        std::cerr << "Failed to receive data" << std::endl;
                        ::close(sock);
                    }

                    for (int i = 0; i < point_count; i++) {
                        point_c point;
                        point.x = point_buffer[i][0] + robot_x;
                        point.y = point_buffer[i][1] + robot_y;
                        QMutexLocker locker(&mutex);
                        points.push_back(point);
                    }

                    //printf("Total point count : %ld\n",points.size());
                    QMutexLocker locker(&mutex);
                    while(points.size() > 75000){
                        points.erase(points.begin());
                    }
                    //printf("Total point count : %ld\n",points.size());
                }
            }
        }
        
    }
};

class MappingView : public QSFMLCanvas
{
public :

    MappingView(QWidget* Parent, const QPoint& Position, const QSize& Size) :
    QSFMLCanvas(Parent, Position, Size)
    {}
    DataReceiverThread* receiverThread;


private :
    
    // Mouse tıklamalarını yönet
    void mousePressEvent(QMouseEvent *event){
        if (event->button() == Qt::LeftButton) {
            
            // Mouse tıklanan pozisyonu al
            sf::Vector2i mousePosition = sf::Vector2i();
            mousePosition.x = event->x();
            mousePosition.y = event->y();

            // Eğer refresh butonuna tıklandıysa pointleri sil
            if (refresh_button.getGlobalBounds().contains(static_cast<sf::Vector2f>(mousePosition)))
            {   
                QMutexLocker locker(&receiverThread->mutex);
                points.clear();
                clickText.setString("");
            }

            // Eğer camera up butonuna tıklandıysa kamerayı yukarıya al
            else if(camera_up_button.getGlobalBounds().contains(static_cast<sf::Vector2f>(mousePosition))){
                camera_y += 100;
            }

            // Eğer camera down butonuna tıklandıysa kamerayı aşağıya al
            else if(camera_down_button.getGlobalBounds().contains(static_cast<sf::Vector2f>(mousePosition))){
                camera_y -= 100;
            }

            // Eğer camera left butonuna tıklandıysa kemarayı sola al
            else if(camera_left_button.getGlobalBounds().contains(static_cast<sf::Vector2f>(mousePosition))){
                camera_x += 100;
            }

            // Eğer kamera right butonuna tıklandıysa kamerayı sağa al
            else if(camera_right_button.getGlobalBounds().contains(static_cast<sf::Vector2f>(mousePosition))){
                camera_x -= 100;
            }

            // Eğer zoom in butonuna tıklandıysa zoom arttır
            else if(zoom_in_button.getGlobalBounds().contains(static_cast<sf::Vector2f>(mousePosition))){
                zoom += 5;
            }

            // Eğer zoom out butonuna tıklandıysa zoom arttır
            else if(zoom_out_button.getGlobalBounds().contains(static_cast<sf::Vector2f>(mousePosition))){
                zoom -= 5;
            }

            // Eğer refresh button dışında bir yere tıkladıysa tıklanan yerin konumunu göster
            else{
                std::ostringstream oss;
                oss << "Clicked Position: (" << mousePosition.x - camera_x << ", " << mousePosition.y - camera_y << ")";
                clickText.setString(oss.str());
            }

            printf("Position x : %d , Position Y : %d\n" , event->x() ,event->y());
        }
    }

    // Sadece başlangıçta çalışır
    void OnInit()
    {
        // Get the center of the window
        sf::Vector2f windowCenter = sf::Vector2f(getSize().x / 2.0f, getSize().y / 2.0f);

        zoom = 45;

        camera_x = windowCenter.x;
        camera_y = windowCenter.y;

        // Load font
        if (!font.loadFromFile("./arial.ttf"))
        {
            std::cout << "Error loading font." << std::endl;
        }

        // Clicked location text Init
        clickText.setFont(font);
        clickText.setCharacterSize(20);
        clickText.setPosition(10.f, 10.f);

        //Refresh Button Init
        refresh_button.setPosition(10.0f, 50.0f);
        refresh_button.setFillColor(sf::Color::Blue);

        //Refresh Button Text Init
        refresh_buttonText.setPosition(refresh_button.getPosition().x + 20.0f, refresh_button.getPosition().y + 20.0f);
        refresh_buttonText.setFillColor(sf::Color::White);

        // Kamera kontrol buton ve textleri initalize et
        camera_down_button.setPosition(camera_down_button.getSize().x,getSize().y - camera_down_button.getSize().y);

        camera_up_button.setPosition(50.0f,camera_down_button.getPosition().y - camera_up_button.getSize().y);

        camera_left_button.setPosition(0.0f,camera_down_button.getPosition().y);
        camera_right_button.setPosition(camera_down_button.getSize().x * 2,camera_down_button.getPosition().y);

        camera_up_button.setFillColor(sf::Color::Blue);
        camera_down_button.setFillColor(sf::Color::Blue);
        camera_left_button.setFillColor(sf::Color::Blue);
        camera_right_button.setFillColor(sf::Color::Blue);

        camera_up_button_text.setPosition(camera_up_button.getPosition().x + 20.0f, camera_up_button.getPosition().y + 20.0f);
        camera_down_button_text.setPosition(camera_down_button.getPosition().x + 20.0f, camera_down_button.getPosition().y + 20.0f);
        camera_left_button_text.setPosition(camera_left_button.getPosition().x + 20.0f, camera_left_button.getPosition().y + 20.0f); 
        camera_right_button_text.setPosition(camera_right_button.getPosition().x + 20.0f, camera_right_button.getPosition().y + 20.0f);

        camera_up_button_text.setFillColor(sf::Color::White);
        camera_down_button_text.setFillColor(sf::Color::White);
        camera_left_button_text.setFillColor(sf::Color::White);
        camera_right_button_text.setFillColor(sf::Color::White);


        //Zoom in ve zoom out initialize et
        zoom_in_button.setPosition(getSize().x - (zoom_in_button.getSize().x * 2) , getSize().y - zoom_in_button.getSize().y);
        zoom_out_button.setPosition(getSize().x - zoom_out_button.getSize().x , getSize().y - zoom_out_button.getSize().y);

        zoom_in_button.setFillColor(sf::Color::Blue);
        zoom_out_button.setFillColor(sf::Color::Blue);

        zoom_in_button_text.setPosition(zoom_in_button.getPosition().x + 20.0f, zoom_in_button.getPosition().y + 20.0f);
        zoom_out_button_text.setPosition(zoom_out_button.getPosition().x + 20.0f, zoom_out_button.getPosition().y + 20.0f);

        zoom_in_button_text.setFillColor(sf::Color::White);
        zoom_out_button_text.setFillColor(sf::Color::White);

        // Lidardan veri alan threadi çalıştır.
        receiverThread = new DataReceiverThread(this->points);
        receiverThread->start();
    }

    // Sürekli çalışır
    void OnUpdate()
    {   
        // Clear the screen
        clear(sf::Color::Black);

        // Get the center of the window
        sf::Vector2f windowCenter = sf::Vector2f(getSize().x / 2.0f, getSize().y / 2.0f);

        // Robotu çiz
        sf::CircleShape center(zoom/20);
        center.setFillColor(sf::Color::Red);
        center.setPosition(receiverThread->robot_x * zoom + camera_x, receiverThread->robot_y  * zoom + camera_y);
        draw(center);

        // Pointleri çiz
        QMutexLocker locker(&receiverThread->mutex);
        for(int i = 0; i < points.size(); i++){
            double point_on_window_x = points.at(i).x;
            point_on_window_x *= zoom;
            point_on_window_x += camera_x;
            double point_on_window_y = points.at(i).y;
            point_on_window_y *= zoom;
            point_on_window_y += camera_y;

            sf::CircleShape circle(2.0f);
            circle.setPosition(point_on_window_x, point_on_window_y);
            draw(circle);// Draw the circle
        }

        // Refresh button çiz
        draw(refresh_button);
        draw(refresh_buttonText);

        // Tıklanan yeri gösteren texti çiz
        draw(clickText);
        
        // Kamera kontrol buton ve textlerini çiz
        draw(camera_up_button);
        draw(camera_down_button);
        draw(camera_left_button);
        draw(camera_right_button);
        draw(camera_up_button_text);
        draw(camera_down_button_text);
        draw(camera_left_button_text);
        draw(camera_right_button_text);

        // Zoom button ve text çiz
        draw(zoom_in_button);
        draw(zoom_out_button);
        draw(zoom_in_button_text);
        draw(zoom_out_button_text);
    }

    sf::Font font;
    sf::Text clickText;
    sf::RectangleShape refresh_button = sf::RectangleShape(sf::Vector2f(100.0f, 50.0f));
    sf::Text refresh_buttonText = sf::Text("Refresh", font, 18);

    sf::RectangleShape camera_up_button = sf::RectangleShape(sf::Vector2f(50.0f, 50.0f));
    sf::RectangleShape camera_down_button = sf::RectangleShape(sf::Vector2f(50.0f, 50.0f));
    sf::RectangleShape camera_left_button = sf::RectangleShape(sf::Vector2f(50.0f, 50.0f));
    sf::RectangleShape camera_right_button = sf::RectangleShape(sf::Vector2f(50.0f, 50.0f));

    sf::Text camera_up_button_text = sf::Text("^", font, 18);
    sf::Text camera_down_button_text = sf::Text("v", font, 18);
    sf::Text camera_left_button_text = sf::Text("<", font, 18);
    sf::Text camera_right_button_text = sf::Text(">", font, 18);

    sf::RectangleShape zoom_in_button = sf::RectangleShape(sf::Vector2f(50.0f, 50.0f));
    sf::RectangleShape zoom_out_button = sf::RectangleShape(sf::Vector2f(50.0f, 50.0f));
    sf::Text zoom_in_button_text = sf::Text("+", font, 18);
    sf::Text zoom_out_button_text = sf::Text("-", font, 18);

    vector<point_c> points;
    double camera_x;
    double camera_y;
    int zoom;
    char* clickedLocation[30];

};

int main(int argc, char **argv)
{
    QApplication App(argc, argv);

    // Create the main frame
    QFrame* MainFrame = new QFrame;
    MainFrame->setWindowTitle("Remote Control Center Group 3");
    MainFrame->resize(1920, 1080);
    MainFrame->show();

    // Mapping View
    int mapX = 20;
    int mapY = 420;
    MappingView* SFMLView = new MappingView(MainFrame, QPoint(mapX, mapY), QSize(900 , 506));
    SFMLView->show();

    // Mapping Label
    QLabel *label = new QLabel("Mapping", MainFrame);
    label->setFont(QFont("Arial", 24, QFont::Bold));
    label->setAlignment(Qt::AlignCenter);
    label->setStyleSheet("color: black;");
    label->setGeometry(SFMLView->getPosition().x + (SFMLView->getSize().x / 2) - 150, mapY - 60, 200, 50 );
    label->show();

    // Ip Input
    QLineEdit *ip_line_edit = new QLineEdit(MainFrame);
    ip_line_edit->setPlaceholderText("IP Adress");
    ip_line_edit->setGeometry(10,10,200,30);
    ip_line_edit->show();

    // Port Input
    QLineEdit *port_line_edit = new QLineEdit(MainFrame);
    port_line_edit->setPlaceholderText("Port");
    port_line_edit->setGeometry(ip_line_edit->pos().x() + ip_line_edit->size().width() + 5,ip_line_edit->pos().y(),100,ip_line_edit->size().height());
    port_line_edit->show();

    // Connect button
    QPushButton *connectButton = new QPushButton("Connect", MainFrame);
    connectButton->setGeometry(port_line_edit->pos().x() + port_line_edit->size().width() + 5,port_line_edit->pos().y(),100,port_line_edit->size().height());
    connectButton->show();


    QObject::connect(connectButton, &QPushButton::clicked, MainFrame, [ip_line_edit, port_line_edit]() {
            QString ipAddressStr = ip_line_edit->text();
            int portNumber = port_line_edit->text().toInt();

            /*
            ipAddress = ipAddressStr.toStdString();
            remote_port = portNumber;
            is_connected = 1;*/
        });
    
    

    return App.exec();
}
