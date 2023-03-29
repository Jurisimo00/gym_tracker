import cv2

class RepsCounter:
    def __init__(self, exercise):
        self.exercise = exercise
        self.reps = 0
        self.toll = 180

    def get(self):
        return self.reps

    def count(self,angle):
        if(self.exercise == "squat"):
            self.__squat(angle)

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
