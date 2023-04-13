# import the necessary packages
import os
import time
import numpy as np
from imutils.video import FPS
from RepsCounter import RepsCounter
from WebcamMultiThread import WebcamStream

# import the necessary packages
from imutils.video import FPS
import numpy as np
import time
import cv2
from RepsCounter import RepsCounter
from videoThread import FileVideoStream as vt
import gui

is_selected_pos=False
toll=0
body_index=0
def start(stream,args):
    pose = True
    # construct the argument parse and parse the arguments
    # start the file video stream thread and allow the buffer to
    # start to fill
    print("[INFO] starting video file thread...")
    #fvs = FileVideoStream(args["video"]).start()
    startWindow=gui.createStartWindow()
    while True:
        event, values = startWindow.read(timeout=20)
        if event != gui.sg.WIN_CLOSED and event != "__TIMEOUT__":
            print(event)
            if(values["Pose"] == False):
                pose = False
            counter = RepsCounter(event.lower())
            startWindow.close()
            break
    if(stream):
        fvs = WebcamStream(pose,stream_id=0)
        fvs.start()
    else:
        fvs = vt(args["video"], pose).start()
    time.sleep(1.0)
    window=gui.createWIndow()

    # start the FPS timer
    fps = FPS().start()
    startFrame, skeleton, land, _ = fvs.read()
    cv2.namedWindow('Frame')
    cv2.setMouseCallback('Frame',getBodyIndex, param=(land,startFrame))
    #select which body part you want to use for the RepsCounter
    while(not is_selected_pos):
        startFrame = cv2.addWeighted(startFrame,1.0,skeleton,0.3,0)
        cv2.imshow('Frame',startFrame)
        print("wait")
        event, _ = window.read(timeout=20)
        window["-OUTPUT-"].update("Select body part")
        if cv2.waitKey(20) & 0xFF == 27:
            break
    (H, W) = startFrame.shape[:2]
    bodyPoints=np.array([[int(land[body_index].x*W),int(land[body_index].y*H)]],dtype=np.uint8)
    cv2.destroyAllWindows()
    # loop over frames from the video file stream
    while True:
        frame, skeleton, land, angles = fvs.read()
        if(stream):
            if frame is None:
                break
        else:
            if(not fvs.more()):
                break
        event, values = window.read(timeout=20)
        if event == "Exit" or event == gui.sg.WIN_CLOSED:
            break
        #frame = imutils.resize(frame, width=450)
        (H, W) = frame.shape[:2]
        if(land):
            #left
            window["-LEFT_KNEE-"].update(str(angles[3]))
            cv2.circle(skeleton, (int(land[25].x*W),int(land[25].y*H)), 2,
                (0, 255, 0), 2)
            window["-LEFT_ELBOW-"].update(str(angles[0]))
            cv2.circle(skeleton, (int(land[13].x*W),int(land[13].y*H)), 2,
                (0, 255, 0), 2)
            #right
            window["-RIGHT_KNEE-"].update(str(angles[2]))
            cv2.circle(skeleton, (int(land[26].x*W),int(land[26].y*H)), 2,
                (0, 255, 0), 2)
            window["-RIGHT_ELBOW-"].update(str(angles[1])) 
            cv2.circle(skeleton, (int(land[14].x*W),int(land[14].y*H)), 2,
                (0, 255, 0), 2)
            #count reps
            #print(angles[3])
            counter.count(angles,land)
            window["-REPS-"].update(counter.get())
            # toll, axis = counter.getToll()
            # if(axis == 0):
            #     cv2.line(frame,(int(toll*1.2*W),0),(int(toll*1.2*W),H),(0,255,0),5)
            # else:
            #     cv2.line(frame,(0,int(toll*1.2*H)),(H,int(toll*1.2*H)),(0,255,0),5)
        # show the frame and update the FPS counter
        cv2.waitKey(1)
        fps.update()
        #update the FPS counter
        fps.update()
        fps.stop()
        #     # initialize the set of information we'll be displaying on
        #     # the frame
        info = [
            ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        if(land[body_index].visibility>0.5):
            bodyPoints=np.append(bodyPoints,[[int(land[body_index].x*W),int(land[body_index].y*H)]], axis=0)
            cv2.polylines(frame, 
                    [bodyPoints[1:len(bodyPoints)]], 
                    isClosed = False,
                    color = (255,255,0),
                    thickness = 3, 
                    lineType = cv2.LINE_AA)
        # show the output frame
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)
        imgbytes = cv2.imencode(".png", skeleton)[1].tobytes()
        window["-SKELETON-"].update(data=imgbytes)
        key = cv2.waitKey(1) & 0xFF
        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):
            print("s")
            #when track movement don't use poseTracking
            pose = False
        # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    # do a bit of cleanup
    window.close()
    cv2.destroyAllWindows()
    fvs.stop()

def getBodyIndex(event,x,y,flags,param):
    global is_selected_pos,toll,body_index
    (land,startframe) = param
    (H,W) = startframe.shape[:2]
# to check if left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        distance_np = [int(np.sqrt([((l.x*W-x)**2) + ((l.y*H-y)**2)])) for l in land]
        if(np.min(distance_np)<50 and land[distance_np.index(np.min(distance_np))].visibility >0.5):
            is_selected_pos = True
        else:
            print("point not valid")
        body_index = distance_np.index(np.min(distance_np))
        print("left click",x,y,body_index)
    if event == cv2.EVENT_RBUTTONDOWN:
        toll = (x,y)