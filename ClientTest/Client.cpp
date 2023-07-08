#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>
#include <thread>
#include <vector>
#include <sstream>

class Client{
    public:
        Client();
        void turn_on_client(std::string ip);
        void turn_off_client();
        void send_data(std::string& data);
        int socket1();
        int socket();
        std::string rcv_data();
        int clientsocket1,clientsocket;
        bool tcpFlag;
};
Client::Client(){
    tcpFlag = false;
}
int socket1(){
    return clientsocket1;
}
int socket(){
    return clientsocket;
}

void Client::turn_on_client(std::string ip){
    cout << "turned on client" << endl;
    clientsocket1 = socket(AF_INET, SOCK_STREAM, 0);
    cli/* The `connectSocket` function is responsible for establishing a connection with a server using
    a client socket. It sets up the server address and port, converts the IP address to the
    appropriate format, and then attempts to connect to the server using the `connect` function.
    If the connection is successful, it returns `true`, otherwise it returns `false`. */
    entsocket = socket(AF_INET, SOCK_STREAM, 0);
    if(clientsocket1 ==-1 || clientsocket ==-1){
        cout << "Socket connection failed" << endl;
        return;
    }
        
    std::cout << ip << std::endl;
}



void Client::turn_off_client(){
    try{
        shutdown(clientsocket, 2);
        shutdown(clientsocket1, 2);
        close(clientsocket);
        close(clientsocket1);
    }catch(std::exception& e){
        std::cout << e.what() << std::endl;
    }
}

void Client::send_data(std::string& data){
    if(tcpFlag){
        try{
            send(clientsocket1, data.c_str(), data.length(), 0);

        }catch(std::exception& e){
            std::cout << e.what() << std::endl;
        }
    }
}

std::string Client::rcv_data(){
    std::string data;
    char buffer[1024];
    memset(buffer, 0 , sizeof(buffer));
    ssize_t bytesRead = recv(clientsocket1, buffer, sizeof(buffer) - 1, 0);
    if(bytesRead > 0){
        data = buffer;
        return data;

    }
    //if non data return null
    else{
        std::cout << "Client read any data"<< std::endl;

        return NULL;

    }
    /*
    while (true) {
        memset(buffer, 0, BUFFER_SIZE);
        ssize_t bytesRead = recv(clientSocket, buffer, BUFFER_SIZE - 1, 0);
        if (bytesRead == -1) {
            std::cerr << "Failed to read data from the server." << std::endl;
            break;
        } else if (bytesRead == 0) {
            std::cout << "Server closed the connection." << std::endl;
            break;
        }

    receivedData += buffer;
        }
    */
}
