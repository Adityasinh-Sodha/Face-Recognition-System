# Face-Recognition-System
This is a basic Face recognition system with its own local-host server by Adityasinh Sodha 

## Overview
This project implements a face recognition system using a webcam. It can recognize registered faces and display their details, while prompting for input when a new face is detected. A localhost web server is also integrated to show real-time updates of recognized faces and their associated information.

## Features
- **Face Recognition**: Detects and identifies faces using webcam.
- **Real-time Updates**: Displays recognized faces and their details in real-time on a webpage.
- **New Face Detection**: Automatically prompts for input when a new face is detected.
- **Local Web Server**: Runs a localhost web server that shows recognized faces on a webpage while the code is running.

## Technologies Used
- Python
- OpenCV (for face detection)
- Flask (for the web server)
- SQLite (for face data storage)

## Requirements
- Python 3.x
- OpenCV
- Flask
- SQLite

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/AdityaSodha/Face-Recognition-System
    cd Face-Recognition-System
    ```
2. Install required dependencies:
    ```bash
    pip install opencv-python flask
    pip install opencv-python-headless
    pip install face_recognition

    ```
3. Run the face recognition script:
    ```bash
    python3 FRS.py
    ```
4. Open a browser and go to `http://localhost:5000` to see real-time face recognition updates.

### How It Works
- The script starts webcam-based face recognition using OpenCV.
- When a face is detected, it checks the database to see if it's registered.
    - If the face is registered, it displays the details.
    - If the face is new, it prompts for input to store the details.
- A localhost Flask server runs concurrently, showing the list of recognized faces and their details in real-time.
- The server stops automatically when the script is stopped.

## Contribution
Feel free to fork the repository and make improvements. Contributions are welcome!

## License
This project is licensed under the MIT License.
