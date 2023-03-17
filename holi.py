import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

def process(image):

  # For webcam input:
  with mp_holistic.Holistic(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as holistic:
      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = holistic.process(image)

      # Draw landmark annotation on the image.
      
      # Flip the image horizontally for a selfie-view display.
      return image