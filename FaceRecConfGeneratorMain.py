import logging, sys, os

def initLogger():
  logging.getLogger().setLevel(logging.INFO)

##########
# Main
##########
initLogger()

if (len(sys.argv) < 3):
  logging.error('ERROR: image directory path required as argv[1] and output text file as argv[2]')
  sys.exit()

# Args
rootDir = sys.argv[1]
outputFile = sys.argv[2]

# Read directory
if not os.path.exists(rootDir):
  raise Exception('Image directory does not exist. ' + rootDir)

subdirs = [(name, os.path.join(rootDir, name)) for name in os.listdir(rootDir) if os.path.isdir(os.path.join(rootDir, name))]


# Make output file
output = open(outputFile, 'w')

# Loop
logging.info ('Found ' + str(len(subdirs)) + ' directories')
userIndex = 1
for subdir in subdirs:
  username = subdir[0]
  imageRoot = subdir[1]

  images = [(name, os.path.join(imageRoot, name)) for name in os.listdir(imageRoot) if name.endswith('.png')]
  
  for image in images:
    line = str(userIndex) + " " + username + " " + image[1]
    print line
    output.write(line+"\n")

  userIndex += 1

output.close()
