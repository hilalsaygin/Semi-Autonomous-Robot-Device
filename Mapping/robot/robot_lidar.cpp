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
#include <unistd.h>


using namespace ydlidar;

#if defined(_MSC_VER)
#pragma comment(lib, "ydlidar_sdk.lib")
#endif


int main(int argc, char *argv[])
{

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
    return 0;
  }

  CYdLidar laser;
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
    return -1;
  }

  ret = laser.turnOn();
  if (!ret)
  {
    fprintf(stderr, "Fail to start %s\n", laser.DescribeError());
    fflush(stderr);
    return -1;
  }

  // Connect to the remote control center
  std::string ipAddress = "192.168.1.115";  // IP address of the receiving computer
  int remote_port = 8080;  // Port number of the receiving computer

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

  double robot_x = 0;
  double robot_y = 0;

  int fd = open("./robot_location.txt",O_RDWR);

  if (fd == -1) {
      std::cerr << "Failed to open the file." << std::endl;
      return 1;
  }

  const int bufferSize_rl = 30;  // Set an appropriate buffer size
  char buffer_rl[bufferSize_rl];

  
  // Main loop
  while (ydlidar::os_isOk()){
    LaserScan scan;

    
    // Read the robot location file
    ssize_t bytesRead = read(fd, buffer_rl, bufferSize_rl);

    if (bytesRead == -1) {
        std::cerr << "Failed to read the file." << std::endl;
        close(fd);
        return 1;
    }

    if (laser.doProcessSimple(scan))
    {   

        // Parse robot location
        char* robot_rl_token = strtok(buffer_rl,",");
        printf("x:%s\n",robot_rl_token);
        robot_x = atof(robot_rl_token);
        robot_rl_token = strtok(NULL,"\n");
        printf("y:%s\n",robot_rl_token);
        robot_y = atof(robot_rl_token);

        // Return the start of the file
        memset(buffer_rl,0,bufferSize_rl);
        lseek(fd,0,SEEK_SET);

        
        
        // Put robot location
        ss << "robot_x: " << robot_x << ",robot_y: " << robot_y << "\n";

        // Draw the points
        for (size_t i = 0; i < scan.points.size(); ++i)
        {   
          const LaserPoint& p = scan.points.at(i);

          // Calculate X, Y coordinates from polar coordinates
          double angle_rad = p.angle;  // Angle in radians
          double distance = p.range;   // Distance in meters

          double x = distance * cos(angle_rad);
          double y = distance * sin(angle_rad);

          //printf("X: %f Y: %f\n", x, y);

          // Convert x and y to string
          ss << "x: " << x << ", y: " << y << "\n";
            
        } 
        
        std::string data = ss.str();        
        
        // Send points to the server
        ssize_t bytesSent = send(sock, data.c_str(), data.size(), 0);
        if (bytesSent == -1) {
          std::cerr << "Failed to send data" << std::endl;
          close(sock);
          return false;
        }         
  
        fflush(stdout);
    }
    else {
      fprintf(stderr, "Failed to get Lidar Data\n");
      fflush(stderr);
    }
  }

  laser.turnOff();
  laser.disconnecting();

  // Close the file using close() function
  close(fd);

  return 0;
}