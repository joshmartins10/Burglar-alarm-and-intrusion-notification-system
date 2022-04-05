'''BURGLAR ALARM AND INTRUSION NOTIFICATION SYSTEM'''
#Importing needed libraries/modules
import sys
sys.path.append("/usr/local/lib/python3.7/site-packages/cv2/python-3.7") #Indicates path to the location of openCV library files

import cv2

import RPi.GPIO as GPIO

import time

from time import sleep

import numpy as np

from datetime import datetime

import os

import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email.mime.text import MIMEText

from email import encoders

from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback, PNStatusCategory

from pubnub.pnconfiguration import PNConfiguration

from pubnub.exceptions import PubNubException

from gpiozero import LED

from gpiozero import Buzzer


gmail_user = "Input email address for sending notification" #Sender email address

gmail_pwd = "Input password for email address for sending notification" #Sender email password

to = 'Input notification recipient's email address' #Receiver email address

subject = "Intrusion Alert"

text = "There is some activity in your home. See the attached picture."


sensor = 4 #Defines the pin for the sensor (Object detection sensor of PIR)

buz = Buzzer(14) # initlize the Buzzer on pin 14

#set red, green and blue pins (For this project an RGB LED was used)
redPin = 12
greenPin = 19
bluePin = 13



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
#set pins as outputs
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

def alarmL():
        #print('Long pause alarm')
        buz.beep(on_time=1,off_time=3)  # turn on the led
        #sleep(1)  # then wait 1 second
        #buz.off() # then turn it off
        #flashes()
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        red()

def alarmS():
        #print('Short pause alarm')
        #buz.on()  # turn on the led
        #sleep(1)  # then wait 1 second
        #buz.off() # then turn it off
        buz.beep(on_time=1,off_time=1)
        #flashes()
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        sleep(2)
        flash()
        red()
    
def reset():
        #print('Reset alarm')
        #buz.on()  # turn on the buzzer
        #sleep(1)  # then wait 1 second
        #buz.off() # then turn it off
        #buz.beep(off_time=1,off_time=1)
        #buz.toggle()
        buz.off()
        turnOff()
        
def turnOff():
        GPIO.output(redPin,GPIO.HIGH)
        GPIO.output(greenPin,GPIO.HIGH)
        GPIO.output(bluePin,GPIO.HIGH)
    
def white():
        GPIO.output(redPin,GPIO.LOW)
        GPIO.output(greenPin,GPIO.LOW)
        GPIO.output(bluePin,GPIO.LOW)
    
def red():
        GPIO.output(redPin,GPIO.LOW)
        GPIO.output(greenPin,GPIO.HIGH)
        GPIO.output(bluePin,GPIO.HIGH)

def green():
        GPIO.output(redPin,GPIO.HIGH)
        GPIO.output(greenPin,GPIO.LOW)
        GPIO.output(bluePin,GPIO.HIGH)
    
def blue():
        GPIO.output(redPin,GPIO.HIGH)
        GPIO.output(greenPin,GPIO.HIGH)
        GPIO.output(bluePin,GPIO.LOW)
    
def yellow():
        GPIO.output(redPin,GPIO.LOW)
        GPIO.output(greenPin,GPIO.LOW)
        GPIO.output(bluePin,GPIO.HIGH)
    
def purple():
        GPIO.output(redPin,GPIO.LOW)
        GPIO.output(greenPin,GPIO.HIGH)
        GPIO.output(bluePin,GPIO.LOW)
    
def lightBlue():
        GPIO.output(redPin,GPIO.HIGH)
        GPIO.output(greenPin,GPIO.LOW)
        GPIO.output(bluePin,GPIO.LOW)
def flashes():
    while True:
        #turnOff()
        sleep(0.1) #1second
        red()
        sleep(0.1)
        white()
        #sleep(1)
        #green()
        sleep(0.1)
        blue()
        #sleep(1)
        #yellow()
        #sleep(1)
        #purple()
        #sleep(1)
        #lightBlue()
        sleep(0.1)
        #turnOff()
        
