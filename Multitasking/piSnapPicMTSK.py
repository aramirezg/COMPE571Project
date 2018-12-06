#THIS GIVES THE FUNCTION OF TAKING A PICTURE WITH THE PI
import picamera
import time
import os

def takePicture():

    taskExec = time.time()

    print("Taking picture")
    with picamera.PiCamera() as camera:
        camera.resolution = (1280,720)
        camera.capture("/home/pi/Desktop/imageTest.jpg")
    print("Camera time", time.time() - taskExec, "s\n")
    print("Took Picture")
    os._exit(0)
    
    
    

