# import the necessary packages
import argparse
import time
import cv2 as cv
import streamUtils as su
import videoPool as vp
import gui

path=""
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
help="path to input video file")
ap.add_argument("-e","--exercise",type=str, default="squat")
args = vars(ap.parse_args())
# if a video path was not supplied, grab the reference to the web cam
window=gui.createSelectionInputWindow()
while True:
    event, values = window.read()
    if(values["-IN-"]!="" and event == "Submit"):
        path=values["-IN-"]
        time.sleep(1.0)
        window.close()
        vp.start(path)
        break
    elif event == gui.sg.WIN_CLOSED or event=="Exit":
        cv.destroyAllWindows()
        window.close()
        break
    elif event == "Webcam":
        print("[INFO] starting video stream...")
        time.sleep(1.0)
        window.close()
        su.start(values["-RECORD-"])
        break

        
		
