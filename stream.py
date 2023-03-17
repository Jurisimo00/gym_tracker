# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import numpy as np
import holi
import PoseTracking
from WebcamMultiThread import WebcamStream

def stream():
    while True:
		# grab the current frame, then handle if we are using a
		# VideoStream or VideoCapture object
		frame = vs.read() if(not webcam) else webcam_stream.read()
		#frame = webcam_stream.read()
		frame = frame[1] if args.get("video", False) else frame
		# check to see if we have reached the end of the stream
		if frame is None:
			break
		# resize the frame (so we can process it faster) and grab the
		# frame dimensions
		frame = imutils.resize(frame, width=500)
		(H, W) = frame.shape[:2]
		#frame = holi.process(frame)
		if pose:
			frame, land = PoseTracking.process(frame)
			a = np.array([int(land[23].x*W),int(land[23].y*H)])
			b = np.array([int(land[25].x*W),int(land[25].y*H)])
			c = np.array([int(land[27].x*W),int(land[27].y*H)])
			cv2.circle(frame, (a[0], a[1]), 12,
				(0, 255, 0), 2)
			check, angle = PoseTracking.getAngle(a,b,c)
#	#print(angle)
			if(check):
				cv2.putText(frame, f'{int(angle)}',(b[0],b[1]),
	  					cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 0, 255), 2)
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
	# if we are using a webcam, release the pointer
	if not args.get("video", False):
		webcam_stream.stop()