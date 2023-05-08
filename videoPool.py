#!/usr/bin/env python

'''
Multithreaded video processing sample.
Usage:
   video_threaded.py {<video device number>|<video file name>}

   Shows how python threading capabilities can be used
   to organize parallel captured frame processing pipeline
   for smoother playback.

Keyboard shortcuts:

   ESC - exit
   space - switch between multi and single threaded processing
'''

# Python 2/3 compatibility
from __future__ import print_function
import faulthandler 
#faulthandler.enable()
import numpy as np
import cv2 as cv

from multiprocessing import Lock
from multiprocessing.pool import ThreadPool
from multiprocessing import active_children
from multiprocessing import Manager
from collections import deque
from os import getpid

import PoseTracking
import gui
from RepsCounter import RepsCounter
from imutils.video import FPS
from screeninfo import get_monitors


class DummyTask:
    def __init__(self, data):
        self.data = data
    def ready(self):
        return True
    def get(self):
        return self.data

is_selected_pos= False
processed=[]
angles_list=[]
reps=[]
def start(args, pose):
    stopped = False
    real_time=True
    cap = cv.VideoCapture(args)
    #study lock!!!
    manager = Manager()
    lock = manager.Lock()
    def process_frame(frame,lock):
        with lock:
            frame, skeleton,land = PoseTracking.process(frame)
            H, W = frame.shape[:2]
            angles = PoseTracking.getAngles(H,W,land)
        counter.count(angles,land)
        print("reps",counter.get(), getpid(), active_children())
        return frame, skeleton, land, angles, counter.get()
    
    threadn = cv.getNumberOfCPUs()
    print(threadn)
    pool = ThreadPool(processes = threadn)
    pending = deque()

    threaded_mode = True

    startWindow=gui.createStartWindow()
    while True:
        event, _ = startWindow.read(timeout=20)
        if event != gui.sg.WIN_CLOSED and event != "__TIMEOUT__":
            print(event)
            counter = RepsCounter(event.lower())
            startWindow.close()
            break
    window=gui.createWIndow()
    messageWindow=gui.messageWindow()

    _, startFrame = cap.read()
    startFrame, skeleton, land = PoseTracking.process(startFrame)
    cv.namedWindow("Skeleton")
    cv.namedWindow('Frame')
    cv.setMouseCallback('Frame',getBodyIndex, param=(land,startFrame))
    #select which body part you want to use for the RepsCounter
    while(not is_selected_pos):
        startFrame = cv.addWeighted(startFrame,1.0,skeleton,0.3,0)
        cv.imshow('Frame',startFrame)
        print(is_selected_pos)
        event, _ = messageWindow.read(timeout=20)
        if cv.waitKey(20) & 0xFF == 27:
            break
    messageWindow.close()
    (H, W) = startFrame.shape[:2]
    bodyPoints=np.array([[int(land[body_index].x*W),int(land[body_index].y*H)]],dtype=np.uint8)
    cv.destroyAllWindows()

    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == gui.sg.WIN_CLOSED:
                break
        while len(pending) > 0 and pending[0].ready() and not stopped:
            frame, skeleton, land, angles, rep = pending.popleft().get()
            if(land):
                if(land[body_index].visibility>0.5):
                    bodyPoints=np.append(bodyPoints,[[int(land[body_index].x*W),int(land[body_index].y*H)]], axis=0)
                    cv.polylines(frame, 
                            [bodyPoints[1:len(bodyPoints)]], 
                            isClosed = False,
                            color = (255,255,0),
                            thickness = 3, 
                            lineType = cv.LINE_AA)
                
                (H, W) = frame.shape[:2]
                #count reps
                # counter.count(angles,land)
                # print(counter.get())
                #if(real_time):
                #left
                window["-LEFT_KNEE-"].update(str(angles[2]))
                cv.circle(skeleton, (int(land[25].x*W),int(land[25].y*H)), 2,
                    (0, 255, 0), 2)
                window["-LEFT_ELBOW-"].update(str(angles[0]))
                cv.circle(skeleton, (int(land[13].x*W),int(land[13].y*H)), 2,
                    (0, 255, 0), 2)
                #right
                window["-RIGHT_KNEE-"].update(str(angles[3]))
                cv.circle(skeleton, (int(land[26].x*W),int(land[26].y*H)), 2,
                    (0, 255, 0), 2)
                window["-RIGHT_ELBOW-"].update(str(angles[1])) 
                cv.circle(skeleton, (int(land[14].x*W),int(land[14].y*H)), 2,
                    (0, 255, 0), 2)
                window["-REPS-"].update(rep)
                cv.imshow("Frame",frame)
                cv.moveWindow("Frame",0,0)
                cv.imshow("Skeleton",skeleton)
                cv.moveWindow("Skeleton",get_monitors()[0].width,get_monitors()[0].height)
                #else:
                # processed.append(frame)
                # angles_list.append(angles)
                # reps.append(counter.get())
        if len(pending) < threadn:
            _, frame = cap.read()
            if frame is None:
                break
            if threaded_mode:
                frame = frame.copy()
                task = pool.apply_async(process_frame, args=(frame,lock))
            else:
                task = DummyTask(process_frame(frame))
            pending.append(task)
        ch = cv.waitKey(1)
        if ch == ord(' '):
            threaded_mode = not threaded_mode
        if ch == ord('p'):
            stopped = not stopped
        if ch == 27:
            break

    pool.close()
    pool.join()
    print('Done')
    cv.destroyAllWindows()
    window.close()
    children = active_children()
    print(f'Active children: {len(children)}')

    # for i,f in enumerate(processed):
    #     cv.imshow("f",f)
    #     print(angles_list[i])
    #     print(reps[i])
    #     cv.waitKey(50) #important!!

def getBodyIndex(event,x,y,flags,param):
    global is_selected_pos,toll,body_index
    (land,startframe) = param
    (H,W) = startframe.shape[:2]
# to check if left mouse button was clicked
    if event == cv.EVENT_LBUTTONDOWN:
        distance_np = [int(np.sqrt([((l.x*W-x)**2) + ((l.y*H-y)**2)])) for l in land]
        if(np.min(distance_np)<50 and land[distance_np.index(np.min(distance_np))].visibility >0.5):
            is_selected_pos = True
            print("ok")
        else:
            print("point not valid")
        body_index = distance_np.index(np.min(distance_np))
        print("left click",x,y,body_index)
    elif event == cv.EVENT_RBUTTONDOWN:
        toll = (x,y)