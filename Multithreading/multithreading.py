#THIS CODE IS PROGRAMMED FOR SENSOR,CAMERA, AND EMAIL FUNCTIONS
import picamera
import time
import RPi.GPIO as GPIO

import threading

import smtplib   #library to import the simple mail transfer protocol
from email.mime.text import MIMEText #library used to display text over email
from email.mime.multipart import MIMEMultipart #library used to display a header in an e-mail
from email.mime.base import MIMEBase #library used to deploy message in e-mail
from email import encoders #library to use the encoders for attachment decoding and encoding

GPIO.setmode(GPIO.BOARD)

Trigger = 18
Echo = 24

GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

inRange = threading.Event()
picTaken = threading.Event()

mutex = threading.Semaphore()
sharedPic = threading.Semaphore()
sharedGPIO = threading.Semaphore()

cameraCount = 0



def distance():

    global cameraCount

    sharedGPIO.acquire(1)

    GPIO.output(Trigger, True)
    time.sleep(0.00001)
    GPIO.output(Trigger, False)

    Start = time.time()
    End = time.time()

    while GPIO.input(Echo) == 0:
        Start = time.time()

    while GPIO.input(Echo) == 1:
        End = time.time()

    sharedGPIO.release()

    #mutex.acquire(1)
    TotalTime = End - Start
    TotalDistance = (TotalTime * 34300)/2

    if(TotalDistance < 1 or TotalDistance > 40):
        mutex.acquire(1)
        cameraCount = 0
        inRange.clear()
        mutex.release()
        
    else:
        mutex.acquire(1)
        cameraCount = cameraCount + 1
        inRange.set()
        mutex.release()
    #mutex.release()

    print("Sensor Done:", TotalDistance, "cm")
    print("cameraCount =", cameraCount)

def picture():
    
    global cameraCount

    sharedPic.acquire(1)

    if(inRange.isSet() and (cameraCount == 1 or not cameraCount%15)):
        with picamera.PiCamera() as camera:
            camera.resolution = (1280,720)
            camera.capture("/home/pi/python_code/email_pics/imageTest.jpg")
            picTaken.set()
            print("Picture Taken\n")
    else:
        picTaken.clear()

    sharedPic.release()

    '''
    #if there are 2 or more threads of this function and they all see the if statement is true
    #they will all be blocked but they are still waiting for the same resource
    #you could be taking pictures later on even if you dont want to
    if(inRange.isSet() and (cameraCount == 1 or not cameraCount%10)):
        sharedPic.acquire(1)
        with picamera.PiCamera() as camera:
            camera.resolution = (1280,720)
            camera.capture("/home/pi/python_code/email_pics/imageTest.jpg")
            picTaken.set()
            print("Picture Taken")
        sharedPic.release()
    else:
        picTaken.clear()
    '''

def email():

    mailUser='compe571rpialerts@gmail.com'
    mailSender='compe571rpialerts@gmail.com'
    subject='Alert!!'

    #MIME library formats from,to,and subject in email from variables above
    message= MIMEMultipart()
    message['From'] = mailUser
    message['To'] = mailSender
    message['Subject'] = subject

    body = '!!!Alert an intruder has been detected! Check the picture out'
    message.attach (MIMEText(body,'plain')) #message body is attached by MIME as plain text

    #3 lines encode the attachment with MIME lib and encoders lib
    part = MIMEBase('application','octet-stream')

    filename= '/home/pi/python_code/email_pics/imageTest.jpg' #this states the path where the filename is attached

    sharedPic.acquire(1)
    try:
        if(picTaken.isSet()):

            attachment = open(filename,'rb')

            #3 lines encode the attachment with MIME lib and encoders lib
            part.set_payload((attachment).read())
            encoders.encode_base64(part)

            #this adds the info for the small preview in gmail
            #NOTE: "filename" variable as is must be defined as such for it to work
            #######always put your file in a "filename" variable no exeptions
            part.add_header('Content-Disposition',"attachment; filename="+filename)

            #attach attachment and send with email protocols
            message.attach(part)
            text = message.as_string()
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(mailUser,'compe571project')

            server.sendmail(mailUser,mailSender,text)
            server.quit()

            print("Email sent!\n")
    
    except:
        print("Error, might be internet connection.\n")

    sharedPic.release()

if __name__ == '__main__':   

    try:

        while 1:

            t = time.time()
            
            t1 = threading.Thread(target=distance)
            t2 = threading.Thread(target=picture)
            t3 = threading.Thread(target=email)

            t1.start()
            t2.start()
            t3.start()

            #t1.join()
            #t2.join()
            #t3.join()
            #print("Total Execution Time:", time.time()-t, "\n")
            
            print("Thread creation done in:", time.time()-t, "\n")

            time.sleep(1)

    except KeyboardInterrupt:
            print("Measurement stopped by user")

GPIO.cleanup()
