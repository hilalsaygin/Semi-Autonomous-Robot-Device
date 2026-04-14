# Semi-Autonomous Robot Device (RoboDog)

This repository contains the source code and documentation for a semi-autonomous robotic system developed as a **CSE396 Computer Engineering Project**[cite: 1, 2, 3].The project features a hybrid control system enabling both manual teleoperation and autonomous navigation using AI-driven object detection and Lidar-based mapping [cite: 97-105, 120-122].

---

## 🚀 Priority Setup

1. **Power:** Ensure batteries are correctly inserted into the slot[cite: 16, 17].
2. **Activation:** Press the **CTRL** key on the robot, then press the **LOAD** key[cite: 18].
3. **Hardware Connections:** Connect to the Raspberry Pi via HDMI and connect the Lidar sensor to the Raspberry Pi using a Type-C entry[cite: 19].
4. **Network:** Ensure the robot has an active internet connection[cite: 20].

---

## 🛠️ Software Installation

### Server Side (Raspberry Pi)
The server logic runs on the robot's Raspberry Pi.
*Establish a connection using **VNC Viewer** via the robot's IP address[cite: 21].
*The HDMI cable can be disconnected once the VNC connection is stable[cite: 22].
*The server code in raspberry pi is located at: `/home/grup3/oto_robot/Code`[cite: 31].

### Client Side (Ubuntu)
The client requires a computer running **Ubuntu**[cite: 50].
1. **Clone the Repository:** Download the client codes from the GitHub repository[cite: 51, 52].
2. **Install Dependencies:** Run the following commands in order[cite: 54]:
    ```bash
   sudo apt install python3-pip [cite: 55]
    pip install yolov5 [cite: 56]
    pip install keras [cite: 57]
    pip install tensorflow [cite: 58]
    pip uninstall opencv-python [cite: 59]
    pip install opencv-python-headless [cite: 60]
    pip3 install pyqt5  # If QT errors occur [cite: 61]
    ```
3.  **Optional Acceleration:** Nvidia CUDA can be installed to speed up image processing and mapping[cite: 62, 63, 64].

---

## 🔧 Configuration and Execution

### 1. Running the Server
*Navigate to the server directory [cite: 31] and compile the script:
    ```bash
   chmod +x serverMake.sh [cite: 33]
    ./serverMake.sh [cite: 35]
    ```
* Verify the server is listening on the designated port (default is often 8066)[cite: 36, 45].
* To change the port, edit `int remote_port` in `/Server/Mapping/robot/robot_lidar.cpp` and re-run the script[cite: 39, 45, 46, 47].

### 2. Running the Client
*Ensure the Raspberry Pi and the remote laptop are on the **same WiFi network**[cite: 26, 67].
*Identify the Raspberry Pi IP using `hostname -I` on the Pi[cite: 69, 70].
*Update `self.ipAddress` and `self.remote_port` in `Main.py` and `ui_client.py` within the Client directory[cite: 71, 80, 81, 87].
* Execute the interface:
    ```bash
   python3 Main.py [cite: 92]
    ```

---

## 🎮 Controller Guide

### User Interface Features
***Manual Control:** Use directional buttons (Forward, Backward, Left, Right, Step Left/Right) for teleoperation[cite: 99, 100, 101].
***Autonomous Mode:** Press the **Autonomous** button to begin automatic navigation[cite: 102].The robot will move forward and steer away from obstacles independently[cite: 103, 104].
***Mapping (Left Frame):** Displays real-time environment data extracted by the mapping algorithm[cite: 120].
***Object Detection (Right Frame):** Displays a camera feed processed with object detection to identify hazards[cite: 121, 122].
***Connection:** Enter the server IP and click **Connect** to link the client to the robot[cite: 106, 107].

---

## 🛑 Termination Procedure
1. Close the **Client window**[cite: 138].
2. Close the **Terminal**[cite: 138].
3. Close the **Server** program on the Raspberry Pi[cite: 139].
