# gym_tracker
Track your movement with opencv

### Setup and running

Setup:
```bash
pip install -r requirements
```

Running:
```bash
$ python main.py [...options|...params]
```

Application parameters:
```bash
    --video, -v {VIDEO PATH}
        Select what video you want to process (Defaults to webcam)

    --tracker, -t {OPENCV TRACKER} 
        Select which tracker you want to use for tracking movement

    --exercise, -e {EXERCISE NAME}
        Exercise you want to analyze (squat, deadlift, horizontal neck movement (for testing))
```

### Webcam live version
When the application is runnig you have to press 'S' button and select the area you want to track
Press 'Q' to close all windows

### pre-registred video version
In video version firstly with left click you have to select which body part you want to use for counting reps
so, with right click you have to select the threshold the body part has to overtake to consider the rep valid
and after you have to selcect which portion of screen you want to track 