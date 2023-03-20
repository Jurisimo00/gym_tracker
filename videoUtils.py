# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import PoseTracking

def video(tracker,args):
    initBB = None
    first = True
    pose = True
    # construct the argument parse and parse the arguments
    # start the file video stream thread and allow the buffer to
    # start to fill
    print("[INFO] starting video file thread...")
    fvs = FileVideoStream(args["video"]).start()
    time.sleep(1.0)
    # start the FPS timer
    fps = FPS().start()
    # loop over frames from the video file stream
    while fvs.more():
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale (while still retaining 3
        # channels)
        frame = fvs.read()
        frame = imutils.resize(frame, width=450)
        (H, W) = frame.shape[:2]
        if pose:
            frame, land = PoseTracking.process(frame)
            a = np.array([int(land[23].x*W),int(land[23].y*H)])
            b = np.array([int(land[25].x*W),int(land[25].y*H)])
            c = np.array([int(land[27].x*W),int(land[27].y*H)])
            cv2.circle(frame, (a[0], a[1]), 12,
                (0, 255, 0), 2)
            check, angle = PoseTracking.getAngle(a,b,c)
            if(check):
                cv2.putText(frame, f'{int(angle)}',(b[0],b[1]),
                        cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 0, 255), 2)
        #frame = np.dstack([frame, frame, frame])	
        # show the frame and update the FPS counter
        cv2.waitKey(1)
        fps.update()
        # check to see if we are currently tracking an object
        if initBB is not None:
            # grab the new bounding box coordinates of the object
            (success, box) = tracker.update(frame)
            # check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                    (0, 255, 0), 2)
                centerX = np.rint((x + (w/2))).astype(int)
                centerY = np.rint((y + (y/2))).astype(int)
                #print(centerX,centerY)
                if first:
                    points = np.array([[centerX,centerY]],dtype=np.uint8)
                    first=False
                points = np.append(points,[[centerX,centerY]], axis=0)
                cv2.polylines(frame, 
                [points], 
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
        key = cv2.waitKey(1) & 0xFF
        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):
            print("s")
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                showCrosshair=True)
            #when track movement don't use poseTracking
            pose = False
            # start OpenCV object tracker using the supplied bounding box
            # coordinates
            tracker.init(frame, initBB)
                # if the `q` key was pressed, break from the loop
        elif key == ord("q"):
            break
        # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    # do a bit of cleanup
    cv2.destroyAllWindows()
    fvs.stop()
