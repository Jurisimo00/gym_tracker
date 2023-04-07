# import the necessary packages
import os
import time

import cv2
import imutils
import numpy as np
from imutils.video import FPS
from mediapipe.python.solutions.pose import PoseLandmark

import PoseTracking
from RepsCounter import RepsCounter
from WebcamMultiThread import WebcamStream


def stream(tracker,args):
    initBB = None
    first = True
    pose = True
    start=False
    counter = RepsCounter(args["exercise"])
    webcam_stream=WebcamStream(stream_id=0)
    webcam_stream.start()
    start_time=time.time()
    while True:
        frame = webcam_stream.read()
        #frame = frame[1]
        # check to see if we have reached the end of the stream
        if frame is None:
            break
        # resize the frame (so we can process it faster) and grab the
        # frame dimensions
        frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]
        if pose:
            frame, skeleton, land = PoseTracking.process(frame)
            if(land):
                a = np.array([int(land[PoseLandmark.LEFT_HIP].x*W),int(land[PoseLandmark.LEFT_HIP].y*H)])
                b = np.array([int(land[PoseLandmark.LEFT_KNEE].x*W),int(land[PoseLandmark.LEFT_KNEE].y*H)])
                c = np.array([int(land[PoseLandmark.LEFT_ANKLE].x*W),int(land[PoseLandmark.LEFT_ANKLE].y*H)])
                cv2.circle(frame, (a[0], a[1]), 12,
                    (0, 255, 0), 2)
                check, angle = PoseTracking.getAngle(a,b,c)
                if(check):
                    cv2.putText(frame, f'{int(angle)}',(b[0],b[1]),
                            cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 0, 255), 2)
                while(not start):
                    cv2.imshow("frame", frame)
                    print("Press any key to start")
                    if cv2.waitKey(0):
                        start = True
                        #to review
                        # if ((cv2.waitKey(1) & 0xFF) == ord("n")):
                        #     print("n")
                        #     counter = RepsCounter("neck")
                        # else:
                        #     counter = RepsCounter(args["exercise"])
                        #     print("default")
                        cv2.destroyAllWindows()
                        break
                angles=PoseTracking.getAngles(W,H,land)
                counter.count(angles,land)
                toll, axis = counter.getToll()
                if(axis == 0):
                    cv2.line(frame,(int(toll*1.2*W),0),(int(toll*1.2*W),H),(0,255,0),5)
                else:
                    cv2.line(frame,(0,int(toll*1.2*H)),(H,int(toll*1.2*H)),(0,255,0),5)
                cv2.putText(frame, "reps:{}".format(counter.get()), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        # check to see if we are currently tracking an object
        if initBB is not None:
            # grab the new bounding box coordinates of the object
            (success, box) = tracker.update(frame)
            # check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                    (0, 255, 0), 2)
                centerX = int((x + (w/2)))
                centerY = int((y + (h/2)))
                if first:
                    print(centerX,centerY)
                    points = np.array([[centerX,centerY]],dtype=np.uint8)
                    first=False
                points = np.append(points,[[centerX,centerY]], axis=0)
                cv2.polylines(frame, 
                [points[1:len(points)]], 
                isClosed = False,
                color = (0,255,0),
                thickness = 3, 
                lineType = cv2.LINE_AA)
            # update the FPS counter
            fps.update()
            fps.stop()
            # initialize the set of information we'll be displaying on
            # the frame
            info = [
                ("Tracker", args["tracker"]),
                ("Success", "Yes" if success else "No"),
                ("FPS", "{:.2f}".format(fps.fps())),
            ]
            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        # show the output frame
        #frame = cv2.flip(frame,1)
        cv2.imshow("Frame", frame)
        cv2.imshow("Skeleton", skeleton)
        key = cv2.waitKey(1) & 0xFF
        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                showCrosshair=True)
            #when track movement don't use poseTracking
            pose = False
            # start OpenCV object tracker using the supplied bounding box
            # coordinates, then start the FPS throughput estimator as well
            tracker.init(frame, initBB)
            fps = FPS().start()
            
                # if the `q` key was pressed, break from the loop
        elif key == ord("q"):
            break
        #Restart application
        if key == ord("r"):
            webcam_stream.stop()
            cv2.destroyAllWindows()
            os.system('python3 "main.py"')
            break
    # if we are using a webcam, release the pointer
    webcam_stream.stop()
    cv2.destroyAllWindows()
