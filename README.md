# Hand Gesture Recognition using MediaPipe and OpenCV

## Project Overview
This project is a real-time Hand Gesture Recognition system developed using Python, OpenCV, and MediaPipe. The application detects hand landmarks through a webcam, identifies different finger combinations, and maps them to predefined gestures. Each recognized gesture displays a custom message on the screen and converts the text into speech using a text-to-speech engine.

## Features
* Real-time hand tracking using webcam
* Hand landmark detection with MediaPipe
* Recognition of multiple hand gestures
* Custom text messages for different gestures
* Voice output using Text-to-Speech (pyttsx3)
* Visual display of hand landmarks and connections
* Automatic model download if not available
  
## Technologies Used
* Python
* OpenCV
* MediaPipe
* pyttsx3
* urllib
* 
## How It Works
1. The webcam captures live video frames.
2. MediaPipe detects hand landmarks from each frame.
3. The program checks which fingers are raised.
4. A predefined gesture is identified based on the finger positions.
5. The corresponding message is displayed on the screen and spoken aloud.
6. Hand landmarks and connections are drawn for visualization.
7. 
## Applications
* Human-Computer Interaction (HCI)
* Gesture-based control systems
* Accessibility and assistive technology
* Educational projects
* Interactive AI applications
