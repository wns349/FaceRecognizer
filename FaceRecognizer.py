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
    # Threshold
    self.threshold = configs['recognizer.threshold']

    # Training files
    trainingConfig = open(configs['recognizer.training'], 'r')
    totalTrainingImages = 0
    for line in trainingConfig:
      if (len(line) <= 0 or line.startswith('#')):
        continue
      totalTrainingImages++
    logging.info('Found ' + totalTrainingImages + ' training images')

    # Identify recognizer type
    recognizerType = configs['recognizer.type'] 
    if (recognizerType == 2):
      self.recognizer = cv2.createLBPHFaceRecognizer()
    elif (recognizerType == 1):
      self.recognizer = cv2.createEigenRecognizer()
    else:
      self.recognizer = cv2.createFisherFaceRecognizer()



