FaceRecognizer
=====

FaceRecognizer is a program that detects and recognizes face using a webcam.

Requirements
-----
 - [OpenCV 2.4.9]
 - [Python 2.7]
 - [Numpy]
 - [Py4j]


Installation
-----
 1. Install Python, Numpy
 
 2. Install OpenCV: [Installation in Linux][1]
 
 3. Install Py4j

Execution
-----
**FaceRecognizerMain**

 - Detects and recognizes face using a webcam.

 ```
 $python FaceRecognizerMain.py ./conf/facerec.cf
 ```

**FaceTrainerMain**

 - Util that helps one to capture faces for training

 ```
 $python FaceTrainerMain.py ./conf/facetrain.cf
 ```

**FaceRecConfGeneratorMain**

 - Util that generates config file for face recognition.

 ```
 $python FaceRecConfGeneratorMain.py ./res/images/ ./sample_config.cf
 ```



[OpenCV 2.4.9]:https://github.com/Itseez/opencv/releases/tag/2.4.9
[Python 2.7]:https://www.python.org/download/
[Numpy]:http://www.numpy.org/
[Py4j]:http://py4j.sourceforge.net/
[1]:http://docs.opencv.org/doc/tutorials/introduction/linux_install/linux_install.html




