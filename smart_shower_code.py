 ##!/usr/bin/env python
## This system is used to Display whether a seat is occupied or not
## Cite: Hossain, S., & Abdelgawad, A. (2023). Low-Cost Architecture for an Advanced Smart Shower System Using Internet of Things Platform. arXiv preprint arXiv:2311.07712.

__author__ = 'Shadeeb Hossain'
# This program logs a Raspberry Pi's Ultrasonic Sensor to a Thingspeak Channel

'''-------------------LIBRARY Setup-----------------------------------'''
import http.client
import urllib.parse
import urllib.request
import json
import time
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
'''-------------------VARIABLE Setup-----------------------------------'''
key = '' #Enter your Primary Channel WRITE API Key
READ_API_KEY='' #Enter your Observation Channel READ API Key
CHANNEL_ID='' #Enter your Observation Channel ID Number
entry_ID=0 #Sequence number of the receiving Observation Channel,

sleep = 1 #How many seconds to sleep between posts to the channel
'''------------------GPIO SETUP---------------------------------------'''
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_LED = 16
GPIO_HOT = 26
GPIO_cold = 19
GPIO_normal = 20
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED,GPIO.OUT)
GPIO.setup(GPIO_HOT,GPIO.OUT)
GPIO.setup(GPIO_cold,GPIO.OUT)
GPIO.setup(GPIO_normal,GPIO.OUT)
def distance():
     # set Trigger to HIGH
     GPIO.output(GPIO_TRIGGER, True)

     # set Trigger after 0.01ms to LOW
     time.sleep(0.00001)
     GPIO.output(GPIO_TRIGGER, False)

     StartTime = time.time()
     StopTime = time.time()

     # save StartTime
     while GPIO.input(GPIO_ECHO) == 0:
         StartTime = time.time()

     # save time of arrival
     while GPIO.input(GPIO_ECHO) == 1:
         StopTime = time.time()

     # time difference between start and arrival
     TimeElapsed = StopTime - StartTime
     # multiply with the sonic speed (34300 cm/s)
     # and divide by 2, because there and back
     distance = (TimeElapsed * 34300) / 2
     Dis=round(distance)
     print("Distance",Dis)

     return Dis
#while True:
    # humidity,temperature=Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, '22')
     #print ("Temperature:{0:0.1f}C Humidity :{0:0.1f}%". format(humidity,temperature))
'''-------------------DATA sending to ThingSpeak-----------------------------------'''
def sending(distance):
     while True:
         INPUT=distance
         params = urllib.parse.urlencode({'field1': INPUT, 'key':key})
         headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept":"text/plain"}
         conn = http.client.HTTPConnection("api.thingspeak.com:80")
         try:
             conn.request("POST", "/update", params, headers)
             response = conn.getresponse()
             #print (temp)
             print(response.status, response.reason)
             data = response.read()
             #conn.close()
         except:
             print ("connection failed")
         break
'''-------------------DATA receiving from ThingSpeak-----------------------------------
'''
def receiving(ID):

    conn=urllib.request.urlopen('http://api.thingspeak.com/feeds/last.json?api_key=MUBAYFQE1GLGT631')
    response = conn.read()
    print("http status code=%s" % (conn.getcode()))
    check=len(response)
    print(len(response))
    pre_entry=ID
    print('pre_entry=',pre_entry)
    data=json.loads(response.decode("utf-8"))
     #entry_ID = data['entry_id']

    if check>4:
         data=json.loads(response.decode("utf-8"))
         entry_ID = data['entry_id']
    else:
         entry_ID=ID
     
    conn.close()
    return entry_ID
while True:
     d=distance()
     time.sleep(.1)

     sending(d)
    
     
     humidity, temperature = Adafruit_DHT.read_retry(AM2302, 22)
   
    
     # print('pre_entry_ID=',entry_ID)
     if d<60:
         print('Shower Turned On')         
         print '{0:0.1f}|{1:0.1f}'. format(temperature, humidity)
         GPIO.output(GPIO_LED,GPIO.HIGH)
         #print ('The temperature is:'
     else:
         print ('Shower Room Empty')
         GPIO.output(GPIO_LED,GPIO.LOW)
         print("")
         print("")
         print("")

     if d<60:
          if temperature<22:
               print("Turn on hot shower")
               GPIO.output(GPIO_HOT,GPIO.HIGH)
               GPIO.output(GPIO_cold,GPIO.LOW)
               GPIO.output(GPIO_normal,GPIO.LOW)
               print("")
               print("")
               print("")
          elif temperature==22:
               print("Turn on normal shower")
               GPIO.output(GPIO_normal,GPIO.HIGH)
               GPIO.output(GPIO_HOT,GPIO.LOW)
               GPIO.output(GPIO_cold,GPIO.LOW)
               print("")
               print("")
               print("")
          else:
               print("Turn on cold shower")
               GPIO.output(GPIO_cold,GPIO.HIGH)
               GPIO.output(GPIO_HOT,GPIO.LOW)
               GPIO.output(GPIO_normal,GPIO.LOW)
               print("")
               print("")
               
              #last=entry_ID
     #entry_ID=receiving(entry_ID)
    # print('post_entry_ID=',entry_ID)
    # if last!=entry_ID:
         #GPIO.setwarnings(False)
        #GPIO.output(GPIO_LED,GPIO.HIGH)
        #time.sleep(.1)
       # last=entry_ID
    # else:
        # GPIO.output(GPIO_LED,GPIO.LOW)

   #  time.sleep(1)
GPIO.cleanup()

