#THIS CODE IS TO GIVE FUNCTION TO THE SENSOR
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#Selecting pin 18 for trigger ouput
Trigger = 18
#Selecting pin 24 for echo input
Echo = 24

GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)


def distance():
    
    #Alternates the timer for the Trigger to signal out every .01ms
    #PWM/Time signal is sent through trigger
    GPIO.output(Trigger, True)
    time.sleep(0.00001)
    GPIO.output(Trigger, False)
    
    
    #Variables will save the start time and end time to measure period
    #for echo to time out
    Start = time.time()
    Stop = time.time()
    
    while GPIO.input(Echo) == 0:
        Start = time.time()
        
    while GPIO.input(Echo) == 1:
        Stop = time.time()
    
    Totaltime = Stop - Start
    
    TotalDistance = (Totaltime * 34300)/2
    
    return TotalDistance

##if __name__ == '__main__':
##    try:
##        while True:
##            def sensorON():
##                
##                dist = distance()
##                print ("Measured Distance = %.1f cm" % dist)
##                time.sleep(1)
##                return dist;
## 
##        # Reset by pressing CTRL + C
##    except KeyboardInterrupt:
##        print("Measurement stopped by User") 
##    
##    #print "Ultrasoinc distance recorded was: ", TotalDistance, "CM"
##    #return TotalDistance
##
##
#GPIO.cleanup()

