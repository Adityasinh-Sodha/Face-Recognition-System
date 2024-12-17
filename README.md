# Face-Recognition-System
This is a advance Face recognition system by Adityasinh Sodha 

## Overview
This project implements a face recognition system using a webcam. It can recognize registered faces and display their details, while prompting for input when a new face is detected.

## Features
- **Face Recognition**: Detects and identifies faces using webcam.
- **Real-time Updates**: Displays recognized faces and their details in real-time.
- **New Face Detection**: Automatically prompts for input when a new face is detected.

## Technologies Used
- Python
- OpenCV (for face detection)
- face_recognition (for face recognition)
- SQLite (for face data storage)

## Requirements
- Windows 10/11 64bit or Linux amd64
- Python 3.11
-  [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (FOR WINDOWS ONLY)

## Installation
### Linux
1. Clone the repository:
    ```bash
    git clone https://github.com/Adityasinh-Sodha/Face-Recognition-System
    cd Face-Recognition-System
    ```   
2. Install required dependencies:
    ```bash
    pip install opencv-python flask
    pip install opencv-python-headless
    sudo apt install libgl1-mesa-glx
    pip install cmake
    pip install face_recognition
    pip install pillow

    ```
3. Run the face recognition script:
    ```bash
    python3 main.py
    ```
### Windows
1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   and download **Desktop development with C++** (ONLY FOR WINDOWS 10/11)

2. Install [python](https://www.python.org/downloads/windows/)
   and confiure pip

3. Open cmd and install required dependencies:
    ```bash
    pip install opencv-python flask
    pip install opencv-python-headless
    pip install cmake
    pip install face_recognition
    pip install pillow

    ```
4. Run the command ```
   python main.py```
6. Ragister your face and enjoy.

### How It Works
- The script starts webcam-based face recognition using OpenCV.
- When a face is detected, it checks the database to see if it's registered.
    - If the face is registered, it displays the details.
    - If the face is new, it prompts for input to store the details.

## Contribution
Feel free to fork the repository and make improvements. Contributions are welcome!

## License
This project is licensed under the MIT License.
## Author
Developed by **Adityasinh**.
