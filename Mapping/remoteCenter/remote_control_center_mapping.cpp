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

constexpr int BUFFER_SIZE = 100000;

void removeLeadingSpace(char* str) {
    if (str == nullptr || *str == '\0') {
        // Empty string or null pointer
        return;
    }

    char* firstNonSpace = str;
    while (*firstNonSpace == ' ') {
        ++firstNonSpace;
    }

    if (firstNonSpace != str) {
        // Shift the string to remove the leading space
        memmove(str, firstNonSpace, strlen(firstNonSpace) + 1);
    }
}

// Function to start the server and listen for incoming connections
bool startServer(int port)
{
    int serverSock = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSock == -1) {
        std::cerr << "Failed to create socket" << std::endl;
        return false;
    }

    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(port);

    if (bind(serverSock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        std::cerr << "Binding failed" << std::endl;
        close(serverSock);
        return false;
    }

    if (listen(serverSock, 1) < 0) {
        std::cerr << "Listening failed" << std::endl;
        close(serverSock);
        return false;
    }

    std::cout << "Server listening on port " << port << std::endl;

    sockaddr_in clientAddr{};
    socklen_t addrLen = sizeof(clientAddr);
    int clientSock = accept(serverSock, (struct sockaddr*)&clientAddr, &addrLen);
    if (clientSock < 0) {
        std::cerr << "Failed to accept connection" << std::endl;
        return false;
    }

    char buffer[BUFFER_SIZE];

    // Create an SFML window
    sf::RenderWindow window(sf::VideoMode(1920, 1080), "Group 3 Mapping");
    double camera_x = 0;
    double camera_y = 0;
    int zoom = 5;
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
        }

        // Clear the window
        window.clear();

        memset(buffer, 0, BUFFER_SIZE);

        ssize_t bytesRead = recv(clientSock, buffer, BUFFER_SIZE - 1, 0);
        if (bytesRead <= 0) {
            std::cerr << "Failed to receive data" << std::endl;
            close(clientSock);
            continue;
        }
        

        char* buffer_2 = (char*) malloc(strlen(buffer) + 1);
        strcpy(buffer_2,buffer);

        double robot_x = -1;
        double robot_y = -1;
        
        // Get robot location
        char* input = strtok(buffer,"\n");
        
        // Get X
        char* robot_info_x = NULL;
        robot_info_x = (char*) malloc(strlen(input) + 1);
        strcpy(robot_info_x,input);
      
        char* robot_x_c = strtok(robot_info_x,":");
        robot_x_c = strtok(NULL,",");
        robot_x = atof(robot_x_c) * 100; // to cm

        // Get Y
        char* robot_info_y = NULL;
        robot_info_y = (char*) malloc(strlen(input) + 1);
        strcpy(robot_info_y,input);
  
        char* robot_y_c = strtok(robot_info_y,":");
        robot_y_c = strtok(NULL,",");
        robot_y_c = strtok(NULL,":");
        robot_y_c = strtok(NULL,"\n");
        robot_y = atof(robot_y_c) * 100; // to cm


        //printf("ROBOT X : %f\n",robot_x);
        //printf("ROBOT Y : %f\n",robot_y);

        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left))
        {
            camera_x += 100;
            printf("Sol\n");
        } 
        else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right))
        {
            camera_x -= 100;
            printf("Sağ\n");
        }
        else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up))
        {
            camera_y += 100;
            printf("Yukarı\n");
        }
        else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down))
        {
            camera_y -= 100;
            printf("Aşağıya\n");
        }  


        sf::CircleShape center(10.0f); // Create a small circle shape for each point
                center.setFillColor(sf::Color::Red);
                center.setPosition(robot_x * zoom + camera_x, robot_y  * zoom + camera_y);
                window.draw(center); // Draw the circle

    
        double point_x_d = -1;
        double point_y_d = -1;
        

        char* input2 = strtok(buffer_2,"\n");
        input2 = strtok(NULL,"\n");
        while(input2 != NULL){
            
            input2 = strtok(NULL,":");
            input2 = strtok(NULL,",");
            point_x_d = atof(input2) * 100; // to cm

            input2 = strtok(NULL,":");
            input2 = strtok(NULL,"\n");
            point_y_d = atof(input2) * 100; // to cm

            //printf("X : %f Y : %f\n",point_x_d,point_y_d);
            
            point_x_d += robot_x;
            point_x_d *= zoom;
            point_x_d += camera_x;
            point_y_d += robot_y;
            point_y_d *= zoom;
            point_y_d += camera_y;

            sf::CircleShape circle(2.0f); // Create a small circle shape for each point
            circle.setPosition(point_x_d, point_y_d);
            window.draw(circle);// Draw the circle

            input2 = strtok(NULL,"\n");                       
        }

        free(robot_info_x);
        free(robot_info_y);
        free(buffer_2);

        // Display the window
        window.display();
    }


    close(clientSock);
    close(serverSock);
    return true;
}

int main()
{
    int port = 8080;  // Port number to listen on
    bool success = startServer(port);
    if (!success) {
        std::cerr << "Failed to start the server" << std::endl;
        return -1;
    }

    return 0;
}