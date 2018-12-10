#THIS CODE IS USED TO EMAIL A PIC OVER EMAIL
import smtplib   #library to import the simple mail transfer protocol
from email.mime.text import MIMEText #library used to display text over email
from email.mime.multipart import MIMEMultipart #library used to display a header in an e-mail
from email.mime.base import MIMEBase #library used to deploy message in e-mail
from email import encoders #library to use the encoders for attachment decoding and encoding
import time
import multiprocessing

def email():

    emailExec = time.time()
    
#3 variables used for user,sender, and subject
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


    filename= '/home/pi/Desktop/imageTest.jpg' #this states the path where the filename is attached

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

    print("Email Time =", time.time()-emailExec, "s\n")
