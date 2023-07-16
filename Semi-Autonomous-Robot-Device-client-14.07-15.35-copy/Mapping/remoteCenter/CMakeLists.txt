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

# Find Qt packages
find_package(Qt5 COMPONENTS Core Widgets REQUIRED)

# Include directories
include_directories(${SFML_INCLUDE_DIRS})

# Include directories for Qt
include_directories(${Qt5_INCLUDE_DIRS})

# Add the SFMLCanvas header file to the sources
set(SOURCES
    remote_control_center_mapping.cpp
    QSFMLCanvas.h
)

add_executable(remote_control_center_mapping ${SOURCES})

# Link SFML and Qt libraries
target_link_libraries(remote_control_center_mapping sfml-system sfml-window sfml-graphics Qt5::Core Qt5::Widgets)
