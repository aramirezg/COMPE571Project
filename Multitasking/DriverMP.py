import piSensorMTSK
import piEmailPicMTSK
import piSnapPicMTSK
import time

import os

import multiprocessing
from multiprocessing import Pool

snapFlag = 0

#process1 = multiprocessing.Process(target=piSensorMTSK.distance())
##process2 = multiprocessing.Process(target=piSnapPicMTSK.takePicture())
##process3 = multiprocessing.Process(target=piEmailPicMTSK.email())
##
##process1.start()
##process2.start()
##process3.start()


####NOTE FOR MULTITAKSING
##really only two tasks:
##perform a process for measuring distance
##perform timeout as another process while detecting distace


###possibly make recording a process??
distance = 0
def distanceChild():
    global distance
    distance = piSensorMTSK.distance()
    #os._exit(0)
    print("exited")
    return(distance)
    



if __name__ == '__main__':
    try:
        #while True:

#            process1 = multiprocessing.Process(target=piSensorMTSK.distance())
#            process2 = multiprocessing.Process(target=piSnapPicMTSK.takePicture())
#            process3 = multiprocessing.Process(target=piEmailPicMTSK.email())
            
         
##
#             process1.start()
#            process2.start()
#            process3.start()

##            process1.join()
##            process2.join()
##            process3.join()
#        global distance 
        newpid = os.fork()
        
        if newpid > 0:
            print(str(os.getpid()))
            distance =piSensorMTSK.distance()
            
        if(newpid == 0):
            print("Child")
            distance = piSensorMTSK.distance()

        startExec = time.time()    
        if distance >2 and distance <40:
            
            if snapFlag == 0:
                    print("Intruder has been detetcted!",)
                    print("sensor Time =", time.time()- startExec, "s\n")
                    print("Snapping picture of Intruder")
                    #newpid1 = os.fork()
                    if(newpid > 0):
                        os.waitpid(newpid,0)
                        os._exit(0)
                        print("exited")
                    print("Parent Waiting")
                    piSnapPicMTSK.takePicture()

                    
                    #piEmailPicMTSK.email()
                    print("email sent to user!")
                    print("Execution Time =", time.time()-startExec,"s\n")

                    snapFlag = 1
                    snapTimer = 0
                    o
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
        
        print("b4 exit")
        os._exit(0)
        
            
            
        
                
	    
    except KeyboardInterrupt:
        print("Measurement stopped by user")





