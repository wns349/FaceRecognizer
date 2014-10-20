import logging
import cv2

class FaceRecognizer:
  def __init__(self):
    self.recognizer = None
    self.threshold = 3000
    self.trainWidth = 0
    self.trainHeight = 0
    self.trainPairs = {}
  
  def initialize(self, configs):
    # Identify recognizer type
    recognizerType = configs['recognizer.type'] 
    if (recognizerType == 2):
      self.recognizer = cv2.createLBPHFaceRecognizer()
    elif (recognizerType == 1):
      self.recognizer = cv2.createEigenRecognizer()
    else:
      self.recognizer = cv2.createFisherFaceRecognizer()

    # Threshold
    self.threshold = configs['recognizer.threshold']
