#THIS GIVES THE FUNCTION OF TAKING A PICTURE WITH THE PI
import picamera

def takePicture():

    tookPick = 0

    print("Taking picture")
    with picamera.PiCamera() as camera:
        camera.resolution = (1280,720)
        camera.capture("/home/pi/Desktop/imageTest.jpg")

    print("Took Picture")
    tookPic = 1;
    
    return(tookPic)

