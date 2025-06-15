# AirPointer - Hand Gesture Navigation System

## Project Description
An interactive system that allows users to:
- Control their computer cursor with hand gestures
- Draw on a virtual canvas using finger movements
- Perform click, scroll, and mode-switching actions

## Features
- Real-time hand tracking using MediaPipe
- Multiple gesture recognition (pointing, pinching, scrolling)
- Virtual drawing canvas with color options
- Smooth cursor movement with position interpolation
- Easy-to-use menu system for testing components

## System Requirements
- Python 3.7+
- Webcam
- Windows/macOS/Linux

## Installation
1. Clone the repository
2. Install dependencies: pip install opencv-python mediapipe numpy pyautogui


## File Structure
- `main.py` - Entry point with system menu
- `airpointer.py` - Main application logic
- `gesture_recognizer.py` - Hand gesture detection algorithms
- `hand_detection.py` - Basic hand landmark visualization
- `camera_test.py` - Webcam verification tool

## How to Run
1. Execute the main program: python main.py
2. Select from the menu:
   - Option 1: Test your camera
   - Option 2: Test hand detection
   - Option 3: Launch full AirPointer system

## Controls (AirPointer Mode)
- ???? Pinch: Left click
- ✌️ Two fingers: Scroll
- ???? Open palm: Lift pen (draw mode)
- Keyboard:
  - 'd': Toggle draw/pointer mode
  - 'c': Clear canvas (draw mode)
  - 'q': Quit

## Datasets
Uses pre-trained MediaPipe hand landmark model:
https://google.github.io/mediapipe/solutions/hands.html

## Troubleshooting
- If camera isn't detected, try `camera_test.py` first
- Ensure proper lighting for hand tracking
- Reduce background movement for better accuracy

## License
Open-source (MIT License)





