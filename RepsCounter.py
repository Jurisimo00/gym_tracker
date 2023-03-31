import cv2
from enum import Enum

#study to use or not
class BodyPositions(Enum):
    RIGHTSHOULDER = 12
    LEFTSHOULDER = 11

class RepsCounter:
    def __init__(self, exercise):
        self.exercise = exercise
        self.reps = 0
        self.toll = 180
        self.prevLand = 0
        self.first = True
        self.counted = False

    def get(self):
        return self.reps

    def count(self,angle,land):
        if(self.exercise == "squat"):
            self.__squat(angle)
        if(self.exercise == "deadlift"):
            if(land[12].visibility > land[11].visibility):
                self.__deadlift(land[12])
            else:
                self.__deadlift(land[11])

    def __squat(self,angles):
        if(type(angles[3]) == type(None)):
            return False
        if(int(float(angles[3]))<100 and self.toll>100):
            #first angle under tollerance
            self.toll=int(float(angles[3]))
            self.reps +=1
            print(self.toll)
            #one more rep
            return True
        if(int(float(angles[3]))>100):
            self.toll=180
            #no rep
            return False
        
    def __deadlift(self,land): 
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
        
