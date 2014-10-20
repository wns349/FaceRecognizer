import logging, sys
import FaceDetector


def initLogger():
  logging.getLogger().setLevel(logging.INFO)

def loadConfig(configFilePath):
  configs = {}
  logging.info("Loading config file: " + configFilePath)
  confFile = open(configFilePath, 'r')
  for line in confFile:
    if (len(line) <= 0 or line.startswith('#') or not '=' in line):
      continue
    words = line.split('=')
    configs[words[0].strip()] = words[1].strip()
    
  confFile.close()

  return configs

def startProcess(configs, faceDetector):
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

# TODO: Face Recognition

# Start Process
startProcess(configs, faceDetector)
