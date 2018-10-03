#THIS CODE IS PROGRAMMED FOR SENSOR AND CAMERA FUNCTIONS
import picamera
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

Trigger = 18
Echo = 24

GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

def distance():

    GPIO.output(Trigger, True)
    time.sleep(0.00001)
    GPIO.output(Trigger, False)
	
    Start = time.time()
    End = time.time()
	
    while GPIO.input(Echo) == 0:
        Start = time.time()

    while GPIO.input(Echo) == 1:
        End = time.time()
	
    TotalTime = End - Start
	
    TotalDistance = (TotalTime * 34300)/2

    return TotalDistance

def picture():
    
	with picamera.PiCamera() as camera:
		camera.resolution = (1280,720)
		camera.capture("/home/pi/python_code/email_pics/imageTest.jpg")



if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            
            if dist > 2 and dist < 40:
                print("Intuder has been detected!")
                print("Snapping picture of Intruder")
                picture()
                
            else:
                print("Measured Distance =", dist, "cm")
                time.sleep(1)
			
            
            
        
                
	    
    except KeyboardInterrupt:
            print("Measurement stopped by user");

GPIO.cleanup()