#THIS GIVES THE FUNCTION OF TAKING A PICTURE WITH THE PI
import picamera


print("Taking picture")
with picamera.PiCamera() as camera:
	camera.resolution = (1280,720)
	camera.capture("/home/pi/python_code/imageTest.jpg")
print("Took Picture")
