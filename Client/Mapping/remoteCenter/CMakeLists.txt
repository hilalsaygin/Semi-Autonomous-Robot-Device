cmake_minimum_required(VERSION 2.8)
project(remote_control_center_mapping)

# Set C++ standard
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
add_definitions(-std=c++14) # Use C++14

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}
)

# Find SFML package
find_package(SFML 2.5 COMPONENTS system window graphics REQUIRED)

# Include directories
include_directories(${SFML_INCLUDE_DIRS})

add_executable(remote_control_center_mapping remote_control_center_mapping.cpp)

# Link ydlidar_sdk and SFML libraries
target_link_libraries(remote_control_center_mapping sfml-system sfml-window sfml-graphics)
