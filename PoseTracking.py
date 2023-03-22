import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def process(image):
  
# For webcam input:
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # mp_drawing.draw_landmarks(
        #     image,
        #     results.pose_landmarks,
        #     mp_pose.POSE_CONNECTIONS,
        #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    #return image and the normalized landmark list
        if(results.pose_landmarks == None):
            print(results.pose_landmarks)
            return image,0
    return image, results.pose_landmarks.landmark

def getAngle(a,b,c):
    #check if a b c is an array
    if(type(a) != None and type(b) != None and type(c) != None):
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        return True, np.degrees(angle)
    return False, 0

def getAngles(width, height, land):
    #list of functional pose points see :https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md#output
    index = [[11,13,15],[12,14,16],[23,25,27],[24,26,28]]
    angles=np.array([])
    for i in index:
        a = np.array([int(land[i[0]].x*width),int(land[i[0]].y*height)]) #if (land[i[0]].visibility > 0.7) else None
        b = np.array([int(land[i[1]].x*width),int(land[i[1]].y*height)]) #if (land[i[1]].visibility > 0.7) else None
        c = np.array([int(land[i[2]].x*width),int(land[i[2]].y*height)]) #if (land[i[2]].visibility > 0.7) else None
        check,angle=getAngle(a,b,c)
        print(angle)
        if(check):
            angles=np.append(angles,angle)
            #print(angles)
    #return tuples of angles and point to write angle
    return angles
    
