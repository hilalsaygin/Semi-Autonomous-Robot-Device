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

using namespace std;


typedef struct  {
    double x;
    double y;
} point_c;


// Function to start the server and listen for incoming connections
bool startClient(std::string ipAddress, int remote_port)
{

    //Open socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        std::cerr << "Failed to create socket" << std::endl;
        return 1;
    }

    //Set server
    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(remote_port);
    if (inet_pton(AF_INET, ipAddress.c_str(), &(serverAddr.sin_addr)) <= 0) {
        std::cerr << "Invalid address or address not supported" << std::endl;
        close(sock);
        return 1;
    }

    // Connect
    if (connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        std::cerr << "Connection failed" << std::endl;
        close(sock);
        return 1;
    }

    printf("Bağlandı\n");

    // Points vector
    vector<point_c> points;
    
    int point_count = 0;
    double robot_location_buffer[2];
    double point_x_d = -1;
    double point_y_d = -1;
    double robot_x = -1;
    double robot_y = -1;
    double camera_x = 800;
    double camera_y = 500;
    int zoom = 50;
    char* clickedLocation[30];


    // Create an SFML window
    sf::RenderWindow window(sf::VideoMode(1920, 1080), "Group 3 Mapping");

    // Clicked Location Text
    sf::Font font;
    if (!font.loadFromFile("./Mapping/remoteCenter/build/arial.ttf"))
    {
        std::cout << "Error loading font." << std::endl;
        return -1;
    }

    sf::Text clickText;
    clickText.setFont(font);
    clickText.setCharacterSize(20);
    clickText.setPosition(10.f, 10.f);

    //Refresh Button
    sf::RectangleShape refresh_button(sf::Vector2f(100.0f, 50.0f));
    refresh_button.setPosition(10.0f, 50.0f);
    refresh_button.setFillColor(sf::Color::Blue);

    //Refresh button text
    sf::Text refresh_buttonText("Refresh", font, 18);
    refresh_buttonText.setPosition(refresh_button.getPosition().x + 20.0f, refresh_button.getPosition().y + 20.0f);
    refresh_buttonText.setFillColor(sf::Color::White);

    // Main loop
    while (window.isOpen())
    {   

        // Get the center of the window
        sf::Vector2f windowCenter = sf::Vector2f(window.getSize().x / 2.0f, window.getSize().y / 2.0f);

        // Process events
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
            
            if (event.type == sf::Event::MouseButtonPressed)
            {
                if (event.mouseButton.button == sf::Mouse::Left)
                {
                    sf::Vector2i mousePosition = sf::Mouse::getPosition(window);
                    if (refresh_button.getGlobalBounds().contains(static_cast<sf::Vector2f>(mousePosition)))
                    {
                        points.clear(); // Truncate the vector
                    }else{
                        std::ostringstream oss;
                        oss << "Clicked Position: (" << mousePosition.x - camera_x << ", " << mousePosition.y - camera_y << ")";
                        clickText.setString(oss.str());
                    }
                }
            }
            else if(event.type == sf::Event::KeyPressed)
            {
                if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left))
                {
                    camera_x += 100;
                } 
                else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right))
                {
                    camera_x -= 100;
                }
                else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up))
                {
                    camera_y += 100;
                }
                else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down))
                {
                    camera_y -= 100;
                }  
            }
        }

        // Clear the window
        window.clear();
        printf("a\n");
        // Point sayısını al
        point_count = 0;
        ssize_t bytesRead_pc = recv(sock, &point_count, sizeof(point_count), 0);
        if (bytesRead_pc <= 0) {
            std::cerr << "Failed to receive data" << std::endl;
            close(sock);
            continue;
        }
        printf("point_count : %d\n",point_count);

        //sleep(1);
        //usleep(500000);
        // Robot konumunu al
        ssize_t bytesRead_rl = recv(sock, robot_location_buffer , sizeof(robot_location_buffer), 0);
        if (bytesRead_rl <= 0) {
            std::cerr << "Failed to receive data" << std::endl;
            close(sock);
            continue;
        }

        robot_x = robot_location_buffer[0];
        robot_y = robot_location_buffer[1];

        printf("robot_x : %f\n",robot_x);
        printf("robot_y : %f\n",robot_y);

        memset(robot_location_buffer,0,sizeof(robot_location_buffer));


        // Draw robot
        
        sf::CircleShape center(10.0f); // Create a small circle shape for each point
                center.setFillColor(sf::Color::Red);
                center.setPosition(robot_x * zoom + camera_x, robot_y  * zoom + camera_y);
                window.draw(center); // Draw the circle
        

        usleep(200000);


        double point_buffer[point_count][2];

        // Pointleri  al
        ssize_t bytesRead = recv(sock, point_buffer , sizeof(point_buffer), 0);
        if (bytesRead <= 0) {
            std::cerr << "Failed to receive data" << std::endl;
            close(sock);
            continue;
        }


        for(int i = 0; i < point_count; i++){
            point_c point;

            point.x = point_buffer[i][0] + robot_x;
            point.y = point_buffer[i][1] + robot_y;
            //printf("x : %f , y : %f\n" , point.x , point.y);
            points.push_back(point);
            
        }
                           

        // Draw clicked location text
        window.draw(clickText);
 

        // Draw refresh button
        window.draw(refresh_button);
        window.draw(refresh_buttonText);

    
        // Draw points
        for(int i = 0; i < points.size(); i++){
            double point_on_window_x = points.at(i).x;
            point_on_window_x *= zoom;
            point_on_window_x += camera_x;
            double point_on_window_y = points.at(i).y;
            point_on_window_y *= zoom;
            point_on_window_y += camera_y;

            sf::CircleShape circle(2.0f); // Create a small circle shape for each point
            circle.setPosition(point_on_window_x, point_on_window_y);
            window.draw(circle);// Draw the circle
        }

        // Display the window
        window.display();
    
    }


    close(sock);
    return true;
}

int main()
{   
    std::string ipAddress = "192.168.148.221"; 
    int port = 8080;  // Port number to listen on
    bool success = startClient(ipAddress,port);
    if (!success) {
        std::cerr << "Failed to start the server" << std::endl;
        return -1;
    }

    return 0;
}
