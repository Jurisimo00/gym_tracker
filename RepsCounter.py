import cv2

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
            self.__deadlift(land)

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
        print((land[12].y,self.toll, land[12].visibility))
        #setting the threshold
        if(self.first):
            self.toll = land[12].y
            self.first = False
        if((land[12].y*1.2) < self.toll and not self.counted):
            self.reps+=1
            self.counted = True
            #self.prevLand=land[12].y
            print(True)
            return True
        if((land[12].y*1.2) > self.toll):
            self.counted = False
            print(False)
        return False
        
