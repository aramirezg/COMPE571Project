#THIS CODE IS PROGRAMMED FOR SENSOR,CAMERA, AND EMAIL FUNCTIONS
import picamera
import time
import RPi.GPIO as GPIO

import smtplib   #library to import the simple mail transfer protocol
from email.mime.text import MIMEText #library used to display text over email
from email.mime.multipart import MIMEMultipart #library used to display a header in an e-mail
from email.mime.base import MIMEBase #library used to deploy message in e-mail
from email import encoders #library to use the encoders for attachment decoding and encoding


GPIO.setmode(GPIO.BOARD)

Trigger = 18
Echo = 24
snapFlag = 0
countPic = 0

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

def email():

    mailUser='aswagisrad@gmail.com'
    mailSender='aswagisrad@gmail.com'
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
    server.login(mailUser,'GOgoopy0926')


    server.sendmail(mailUser,mailSender,text)
    server.quit()



if __name__ == '__main__':
    try:
        while True:
            dist = distance()



            if dist > 2 and dist < 40:


                if snapFlag == 0:

                    print("Intuder has been detected!")
                    print("Snapping picture of Intruder")
                    picture() #calls picture() method
                    print("Sending email alert with pic to user")
                    email() #calls email() method
                    snapFlag = 1


                elif snapFlag == 1:
                    print("Snap Flag value is", snapFlag)
                    time.sleep(30)
                    snapFlag = 0;

            else:


                print("Measured Distance =", dist, "cm")
                time.sleep(1)






    except KeyboardInterrupt:
            print("Measurement stopped by user");

GPIO.cleanup()
