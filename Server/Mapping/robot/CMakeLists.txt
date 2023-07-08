cmake_minimum_required(VERSION 2.8)
project(robot_lidar)

# Set C++ standard
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
add_definitions(-std=c++14) # Use C++14

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}
)

############## YDLIDAR SDK START#####################################
# Find ydlidar_sdk package
find_package(ydlidar_sdk REQUIRED)

# Include directories
include_directories(${YDLIDAR_SDK_INCLUDE_DIRS})

# Link library directories
link_directories(${YDLIDAR_SDK_LIBRARY_DIRS})

############## YDLIDAR SDK END#####################################

add_executable(robot_lidar robot_lidar.cpp)

# Link ydlidar_sdk and SFML libraries
target_link_libraries(robot_lidar ${YDLIDAR_SDK_LIBRARIES} )
