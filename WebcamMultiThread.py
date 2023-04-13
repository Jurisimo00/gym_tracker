# importing required libraries 
import cv2 
import PoseTracking
from threading import Thread # library for implementing multi-threaded processing 

# defining a helper class for implementing multi-threaded processing 
class WebcamStream:
    def __init__(self, pose, stream_id=0):
        self.stream_id = stream_id   # default is 0 for primary camera 
        self.pose = pose
        
        # opening video capture stream 
        self.vcap      = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False :
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))
        print("FPS of webcam hardware/input stream: {}".format(fps_input_stream))
            
        # reading a single frame from vcap stream for initializing 
        self.grabbed , self.frame = self.vcap.read()
        if self.grabbed is False :
            print('[Exiting] No more frames to read')
            exit(0)

        # self.stopped is set to False when frames are being read from self.vcap stream 
        self.stopped = True 

        # reference to the thread for reading next available frame from input stream 
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True # daemon threads keep running in the background while the program is executing 
        
    # method for starting the thread for grabbing next available frame in input stream 
    def start(self):
        self.stopped = False
        self.t.start() 

    # method for reading next frame 
    def update(self):
        while True :
            if self.stopped is True :
                break
            self.grabbed , self.frame = self.vcap.read()
            if(self.pose):
                (H, W) = self.frame.shape[:2]
                self.frame, self.skeleton,self.land = PoseTracking.process(self.frame)
                self.angles=PoseTracking.getAngles(W,H,self.land)
            if self.grabbed is False :
                print('[Exiting] No more frames to read')
                self.stopped = True
                break 
        self.vcap.release()

    # method for returning latest read frame 
    def read(self):
        return (self.frame, self.skeleton, self.land, self.angles)

    # method called to stop reading frames 
    def stop(self):
        self.stopped = True 