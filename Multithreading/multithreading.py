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

#mutex = threading.Lock()
sendEmail = threading.Lock()
cameraLock = threading.Lock()



cameraCounter = 0
mutex = 1
takePic = 1
cameraSem = threading.Semaphore()
sensorSem = threading.Semaphore()

sendEmail.acquire()

GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

def distance():

    startExec = time.time()

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

    global mutex
    global takePic
    global cameraCounter

    if(TotalDistance < 1 or TotalDistance > 40):
        
        sensorSem.acquire(1)
        if(cameraCounter > 0):
            cameraCounter = cameraCounter - 1
        sensorSem.release()

        print("we're here")
            
    else:
        sensorSem.acquire(1)
        cameraCounter = cameraCounter + 1
        sensorSem.release()
    
    print("cameraCounter", cameraCounter)

    sensorResponse = time.time()-startExec

    print("Total Distance:", TotalDistance)
    print("Sensor Response Time:", sensorResponse)

    if(cameraCounter == 0):
        cameraSem.acquire(takePic)
    if(cameraCounter == 1):
        cameraSem.release()

    time.sleep(1)


def picture():

    cameraSem.acquire(takePic)

    picExec = time.time()

    with picamera.PiCamera() as camera:
        camera.resolution = (1280,720)
        camera.capture("/home/pi/python_code/email_pics/imageTest.jpg")
    
    cameraResponse = time.time()-picExec
    
    cameraSem.release()

    print("Camera Response Time:", cameraResponse)

    time.sleep(1)

    return cameraResponse

def email():

    sendEmail.acquire()

    emailExec = time.time()
    
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


    filename= '/home/pi/python_code/email_pics/imageTest.jpg' #this states the path where the filename is attached

    attachment = open(filename,'rb')

    #3 lines encode the attachment with MIME lib and encoders lib
    part = MIMEBase('application','octet-stream')
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

    sendEmail.release()

    emailResponse = time.time()-emailExec
    print("Email Response Time:", emailResponse)

    return emailResponse

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
            
##            t1.join()
##            t2.join()
##            t3.join()

##            print("Multithreading done in:", time.time()-t)

            time.sleep(1)

    except KeyboardInterrupt:
            print("Measurement stopped by user")

GPIO.cleanup()
