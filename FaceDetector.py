import logging
import cv2

class FaceDetector:
  def __init__(self):
    self.faceClassifier = None
    self.mirror = False
    self.video = None
    self.scaleFactor = 2.0
    self.minNeighbors = 5
    self.minWidth = 80
    self.minHeight = 80

  def initialize(self, configs):
    # Classifier
    detectionAlgorithmPath = configs['detection.algorithm']
    self.faceClassifier = cv2.CascadeClassifier()
    if (not self.faceClassifier.load(detectionAlgorithmPath)):
      raise Exception("Failed to load " + detectionAlgorithmPath)

    # Classifier related configs
    self.scaleFactor = float(configs['detection.scalefactor'])
    self.minNeighbors = int(configs['detection.minneighbors'])
    self.minWidth = int(configs['detection.minwidth'])
    self.minHeight = int(configs['detection.minheight'])

    # Mirror
    self.mirror = configs['detection.mirror'].startswith('t')

    # Start video
    self.video = cv2.VideoCapture(0)
    videoWidth = int(configs['detection.width'])
    videoHeight = int(configs['detection.height'])
    if (videoWidth > 0):
      self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, videoWidth)
    if (videoHeight > 0):
      self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, videoHeight)

  def grab(self):
    if(self.video is None or self.faceClassifier is None):
      logging.error('Either VideoCapture or Classifier is not available.')
      return
    
    # Grab image
    ret, cameraFrame = self.video.read()
    if (not ret):
      return (None, [])

    if (self.mirror):
      cv2.flip(cameraFrame, 1)

    # Detect faces
    faces = self.faceClassifier.detectMultiScale(cameraFrame,
      scaleFactor=self.scaleFactor,
      minNeighbors=self.minNeighbors,
      minSize=(self.minWidth, self.minHeight),
      flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    return (cameraFrame, faces)

  def terminate(self):
    if (not self.video is None):
      self.video.release() 
    logging.info ('Terminating FaceDetector...')

