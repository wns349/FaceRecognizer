import logging, sys, os, cv2, time

classifier = None
video = None
scaleFactor = 2.0
minNeighbors = 5
minWidth = 80
minHeight = 80

def getTime():
  return int(round(time.time() * 1000))

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

def grab():
  global video, classifier, scaleFactor, minNeighbors, minWidth, minHeight

  cameraFrame = None
  faces = []
  found = False
  while not found:
    logging.info('Looking for face...')
    ret, cameraFrame = video.read()
    if (not ret):
      return (None, [])
    if (mirror):
      cv2.flip(cameraFrame, 1)
    faces = classifier.detectMultiScale(cameraFrame,
      scaleFactor=scaleFactor,
      minNeighbors=minNeighbors,
      minSize=(minWidth, minHeight),
      flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
  
    if (len(faces) > 0):
      found = True

    return cameraFrame, faces

def trainUsers(users, configs):
  imagesPerUser = int(configs['train.imagecount'])
  imageSize = ( int(configs['train.imagewidth']), int(configs['train.imageheight']) )
  for user in users:
    raw_input('Press enter when ready to train user ' + user[0])
    imageIndex = 0
    while imageIndex < imagesPerUser:
      filename = user[1] + os.sep + user[0]+str(imageIndex)+'.png'
      logging.info(user[0] + ' - (' + str(imageIndex+1) + '/' + str(imagesPerUser) + ') - ' + filename)
      
      cameraFrame, faces = grab()

      for face in faces:
        cropFace = cameraFrame[face[1]:face[1]+face[3], face[0]:face[0]+face[2]]

        cropFace = cv2.resize(cropFace, imageSize)

        cv2.imshow(filename, cropFace)
        if(cv2.waitKey(0) == ord('y')):
          # if Y is pressed, save
          cv2.imwrite(filename, cropFace)
          imageIndex += 1
          break

      # sleep a little before processing further
      time.sleep(0.2) 

    # clear windows before starting second user
    cv2.destroyAllWindows()
    

def initializeFaceDetector(facerecConfig):
  global classifier, video, videoWidth, videoHeight, mirror, scaleFactor, minNeighbors, minWidth, minHeight

  classifier = cv2.CascadeClassifier()
  if (not classifier.load(facerecConfig['detection.algorithm'])):
    raise Exception('Failed to load ' + facerecConfig['detection.algorithm'])

  scaleFactor = float(facerecConfig['detection.scalefactor'])
  minNeighbors = int(facerecConfig['detection.minneighbors'])
  minWidth = int(facerecConfig['detection.minwidth'])
  minHeight = int(facerecConfig['detection.minheight'])
  mirror = facerecConfig['detection.mirror'].startswith('t')

  video = cv2.VideoCapture(0)
  videoWidth = int(facerecConfig['detection.width'])
  videoHeight = int(facerecConfig['detection.height'])
  if (videoWidth > 0):
    video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, videoWidth)
  if (videoHeight > 0):
    video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, videoHeight)

  

def startProcess(configs):
  logging.info('Starting process')

  # Initialize face detector
  facerecConf = loadConfig(configs['train.facerec'])
  initializeFaceDetector(facerecConf)

  # Make output dir, if not exist
  outputDir = configs['train.output']
  if not os.path.exists(outputDir):
    os.makedirs(outputDir)
    logging.info('Created new directory: ' + outputDir)

  # Get number of users to train and their names
  users = int(raw_input("Enter total number of users to train: "))
  userNames=[]
  i = 0
  while i < users:
    userName = raw_input("Enter " + str(i+1) + "/" + str(users) + " user's name: ")
    userDir = outputDir + os.sep + userName
    if os.path.exists(userDir):
      logging.error('User directory already exists. ' + userDir)
      logging.error('Try another name')
      continue
    else:
      os.makedirs(userDir)
      logging.info('Created new user directory: ' + userDir)
      userNames.append((userName, userDir))
    i += 1

  # Train users
  trainUsers(userNames, configs)

def terminateProcess(configs):
  logging.info('Terminated...Bye')
 
##########
# MAIN
##########
initLogger()

if (len(sys.argv) < 2):
  logging.error('ERROR: config file path required as argv[1]')
  sys.exit()

# Read config
configs = loadConfig(sys.argv[1])

startProcess(configs)

terminateProcess(configs)
