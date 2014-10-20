import logging
import cv2

class FaceDetector:
  def __init__(self):
    self.faceClassifier = None
    self.mirror = False
    self.video = None

  def initialize(self, configs):
    # Classifier
    detectionAlgorithmPath = configs['detection.algorithm']
    self.faceClassifier = cv2.CascadeClassifier()
    if (not self.faceClassifier.load(detectionAlgorithmPath)):
      raise Exception("Failed to load " + detectionAlgorithmPath)

    # Mirror
    self.mirror = configs['detection.mirror'].startswith('t')

    # Start video
    self.video = cv2.VideoCapture(0)

