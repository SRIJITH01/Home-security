import RPi.GPIO as gpio
import picamera
import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
 
#After it, we have initialized mail and define mail address and messages:
 
fromaddr = "raspicrazy@gmail.com"    # change the email address accordingly
toaddr = "penamaansk@gmail.com"
 
mail = MIMEMultipart()
 
mail['From'] = fromaddr
mail['To'] = toaddr
mail['Subject'] = "Attachment"
body = "Please find the attachment"

#Assaigning pins
led1=18 #HOME MAINS
led0=17 #BULB FOR CAMERA
pir=4
HIGH=1
LOW=0
prev_input = 0
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
#gpio.setup(led0, gpio.OUT)            # initialize GPIO Pin as outputs
gpio.setup(pir,gpio.IN)           # initialize GPIO Pin as input
data=""

#Then we have created def sendMail(data) function for sending mail:

def sendMail(data):
    mail.attach(MIMEText(body, 'plain'))
    print (data)
    dat='%s.jpg'%data
    print (dat)
    attachment = open(dat, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "#berriesaretasty123")
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


#Function def capture_image() is created to capture the image with time and date. 

def capture_image():
    data= time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(5)
    print (data)
    camera.capture('%s.jpg'%data)
    camera.stop_preview()
    time.sleep(1)
    sendMail(data)

# initialization of Picamera


#gpio.output(led , 0)
camera = picamera.PiCamera()
camera.rotation=180
camera.awb_mode= 'auto'
camera.brightness=55

try:
    while True:
        #take a reading
        input = gpio.input(4)
        #if the last reading was low and this one high, alert us
        if ((not prev_input) and input):
            print("Under Pressure")
            capture_image()
        #update previous input
        prev_input = input
        #slight pause
        time.sleep(0.10)
except KeyboardInterrupt:
    pass
finally:
    gpio.cleanup()
