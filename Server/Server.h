#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>
#include <thread>
#include <vector>
#include <sstream>

#define SERVER_PORT 12345
#define SERVER_PORT1 12346
#define MAX_BUFFER_SIZE 1024

class Server {
public:
    Server();
    void turnOnServer();
    void turnOffServer();
    void resetServer();
    void sendData(int socket, const std::string& data);

public:
    int server_socket;
    int client_socket;
    int server_socket1;
    int client_socket1;
    struct sockaddr_in server_address;
    struct sockaddr_in server_address1;
    std::thread videoThread;
    std::thread instructionThread;
    std::vector<std::string> order;
    bool tcp_flag;
    int moveFlag;
    bool relaxFlag;
    std::string command;

    void transmissionVideo();
    void sendRelaxFlag();
    void receiveInstruction();
};

Server::Server() {
    tcp_flag = false;
    moveFlag = 0;
    relaxFlag = false;
    order.resize(1);
}

void Server::turnOnServer() {
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        perror("Failed to create socket");
        exit(EXIT_FAILURE);
    }

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(SERVER_PORT);

    if (bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0) {
        perror("Failed to bind the socket");
        exit(EXIT_FAILURE);
    }

    listen(server_socket, 1);

    std::cout << "Server is turned on and waiting for connection..." << std::endl;

    client_socket = accept(server_socket, NULL, NULL);
    if (client_socket < 0) {
        perror("Failed to accept connection");
        exit(EXIT_FAILURE);
    }

    std::cout << "Client is connected." << std::endl;

    close(server_socket);

    videoThread = std::thread(&Server::transmissionVideo, this);
    instructionThread = std::thread(&Server::receiveInstruction, this);
}

void Server::turnOffServer() {
    if (client_socket > 0) {
        close(client_socket);
    }

    if (server_socket > 0) {
        close(server_socket);
    }

    if (client_socket1 > 0) {
        close(client_socket1);
    }

    if (server_socket1 > 0) {
        close(server_socket1);
    }
}

void Server::resetServer() {
    videoThread = std::thread(&Server::transmissionVideo, this);
    instructionThread = std::thread(&Server::receiveInstruction, this);
}

void Server::transmissionVideo() {
    client_socket = accept(server_socket, NULL, NULL);
    if (client_socket < 0) {
        perror("Failed to accept connection");
        exit(EXIT_FAILURE);
    }

    std::cout << "Video transmission started." << std::endl;

    // Video transmission code goes here

    close(client_socket);
}

void Server::sendRelaxFlag() {
    if (moveFlag != 2) {
        sendData(client_socket1, command);
    }
}
void Server::sendData(int socket, const std::string& data) {
    ssize_t bytesSent = send(socket, data.c_str(), data.length(), 0);
    if (bytesSent < 0) {
        perror("Failed to send data");
        exit(EXIT_FAILURE);
    }
}
void Server::receiveInstruction() {
    server_socket1 = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket1 < 0) {
        perror("Failed to create socket");
        exit(EXIT_FAILURE);
    }

    server_address1.sin_family = AF_INET;
    server_address1.sin_addr.s_addr = INADDR_ANY;
    server_address1.sin_port = htons(SERVER_PORT1);

    if (bind(server_socket1, (struct sockaddr *)&server_address1, sizeof(server_address1)) < 0) {
        perror("Failed to bind the socket");
        exit(EXIT_FAILURE);
    }

    listen(server_socket1, 1);

    std::cout << "Instruction receiver is turned on and waiting for connection..." << std::endl;

    client_socket1 = accept(server_socket1, NULL, NULL);
    if (client_socket1 < 0) {
        perror("Failed to accept connection");
        exit(EXIT_FAILURE);
    }

    std::cout << "Instruction receiver is connected." << std::endl;

    close(server_socket1);

    std::string instructionData;
    char buffer[MAX_BUFFER_SIZE];
    while (true) {
        memset(buffer, 0, sizeof(buffer));
        ssize_t bytesRead = read(client_socket1, buffer, sizeof(buffer));
        if (bytesRead <= 0) {
            std::cout << "Connection closed." << std::endl;
            break;
        }

        instructionData += buffer;
        size_t pos = instructionData.find('\n');
        if (pos != std::string::npos) {
            std::vector<std::string> instructions;
            std::istringstream iss(instructionData);
            std::string item;
            while (std::getline(iss, item, '\n')) {
                instructions.push_back(item);
            }

            for (const auto& instruction : instructions) {
                std::vector<std::string> data;
                std::istringstream iss(instruction);
                std::string item;
                while (std::getline(iss, item, ' ')) {
                    data.push_back(item);
                }

                if (data.empty() || data[0].empty()) {
                    continue;
                }

                if (data[0] == "CMD_BUZZER") {
                    // Process CMD_BUZZER command
                } else if (data[0] == "CMD_LED") {
                    // Process CMD_LED command
                } else if (data[0] == "CMD_LED_MOD") {
                    // Process CMD_LED_MOD command
                } else if (data[0] == "CMD_HEAD") {
                    // Process CMD_HEAD command
                } else if (data[0] == "CMD_SONIC") {
                    // Process CMD_SONIC command
                } else if (data[0] == "CMD_POWER") {
                    // Process CMD_POWER command
                } else if (data[0] == "CMD_WORKING_TIME") {
                    // Process CMD_WORKING_TIME command
                }
            }

            instructionData.erase(0, pos + 1);
        }
    }

    close(client_socket1);
}
/*
int main() {
    Server server;
    server.turnOnServer();
    // ...
    server.turnOffServer();

    return 0;
}*/
