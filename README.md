# gym_tracker
Track your movement with opencv

Libraries to install:
opencv
imutils
mediapipe

For run the application:

parameters:
--video, -v {VIDEO PATH} -> select what video you want to process
--tracker, -t {OPENCV TRACKER} -> select which tracker you want to use for tracking movement

**Webcam live version**
python3 main.py
when the application is runnig you have to press 'S' button and select the area you want to track
Press 'Q' to close all windows

**Pre-registred video version**
python3 main.py --video {VIDEO PATH}
