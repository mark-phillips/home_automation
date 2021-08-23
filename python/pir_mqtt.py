#!/usr/bin/env python

from time import time, sleep
import datetime
import os	          # For running external commands
import RPi.GPIO as GPIO
import urlparse
import paho.mqtt.client as paho
import configparser
#=====================================================================================
#  Handle movement 
#
def motion_detected(PIN):
    global need_to_cancel_motion 
    topic = pins[str(PIN)] 

    if (GPIO.input(PIN )):
###        if ( need_to_cancel_motion == False): # don't alert if we already did 
          logit("motion detected " + topic)
          sendmqtt("motion", topic, False)
          need_to_cancel_motion=True
    else:                                    
###        if ( need_to_cancel_motion):
          sendmqtt("no_motion", topic, False)
          logit( " no motion " + topic ) 
          need_to_cancel_motion=False
#
#  Send message
#
def sendmqtt(mess,topic, retention):
    mqttc.connect(url.hostname, url.port)
    mqttc.publish(topic, mess, retain=retention)
#
#  Print message prepended by date
#
def logit(text):
  now = datetime.datetime.now()
  print str(now) + " - " + str(text)

#=====================================================================================
homedir = os.path.expanduser("~")
inifile = open(homedir + "/.pir.ini")
config = configparser.ConfigParser()
config.read_file(inifile)

# Setup Gpio
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
need_to_cancel_motion=False

if not config.has_section("pins"):
  print('Config file does not have section "pins" - exiting.')
  exit(1)

if not config.has_section("mqtt_server"):
  print('Config file does not have section "mqtt_server" - exiting.')
  exit(1)

pins = config['pins']

# Print config 
#url_str = 'mqtt://home.local:1883'
url_str = config['mqtt_server']['mqtt_url']
if config.has_option('mqtt_server', 'mqtt_user'):
    mqtt_user = config['mqtt_server']['mqtt_user']
else:
    mqtt_user = ""

if config.has_option('mqtt_server', 'mqtt_password'):
    mqtt_password = config['mqtt_server']['mqtt_password']
else:
    mqtt_password = ""

print "============================================================"
logit( "Starting pir_mqtt with config:")
print("\n  MQTT URL:      %s" % ( url_str ))
print("  MQTT User:     %s" % ( mqtt_user ))
print("  MQTT Password: %s" % ( mqtt_password ))
print("\n  Pins / Topics:")
for pin, topic in pins.items():
  print("    %s  -  %s" % (pin, topic))
print "------------------------------------------------------------"

#
# Set up GPIO pins for input 
#
for pin in pins.keys():
    GPIO.setup(int(pin), GPIO.IN)

#
# Mqtt 
#
mqttc = paho.Client()
url = urlparse.urlparse(url_str)
### mqttc.username_pw_set("user", "password")



# Add callbacks
for pin, value in pins.items():
    GPIO.add_event_detect(int(pin), GPIO.BOTH, callback=motion_detected, bouncetime=150)

try:
  for pin, topic in pins.items():
        sendmqtt("Connected", topic + "/" + "status", True)
  logit("connected")

  while True:
    sleep(1)    # Dont send too many messages

except KeyboardInterrupt:
  print " Quit"

finally  :
  for pin, topic in pins.items():
    sendmqtt("Disconnected", topic + "/" + "status", True)
  GPIO.cleanup()
