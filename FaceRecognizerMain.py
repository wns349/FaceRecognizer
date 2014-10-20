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
  while True:
    # Grab cameraFrame and detected faces
    cameraFrame, faces = faceDetector.grab()

    # Draw face
    for face in faces:
      cv2.rectangle(cameraFrame, (face[0] + face[2], face[1] + face[3]), (face[0], face[1]), (0, 255, 0))

    # Display image
    cv2.imshow('FaceRecognizer', cameraFrame)

    if (cv2.waitKey(30) >= 0):
      break

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
