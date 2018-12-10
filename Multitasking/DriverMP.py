import piSensorMTSK
import piEmailPicMTSK
import piSnapPicMTSK
import time
import RPi.GPIO as GPIO

import multiprocessing


snapFlag = 0


####NOTE FOR MULTITAKSING
##really only two tasks:
##perform a process for measuring distance
##perform timeout as another process while detecting distace


if __name__ == '__main__':
#def main():
    try:

        
        while True:


            #distance = piSensorMTSK.distance()
            startExec = time.time()

            ##
            dist = multiprocessing.Value('d',0.0)
            distanceProcess = multiprocessing.Process(target=piSensorMTSK.distance, args=(dist,))
            pictureProcess = multiprocessing.Process(target=piSnapPicMTSK.takePicture)
            emailProcess = multiprocessing.Process(target=piEmailPicMTSK.email)

            distanceProcess.start()
            distanceProcess.join()
            ##

            if dist.value >2 and dist.value <40:

                if snapFlag == 0:
                        print("Intruder has been detetcted!",)
                        print("sensor Time =", time.time()- startExec, "s\n")
                        print("Snapping picture of Intruder")
                        pictureProcess.start()
                        pictureProcess.join()
                        emailProcess.start()
                        emailProcess.join()
                        print("email sent to user!")
                        print("Execution Time =", time.time()-startExec,"s\n")

                        snapFlag = 1
                        snapTimer = 0
                        
                else:
                    snapTimer += 1                  
                    if snapTimer == 15:
                       snapFlag = 0
                    print("Intruder Detected", dist.value, "cm", snapTimer,"s")
                    time.sleep(1)
                    #os._exit(0)

            else:
                print("Measured Distance =", dist.value, "cm")
                snapFlag = 0 
                snapTimer = 0 #reset timer
                time.sleep(1)
                
	    
    except KeyboardInterrupt:
        print("Measurement stopped by user")


	GPIO.cleanup()


