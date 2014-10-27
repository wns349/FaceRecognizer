import logging
import cv2
import numpy

class FaceRecognizer:
  def __init__(self):
    self.recognizer = None
    self.threshold = 3000
    self.trainPairs = {}
    self.trainShape = None
  
  def initializeTraining(self, trainingConfigPath):
    trainingConfig = open(trainingConfigPath, 'r')
    totalTrainingImages = 0
    for line in trainingConfig:
      if (len(line) <= 0 or line.startswith('#')):
        continue
      totalTrainingImages += 1
    logging.info('Found ' + str(totalTrainingImages) + ' training images')

    trainingConfig.seek(0)
    trainingImages = []
    trainingIndices = []
    for line in trainingConfig:
      if (len(line) <= 0 or line.startswith('#')):
        continue
      tokens = line.split(' ')
      if len(tokens) < 3:
        continue

      personId = int(tokens[0].strip())
      personName = tokens[1].strip()
      personImagePath = tokens[2].strip()
      
      im = cv2.imread(personImagePath, cv2.IMREAD_GRAYSCALE)
      # Resize if necessary,
      if (self.trainShape is None):
        self.trainShape = im.shape
      else:
        cv2.resize(im, self.trainShape)

      # Add to list
      trainingImages.append(numpy.asarray(im, dtype=numpy.uint8))
      trainingIndices.append(personId)
      if (not personId in self.trainPairs):
        self.trainPairs[personId] = personName

    trainingConfig.close()

    return (trainingImages, trainingIndices)

  
  def initialize(self, configs):
    # Threshold
    self.threshold = configs['recognizer.threshold']

    # Training files
    trainingConfigPath = configs['recognizer.training']
    trainingImages, trainingIndices = self.initializeTraining(trainingConfigPath)

    # Identify recognizer type
    recognizerType = configs['recognizer.type'] 
    if (recognizerType == 2):
      self.recognizer = cv2.createLBPHFaceRecognizer()
    elif (recognizerType == 1):
      self.recognizer = cv2.createEigenRecognizer()
    else:
      self.recognizer = cv2.createFisherFaceRecognizer()

    # Train recognizer
    self.recognizer.train(numpy.asarray(trainingImages), numpy.asarray(trainingIndices))
    logging.info('Trained FaceRecognizer');


  def predict(self, img):
    if(img.shape != self.trainShape):
      img = cv2.resize(img, self.trainShape)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    label, confidence = self.recognizer.predict(numpy.asarray(img))

    name = None
    if(label in self.trainPairs):
      name = self.trainPairs[label]

    # Use threshold here?
    if (confidence > self.threshold):
      name = None

    return (name, label, confidence)
  def terminate(self):
    logging.info('Terminating FaceRecognizer...')


