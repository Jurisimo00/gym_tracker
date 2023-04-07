from enum import Enum
import numpy as np

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
    
    def count(self, angle, land):
        if(self.exercise == "squat"):
            self.__squat(angle)
        elif (self.exercise == "deadlift"):
            if(land[12].visibility > land[11].visibility):
                self.__deadlift(land[12])
            else:
                self.__deadlift(land[11])
        elif (self.exercise == "neck"):
            if(land[0].visibility == False):
                print("false")
            if(land[0].visibility > land[1].visibility):
                self.__neck(land[0])
            else:
                self.__neck(land[1])

    def __squat(self, angles: np.array) -> bool:
        assert type(angles) == np.ndarray and "angles must be of type NDArray"
        assert len(angles) >= 4 
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
