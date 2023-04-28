import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose

class RepsCounter:
    def __init__(self, exercise,body_index = 12):
        self.exercise = exercise
        self.body_index=body_index
        self.reps = 0
        self.toll = 180
        self.prevLand = 0
        self.first = True
        self.counted = False

    def get(self):
        return self.reps
    
    def getToll(self):
        #0 = axis x
        #1 = axis y
        if(self.exercise == "deadlift"):
            print(self.toll*1.2)
            return self.toll,1

        if(self.exercise == "squat"):
            print(self.toll*1.2)
            return self.toll,1

        if(self.exercise == "neck"):
            print(self.toll*1.2)
            return self.toll,0
    
    def count(self, angles, land):
        if(self.exercise == "squat"):
            print(angles[2:4])
            self.__squat(angles[2:4])
            # print(land[mp_pose.PoseLandmark.LEFT_KNEE].visibility-land[mp_pose.PoseLandmark.RIGHT_KNEE].visibility)
            # if(land[mp_pose.PoseLandmark.LEFT_KNEE].visibility-land[mp_pose.PoseLandmark.RIGHT_KNEE].visibility<0.45):
            #     self.__squat(angles[2:4])
            # elif(land[mp_pose.PoseLandmark.LEFT_KNEE].visibility>land[mp_pose.PoseLandmark.RIGHT_KNEE].visibility):
            #     self.__squat(angles[2])
            #     print("left")
            # else:
            #     self.__squat(angles[3])
            #     print("right")
        elif (self.exercise == "deadlift"):
            if(land[mp_pose.PoseLandmark.RIGHT_SHOULDER].visibility > land[mp_pose.PoseLandmark.LEFT_SHOULDER].visibility):
                self.__deadlift(land[mp_pose.PoseLandmark.RIGHT_SHOULDER])
            else:
                self.__deadlift(land[mp_pose.PoseLandmark.LEFT_SHOULDER])
        elif (self.exercise == "neck"):
            if(land[0].visibility == False):
                print("false")
            if(land[0].visibility > land[1].visibility):
                self.__neck(land[0])
            else:
                self.__neck(land[1])


    def __squat(self, angle: np.array) -> bool:
        # assert type(angles) == np.ndarray and "angles must be of type NDArray"
        #assert len(angles) >= 1
        # if(type(angle) is np.float64):
        #     if(type(angle) == type(None)):
        #         return False
        #     if(int(float(angle))<120 and self.toll>120):
        #         #first angle under tollerance
        #         self.toll=int(float(angle))
        #         self.reps +=1
        #         print(self.toll)
        #         #one more rep
        #         return True
        #     if(int(float(angle))>120):
        #         self.toll=180
        #         #no rep
        #         return False
        # elif(len(angle)==2):
        #easier angle[angle<100] not empty
        #check if all angles are nan
        if(np.count_nonzero(np.isnan(angle))==len(angle)):
            return False
        if(np.any(angle[angle<120]) and self.toll>120):
            #first angle under tollerance
            self.toll=int(float(np.nanmin(angle)))
            self.reps +=1
            print(self.toll)
            #one more rep
            return True
        if(np.nanmin(angle)>120):
            self.toll=180
            #no rep
            return False

            
    def __deadlift(self, land) -> bool:
        print((land.y,self.toll, land.visibility))
        #setting the threshold
        if(self.first):
            self.toll = land.y
            self.first = False
        if((land.y*1.2) < self.toll and not self.counted):
            self.reps+=1
            self.counted = True
            #self.prevLand=land[12].y
            print(True)
            return True
        if((land.y*1.2) > self.toll):
            self.counted = False
            print(False)
        return False
    
    def __neck(self,land) -> bool:
        if(self.first):
            self.toll = land.x
            self.first = False
        if(land.x>(self.toll*1.2) and not self.counted):
            self.reps+=1
            self.counted=True
            print((land.x,self.toll*1.2))
            return True
        if(land.x<=(self.toll*1.2)):
            print((land.x,self.toll*1.2,self.counted))
            self.counted=False
        return False   
