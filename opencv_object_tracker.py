# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import numpy as np
import PoseTracking
from WebcamMultiThread import WebcamStream
import streamUtils as su
import videoUtils as vu

def track():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
	ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
	ap.add_argument("-e","--exercise",type=str)
	args = vars(ap.parse_args())
	# extract the OpenCV version info
	(major, minor) = cv2.__version__.split(".")[:2]
# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# function to create our object tracker
	if int(major) == 3 and int(minor) < 3:
		tracker = cv2.Tracker_create(args["tracker"].upper())
# otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
# approrpiate object tracker constructor:
	else:
	# initialize a dictionary that maps strings to their corresponding
	# OpenCV object tracker implementations
		OPENCV_OBJECT_TRACKERS = {
			"csrt": cv2.TrackerCSRT_create,
			"kcf": cv2.TrackerKCF_create,
			#"boosting": cv2.TrackerBoosting_create,
			"mil": cv2.TrackerMIL_create,
			#"tld": cv2.TrackerTLD_create,
			#"medianflow": cv2.TrackerMedianFlow_create,
			#"mosse": cv2.TrackerMOSSE_create
		}
	# grab the appropriate object tracker using our dictionary of
	# OpenCV object tracker objects
		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

# if a video path was not supplied, grab the reference to the web cam
	if not args.get("video", False):
		print("[INFO] starting video stream...")
		#vs = VideoStream(src=0).start()
		#webcam_stream=WebcamStream(stream_id=0)
		#webcam_stream.start()
		#flag to know if is a stream or not
		webcam = True
		time.sleep(1.0)
		su.stream(tracker,args)
# otherwise, grab a reference to the video file
	else:
		vs = cv2.VideoCapture(args["video"])
		#vs = FileVideoStream(args["video"]).start()
		time.sleep(1.0)
		webcam = False
		vu.video(tracker,args)
# initialize the FPS throughput estimator
		fps = None