def flash():
    #while True:
        #turnOff()
        sleep(0.1) #1second
        red()
        sleep(0.1)
        white()
        #sleep(1)
        #green()
        sleep(0.1)
        blue()
        #sleep(1)
        #yellow()
        #sleep(1)
        #purple()
        #sleep(1)
        #lightBlue()
        sleep(0.1)
        turnOff()
        
class SubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        print('Received message: %', message.message)

        if message.message == "alarm1":
            print ("Long pause alarm started")
            alarmL()
        elif message.message == "alarm2":
            print ("Short pause alarm started")
            alarmS()
        elif message.message == "flashes":
            print ("LED flashers started")
            flashes()
        elif message.message == "flash":
            print ("LED flash one cycle started")
            flash()
        elif message.message == "light":
            print ("Red LED ON")
            white()
        elif message.message == "red":
            print ("Red LED ON")
            red()
        elif message.message == "nolight":
            print ("LED turned off")
            turnOff()
        elif message.message == "reset":
            print ("Alarm and LED reset")
            reset()
            
           
previous_state = 0
current_state = 0   

cam = cv2.VideoCapture(0)

cv2.namedWindow("Surveilance Camera")

img_counter = 0

while (img_counter >=0):
    
    previous_state = current_state

    current_state = GPIO.input(sensor)
    
    
    if current_state != previous_state:

        new_state = "HIGH" if current_state else "LOW"

        print("GPIO pin %s is %s" % (sensor, new_state))
        
        
        
    ret, frame = cam.read()    
        
    cv2.imshow("Surveilance Camera", frame)
    k = cv2.waitKey(1)

    if ret:
        
        if (current_state == 0): #set 0 for object detection sensor but 1 for PIR sensor
            
            img_name = datetime.now().strftime("%m-%d-%Y %H:%M:%S")+" IntruderCapture{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            print("Intruder Captured!")
            img_counter += 1
        
            msg = MIMEMultipart()
        
            msg['From'] = gmail_user

            msg['To'] = to

            msg['Subject'] = subject

            msg.attach(MIMEText(text))

            part = MIMEBase('application', 'octet-stream')

            part.set_payload(open(img_name, 'rb').read())

            encoders.encode_base64(part)

            part.add_header('Content-Disposition',

        'attachment; filename="%s"' % os.path.basename(img_name))

            msg.attach(part)

            mailServer = smtplib.SMTP("smtp.gmail.com", 587)

            mailServer.ehlo()

            mailServer.starttls()

            mailServer.ehlo()

            mailServer.login(gmail_user, gmail_pwd)

            mailServer.sendmail(gmail_user, to, msg.as_string())

            mailServer.close()

            print ("Email Sent")

            os.remove(img_name)
        
            cam.release()

            cv2.destroyAllWindows()
  
        
            pnconfig = PNConfiguration() # create pubnub_configuration_object

            pnconfig.publish_key = 'Input pubnub publish key' # set pubnub publish_key

            pnconfig.subscribe_key = 'Input pubnub subscribe key' # set pubnub subscibe_key

            pnconfig.uuid = 'Input your UUID key' # set pubnub uuid_key. Just set one

            pubnub = PubNub(pnconfig) # create pubnub_object using pubnub_configuration_object

            channel='Input your channel name' # provide pubnub channel_name. Just set one



            data = {
    'message': 'Intruder Captured on photo '+ img_name
 + '. Notification sent to ' + to
    }

            pubnub.add_listener(SubscribeCallback()) # add listner_object to pubnub_object to subscribe it
            pubnub.subscribe().channels(channel).execute() # subscribe the channel (Runs in background)

            print('Connected! Standing by for command') # print confirmation msg
            pubnub.subscribe().channels(channel).execute() # subscribe the channel (Runs in background)

            pubnub.publish().channel(channel).message(data).sync() # publish the data to the mentioned channel
            alarmL()
            #flash()
            #flashes()
            
            pubnub.add_listener(SubscribeCallback()) # add listner_object to pubnub_object to subscribe it
            pubnub.subscribe().channels(channel).execute() # subscribe the channel (Runs in background)

            print('Connected! Standing by for command') # print confirmation msg



        