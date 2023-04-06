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
--exercise, -e -> say which exercise you want to anlize (squat,deadlift, horizontal neck movement(for testing))

**webcam live version**
python3 main.py
when the application is runnig you have to press 'S' button and select the area you want to track
Press 'Q' to close all windows

**pre-registred video version**
python3 main.py --video {VIDEO PATH}
in video version firstly with left click you have to select which body part you want to use for counting reps
so, with right click you have to select the threshold the body part has to overtake to consider the rep valid
and after you have to selcect which portion of screen you want to track 
