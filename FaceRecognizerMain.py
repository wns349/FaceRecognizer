import logging, sys, time
import FaceDetector, FaceRecognizer
import cv2

def initLogger():
  logging.getLogger().setLevel(logging.INFO)

def loadConfig(configFilePath):
  configs = {}
  logging.info('Loading config file: ' + configFilePath)
  confFile = open(configFilePath, 'r')
  for line in confFile:
    if (len(line) <= 0 or line.startswith('#') or not '=' in line):
      continue
    words = line.split('=')
    configs[words[0].strip()] = words[1].strip()
    
  confFile.close()

  return configs

def startProcess(configs, faceDetector, faceRecognizer):
  isGUI = configs['main.gui'].startswith('t')

  faceTuples = []
  while True:
    # Grab cameraFrame and detected faces
    cameraFrame, faces = faceDetector.grab()

    if (cameraFrame is None):
      continue

    # Crop faces for recognition
    for face in faces:
      cropFace = cameraFrame[face[1]:face[1] + face[3], face[0]:face[0] + face[2]]
      predictResult = faceRecognizer.predict(cropFace)
      faceTuples.append((predictResult, face))
      #cv2.imshow('CROP FACE', cropFace)
      #if(cv2.waitKey(3000) >= 0):break
      
    # Draw face
    for faceTuple in faceTuples:
      predictResult = faceTuple[0]
      face = faceTuple[1]

      print predictResult

      faceRecognized = (not predictResult[0] is None)
      rectColor = (0, 255, 0) if faceRecognized else (255, 0, 0)
      cv2.rectangle(cameraFrame, (face[0] + face[2], face[1] + face[3]), (face[0], face[1]), rectColor)

    # Display image
    if (isGUI):
      cv2.imshow('FaceRecognizer', cameraFrame)

    if (cv2.waitKey(30) >= 0):
      break

    # Clear
    del faceTuples[:]

  return

##########
# Main
##########
initLogger()

if (len(sys.argv) < 2):
  logging.error('ERROR: config file path required as argv[1]')
  sys.exit()

# Read config
configs = loadConfig(sys.argv[1])

# Face Detector
faceDetector = FaceDetector.FaceDetector()
faceDetector.initialize(configs)

# Face Recognition
faceRecognizer = FaceRecognizer.FaceRecognizer()
faceRecognizer.initialize(configs)

# Start Process
startProcess(configs, faceDetector, faceRecognizer)
