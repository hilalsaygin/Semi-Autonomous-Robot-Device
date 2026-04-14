# Semi-Autonomous Robot Device (RoboDog)

Contains the source code and documentation for a semi-autonomous robotic system developed as a **CSE396 Computer Engineering Project**. The project features a hybrid control system enabling both manual teleoperation and autonomous navigation using AI-driven object detection and Lidar-based mapping.

---

## 🚀 Priority Setup

1.  **Power:** Ensure batteries are correctly inserted into the slot.
2.  **Activation:** Press the **CTRL** key on the robot, then press the **LOAD** key.
3.  **Hardware Connections:** Connect to the Raspberry Pi via HDMI and connect the Lidar sensor to the Raspberry Pi using a Type-C entry.
4.  **Network:** Ensure the robot has an active internet connection.

---

## 🛠️ Software Installation

### Server Side (Raspberry Pi)
The server logic runs on the robot's Raspberry Pi.
* Establish a connection using **VNC Viewer** via the robot's IP address.
* The HDMI cable can be disconnected once the VNC connection is stable.
* The server code is located at: `/home/grup3/oto_robot/Code`.

### Client Side (Ubuntu)
The client requires a computer running **Ubuntu**.
1.  **Clone the Repository:** Download the client codes from the GitHub repository.
2.  **Install Dependencies:** Run the following commands in order:
    ```bash
    sudo apt install python3-pip
    pip install yolov5
    pip install keras
    pip install tensorflow
    pip uninstall opencv-python
    pip install opencv-python-headless
    pip3 install pyqt5  # If QT errors occur
    ```
3.  **Optional Acceleration:** Nvidia CUDA can be installed to speed up image processing and mapping.

---

## 🔧 Configuration and Execution

### 1. Running the Server
* Navigate to the server directory and compile the script:
    ```bash
    chmod +x serverMake.sh
    ./serverMake.sh
    ```
* Verify the server is listening on the designated port (default is often 8066).
* To change the port, edit `int remote_port` in `/Server/Mapping/robot/robot_lidar.cpp` and re-run the script.

### 2. Running the Client
* Ensure the Raspberry Pi and the remote laptop are on the **same WiFi network**.
* Identify the Raspberry Pi IP using `hostname -I` on the Pi.
* Update `self.ipAddress` and `self.remote_port` in `Main.py` and `ui_client.py` within the Client directory.
* Execute the interface:
    ```bash
    python3 Main.py
    ```

---

## 🎮 Controller Guide

### User Interface Features
* **Manual Control:** Use directional buttons (Forward, Backward, Left, Right, Step Left/Right) for teleoperation.
* **Autonomous Mode:** Press the **Autonomous** button to begin automatic navigation. The robot will move forward and steer away from obstacles independently.
* **Mapping (Left Frame):** Displays real-time environment data extracted by the mapping algorithm.
* **Object Detection (Right Frame):** Displays a camera feed processed with object detection to identify hazards.
* **Connection:** Enter the server IP and click **Connect** to link the client to the robot.

---

## 🛑 Termination Procedure
1.  Close the **Client window**.
2.  Close the **Terminal**.
3.  Close the **Server** program on the Raspberry Pi.
