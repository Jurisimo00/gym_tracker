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

##webcam live version
python3 main.py

##pre-registred video version
python3 main.py --video {VIDEO PATH}
