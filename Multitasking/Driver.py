import piSensorMTSK
import piEmailPicMTSK
import piSnapPicMTSK
import time

snapFlag = 0

if __name__ == '__main__':
    try:
        while True:
            distance = piSensorMTSK.distance()
            
            

            if distance >2 and distance <40:
                if snapFlag == 0:
                    print("Intruder has been detetcted!")
                    print("Snapping picture of Intruder")
                    piSnapPicMTSK.takePicture()
                    piEmailPicMTSK.email()
                    print("email sent to user!")
                    snapFlag = 1

                elif snapFlag == 1:
                    print("Snap Flag Status:", snapFlag)
                    time.sleep(60)
                    snapFlag = 0
        
        
            else:
                print("Measured Distance =", distance, "cm")
                time.sleep(1)
			
            
            
        
                
	    
    except KeyboardInterrupt:
        print("Measurement stopped by user");





