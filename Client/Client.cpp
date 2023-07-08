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
        std::string rcv_data();
        int clientsocket1,clientsocket;
        bool tcpFlag;
};
Client::Client(){
    tcpFlag = false;
}

void Client::turn_on_client(std::string ip){
    cout << "turned on client" << endl;
    clientsocket1 = socket(AF_INET, SOCK_STREAM, 0);
    clientsocket = socket(AF_INET, SOCK_STREAM, 0);
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
    }
    return data;
}
