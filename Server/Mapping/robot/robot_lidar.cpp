#include "CYdLidar.h"
#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>
#include <core/base/timer.h>
#include <core/common/ydlidar_help.h>
#include <cmath>
#include <sstream>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <vector>
#include <algorithm>


constexpr int BUFFER_SIZE = 50000;
using namespace ydlidar;
#if defined(_MSC_VER)
#pragma comment(lib, "ydlidar_sdk.lib")
#endif
//Set lidar settings
CYdLidar laser;
int serverSock;
// Function to handle the SIGPIPE signal
void sigpipeHandler(int signal)
{
    //laser.turnOff();
    //laser.disconnecting();
    close(serverSock);
    std::cerr << "Received SIGPIPE signal" << std::endl;

    // Print a message to indicate the signal handling
}
bool sortcol(const std::vector<double>& v1, const std::vector<double>& v2)
{
	return v1[0] < v2[0];
}
int main(int argc, char *argv[])
{
  // Register the signal handler for SIGPIPE
  signal(SIGPIPE, sigpipeHandler);
  signal(SIGINT, sigpipeHandler);
  signal(SIGTSTP, sigpipeHandler);



  int remote_port = 8655;

  // Set lidar usb port
  std::string port;
  ydlidar::os_init();

  std::map<std::string, std::string> ports =
      ydlidar::lidarPortList();
  std::map<std::string, std::string>::iterator it;

  if (ports.size() == 1)
  {
    port = ports.begin()->second;
  }
  else
  {
    int id = 0;

    for (it = ports.begin(); it != ports.end(); it++)
    {
      printf("[%d] %s %s\n", id, it->first.c_str(), it->second.c_str());
      id++;
    }

    if (ports.empty())
    {
      printf("Not Lidar was detected. Please enter the lidar serial port:");
      std::cin >> port;
    }
    else
    {
      while (ydlidar::os_isOk())
      {
        printf("Please select the lidar port:");
        std::string number;
        std::cin >> number;

        if ((size_t)atoi(number.c_str()) >= ports.size())
        {
          continue;
        }

        it = ports.begin();
        id = atoi(number.c_str());

        while (id)
        {
          id--;
          it++;
        }

        port = it->second;
        break;
      }
    }
  }

  // Set lidar baudrate (115220 for X2 Lidar)
  int baudrate = 115200;
  printf("Baudrate: %d\n",baudrate);

  if (!ydlidar::os_isOk())
  {
    return 0;
  }

  bool isSingleChannel = true;
  printf("is Single Channel: %d\n",isSingleChannel);

  if (!ydlidar::os_isOk())
  {
    //laser.turnOff();
    //laser.disconnecting();
    return 0;
  }

  
  //////////////////////string property/////////////////
  /// lidar port
  laser.setlidaropt(LidarPropSerialPort, port.c_str(), port.size());
  /// ignore array
  std::string ignore_array;
  ignore_array.clear();
  laser.setlidaropt(LidarPropIgnoreArray, ignore_array.c_str(),
                    ignore_array.size());

  //////////////////////int property/////////////////
  /// lidar baudrate
  laser.setlidaropt(LidarPropSerialBaudrate, &baudrate, sizeof(int));
  /// tof lidar
  int optval = TYPE_SCL;
  laser.setlidaropt(LidarPropLidarType, &optval, sizeof(int));
  /// device type
  optval = YDLIDAR_TYPE_SERIAL;
  laser.setlidaropt(LidarPropDeviceType, &optval, sizeof(int));
  /// sample rate
  optval = isSingleChannel ? 3 : 4;
  laser.setlidaropt(LidarPropSampleRate, &optval, sizeof(int));
  /// abnormal count
  optval = 4;
  laser.setlidaropt(LidarPropAbnormalCheckCount, &optval, sizeof(int));
  /// Intenstiy bit count
  optval = 10;
  laser.setlidaropt(LidarPropIntenstiyBit, &optval, sizeof(int));

  //////////////////////bool property/////////////////
  /// fixed angle resolution
  bool b_optvalue = true;
  laser.setlidaropt(LidarPropFixedResolution, &b_optvalue, sizeof(bool));
  /// rotate 180
  laser.setlidaropt(LidarPropReversion, &b_optvalue, sizeof(bool));
  /// Counterclockwise
  laser.setlidaropt(LidarPropInverted, &b_optvalue, sizeof(bool));
  b_optvalue = true;
  laser.setlidaropt(LidarPropAutoReconnect, &b_optvalue, sizeof(bool));
  /// one-way communication
  laser.setlidaropt(LidarPropSingleChannel, &isSingleChannel, sizeof(bool));
  /// intensity
  b_optvalue = false;
  laser.setlidaropt(LidarPropIntenstiy, &b_optvalue, sizeof(bool));
  /// Motor DTR
  b_optvalue = false;
  laser.setlidaropt(LidarPropSupportMotorDtrCtrl, &b_optvalue, sizeof(bool));
  /// HeartBeat
  b_optvalue = false;
  laser.setlidaropt(LidarPropSupportHeartBeat, &b_optvalue, sizeof(bool));

  //////////////////////float property/////////////////
  /// unit: °
  float f_optvalue = 180.0f;
  laser.setlidaropt(LidarPropMaxAngle, &f_optvalue, sizeof(float));
  f_optvalue = -180.0f;
  laser.setlidaropt(LidarPropMinAngle, &f_optvalue, sizeof(float));
  /// unit: m
  f_optvalue = 64.f;
  laser.setlidaropt(LidarPropMaxRange, &f_optvalue, sizeof(float));
  f_optvalue = 0.05f;
  laser.setlidaropt(LidarPropMinRange, &f_optvalue, sizeof(float));


  laser.enableGlassNoise(false);
  laser.enableSunNoise(false);
  laser.setBottomPriority(true);

  bool ret = laser.initialize();
  if (!ret)
  {
    fprintf(stderr, "Fail to initialize %s\n", laser.DescribeError());
    fflush(stderr);
    //laser.turnOff();
    //laser.disconnecting();
    return -1;
  }

  ret = laser.turnOn();
  if (!ret)
  {
    fprintf(stderr, "Fail to start %s\n", laser.DescribeError());
    fflush(stderr);
   // laser.turnOff();
    //laser.disconnecting();
    return -1;
  }


  // Create server socket
  serverSock = socket(AF_INET, SOCK_STREAM, 0);
  if (serverSock == -1) {
      std::cerr << "Failed to create socket" << std::endl;
      return false;
  }

  // Bind socket
  sockaddr_in serverAddr{};
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_addr.s_addr = INADDR_ANY;
  serverAddr.sin_port = htons(remote_port);

  if (bind(serverSock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
      std::cerr << "Binding failed" << std::endl;
      close(serverSock);
    //   laser.turnOff();
    //laser.disconnecting();
      
      return false;
  }

  // Listen the server
  if (listen(serverSock, 1) < 0) {
      std::cerr << "Listening failed" << std::endl;
      close(serverSock);
      // laser.turnOff();
    //laser.disconnecting();
      return false;
  }

  std::cout << "Server listening on port " << remote_port << std::endl;


  // Main things start
  double robot_x = 0;
  double robot_y = 0;
  const int bufferSize_rl = 30;
  char buffer_rl[bufferSize_rl];

  while (ydlidar::os_isOk()){
    sockaddr_in clientAddr{};
    socklen_t addrLen = sizeof(clientAddr);
    int clientSock = accept(serverSock, (struct sockaddr*)&clientAddr, &addrLen);
    if (clientSock < 0) {
        std::cerr << "Failed to accept connection" << std::endl;
        // laser.turnOff();
      //  laser.disconnecting();
        return false;
    }

    printf("Bağlandı\n");

    // Main loop
    while (true){       

      LaserScan scan;
      double robot_location_buffer[3];
      memset(robot_location_buffer,0,sizeof(robot_location_buffer));

      // Open the robot location file
      int fd = open("/home/grup3/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server/Mapping/robot/build/robot_location.txt",O_RDWR);
        
     int dosya = open("/home/grup3/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/Code/Server/Mapping/robot/build/lidardata.txt",O_RDWR);
       if (fd == -1) {
          std::cerr << "Failed to open the file." << std::endl;
          return 1;
      }
     if (dosya == -1) { printf("Lidarr data file failed to open!"); return 1; }
    
        
       memset(buffer_rl,0,sizeof(buffer_rl));
   
      // Read the robot location file
      ssize_t bytesRead = read(fd, buffer_rl, bufferSize_rl);
      buffer_rl[bytesRead]='\0';
      //printf("size: %d  %s ****\n",bytesRead,buffer_rl); 

      char *token = strtok(buffer_rl, ",");
      int i=0;
        while (token != NULL) { // Virgülle ayrılan değerleri parçala
            robot_location_buffer[i] = atof(token);
            //printf("%d  : %lf\n",i,robot_location_buffer[i] );

            i++;
            token = strtok(NULL, ",");
           
      }
      // Close the file using close() function
      close(fd);
      

      if (bytesRead == -1) {
          std::cerr << "Failed to read the file." << std::endl;
          close(fd);
          return 1;
      }

      if (laser.doProcessSimple(scan))
      {   
          // Point sayısını client'a gönder
          int point_count = scan.points.size();
          ssize_t bytesSent_pc = send(clientSock, &point_count, sizeof(point_count), 0);
          if (bytesSent_pc == -1) {
            std::cerr << "Failed to send data" << std::endl;
            close(clientSock);
            break;
          } 
          
          //printf("Point count : %d\n",point_count);
          //printf("bytesSent_pc : %lu\n",bytesSent_pc);

          // Eğer point sayısı valid ise
          if(point_count > 0 && point_count < 20000) {

            // Robot konumunu gönder
            ssize_t bytesSent_rl = send(clientSock, robot_location_buffer, sizeof(robot_location_buffer), 0);
            if (bytesSent_rl == -1) {
              std::cerr << "Failed to send data" << std::endl;
              close(clientSock);
              break;
            } 

            // Bulunan pointleri gönder

            char buffer[10];
            double point_buffer[point_count][2];
            //double angle_dist[point_count][2];
            
            std::vector<std::vector<double> > vec(point_count);

            for (size_t i = 0; i < scan.points.size(); ++i)
            { 
              memset(point_buffer[i],0,sizeof(point_buffer[i]));

              const LaserPoint& p = scan.points.at(i);

              double angle_rad = p.angle;
                        
              double distance = p.range;
              double updated_angle = angle_rad + (robot_location_buffer[2]*3.1415)/180 ;
              //printf("%lf updated, buffer: %lf\n",updated_angle,robot_location_buffer[2]);

              double x = distance * cos(updated_angle);
              double y = distance * sin(updated_angle);

              point_buffer[i][0] = x;
              point_buffer[i][1] = y;
              
              
              
              
              

              vec[i] = std::vector<double>(2);
              double angle= (angle_rad*180)/3.1415;

               if((angle <= -100.0 && angle >= -175.0 )|| (angle <=175.0 && angle >= 100.0))
               {
                        vec[i][0]=distance;
                        vec[i][1]=angle;
               }
            }   

            // sort angle_dist by first demension(dist)
            std::sort(vec.begin(), vec.end(), sortcol);
        
            std::string str = std::to_string(vec[point_count-1][1]);
            char digits[str.length()];
            std::strncpy(digits, std::to_string(vec[point_count-1][1]).c_str(), sizeof(digits));

           if(vec[point_count-1][1]<0.0) ssize_t bytes_written = write(dosya, digits,8);
           else  ssize_t bytes_written = write(dosya, digits, 7);
            //fprintf(dosya, "%.3f\n", (vec[point_count-1][1]));
            //printf("largest: %.3f\n", vec[point_count-1][1]);

            close(dosya);
            
            
            ssize_t bytesSent = send(clientSock, point_buffer, sizeof(point_buffer), 0);
            if (bytesSent == -1) {
              std::cerr << "Failed to send data" << std::endl;
              close(clientSock);
              break;
            }
            memset(point_buffer , 0 , sizeof(point_buffer)); 
            memset(robot_location_buffer,0,sizeof(robot_location_buffer));

          }

          fflush(stdout);
      }
      else {
        fprintf(stderr, "Failed to get Lidar Data\n");
        fflush(stderr);
      
      }


    }
    
  }
  

  laser.turnOff();
  laser.disconnecting();

  

  return 0;
}

