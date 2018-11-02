import piSensorMTSK
import piEmailPicMTSK
import piSnapPicMTSK
import time

snapFlag = 0

if __name__ == '__main__':
    try:
        while True:
            distance = piSensorMTSK.distance()
            
            startExec = time.time()
            

            if distance >2 and distance <40:

                if snapFlag == 0:
                    print("Intruder has been detetcted!",)
                    print("sensor Time =", time.time()- startExec, "s\n")
                    print("Snapping picture of Intruder")
                    piSnapPicMTSK.takePicture()
                    piEmailPicMTSK.email()
                    print("email sent to user!")
                    print("Execution Time =", time.time()-startExec,"s\n")

                    snapFlag = 1
                    snapTimer = 0
                else:
                    snapTimer += 1                  
                    if snapTimer == 15:
                        snapFlag = 0
                    print("Intruder Detected", distance, "cm", snapTimer,"s")
                    time.sleep(1)
        
            else:
                print("Measured Distance =", distance, "cm")
                snapFlag = 0 
                snapTimer = 0 #reset timer
                time.sleep(1)
			
            
            
        
                
	    
    except KeyboardInterrupt:
        print("Measurement stopped by user");





