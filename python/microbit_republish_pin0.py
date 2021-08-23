#!/usr/bin/python3
import os	   
import dbus	   
from time import time, sleep
import sys
import urllib.parse
import paho.mqtt.client as paho
import configparser
from bluezero import microbit
from bluezero import async_tools
import datetime
from pathlib import Path


#================================================================
# Publish message
# ---------------
def sendmqtt(mess,topic, retention):
    mqttc.connect(url.hostname, url.port)
    mqttc.publish(topic, mess, retain=retention)

#================================================================
# Print message prepended by date
# --------------
def logit(text):
  now = datetime.datetime.now()
  print(str(now) + " - " + str(text))

#================================================================
# button_a_pressed
# --------------
def button_a_pressed(value):
  # value = 0 : Release
  # value = 1 : Press down
  # value = 2 : Long Press
  if (value == 1):
    logit("button A pressed")
    sendmqtt("pressed", topic + "/" + "button_A", True)
  if (value == 0):
    logit("button A released" )
    sendmqtt("release", topic + "/" + "button_A", True)
  if (value == 2):
    logit("button A long pressed")
    sendmqtt("long_pressed", topic + "/" + "button_A", True)

#================================================================
# button_b_pressed
# --------------
def button_b_pressed(value):
  if (value == 1):
    logit("button B pressed")
    sendmqtt("pressed", topic + "/" + "button_B", True)
  if (value == 0):
    logit("button B released" )
    sendmqtt("release", topic + "/" + "button_B", True)
  if (value == 2):
    logit("button B long pressed")
    sendmqtt("long_pressed", topic + "/" + "button_B", True)
  
#================================================================
# Microbit analog pin changed
# ---------------------------
def pin_changed(pin,value):
  global time_of_last_light_reading 
  global topic

  if __debug__:
    logit(f'DEBUG: Pin: { pin } value: { value }')

  if (pin == 0): 
      difference = (datetime.datetime.now() - time_of_last_light_reading ).total_seconds()
      if (difference >= 30): 
          light = value
          sendmqtt(light, topic + "/" + "light_level", False)
          logit(f'light level { light }') 
          sendmqtt(ubit.temperature, topic + "/" + "temperature", False)
          time_of_last_light_reading = datetime.datetime.now()
      else:
        if __debug__:
          logit(f'DEBUG: Too soon for light level { value } - diff { difference } ') 

#================================================================
# Hearbeat Timer
# --------------
def heartbeat_timer(): 
  global topic
  global ubit

  if __debug__:
    logit('DEBUG: heartbeat timer tick ')
    light = ubit.pin_values["0"] 
    logit(f'DEBUG: light level { light }') 

  if (not ubit.connected):
    sendmqtt("Heartbeat_Lost_Connection_To_Microbit", topic + "/" + "status", True)
    raise Exception('Heartbeat found microbit had disconnected')
  #
  # Touch file to indicate service is actively publishing
  Path('/tmp/microbit_heartbeat').touch()
  #
  # Publish heartbeat
  sendmqtt(datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), topic + "/" + "heartbeat", False)
  return True

#================================================================
# disconnect
# ----------
def disconnect(): 
  global topic
  global ubit

  sendmqtt("Disconnecting", topic + "/" + "status", True)
  logit("Disconnecting")
  ubit.disconnect()
  sendmqtt("Disconnected", topic + "/" + "status", True)

#================================================================
# connect_to_microbit
# -------------------
def connect_to_microbit(): 
  global topic
  global ubit

  while (not ubit.connected):
    try:
      ubit.connect()

    except dbus.exceptions.DBusException:
        pass

    finally  :
        if (ubit.connected):
          logit("Connected to microbit")
        else:
          logit("Connection to microbit failed")
          sleep(5)    # Dont send too many messages

#================================================================
#  M A I N L I N E 
#  ---------------

#
# Read mqtt config 

homedir = os.path.expanduser("~")
inifile = open(homedir + "/.pir.ini")
config = configparser.ConfigParser()
config.read_file(inifile)
url_str = config['mqtt_server']['mqtt_url']
if config.has_option('mqtt_server', 'mqtt_user'):
    mqtt_user = config['mqtt_server']['mqtt_user']
else:
    mqtt_user = ""
if config.has_option('mqtt_server', 'mqtt_password'):
    mqtt_password = config['mqtt_server']['mqtt_password']
else:
    mqtt_password = ""
print("============================================================")
logit( "Starting " + sys.argv[0])
print( "Config:")
print("\n  MQTT URL:      %s" % ( url_str ))
print("  MQTT User:     %s" % ( mqtt_user ))
print("  MQTT Password: %s" % ( mqtt_password ))
print("------------------------------------------------------------")

#
# Set up Mqtt client 
#
mqttc = paho.Client()
url = urllib.parse.urlparse(url_str)
topic="homeassistant/microbit"
time_of_last_light_reading = datetime.datetime.now() 

sendmqtt("Starting", topic + "/" + "status", True)
#
# Setup heartbeat timer 
#
#https://bluezero.readthedocs.io/en/v0.4.0/shared.html#module-bluezero.async_tools
async_tools.add_timer_seconds(10,heartbeat_timer)

#
# Connect to Microbit
#
ubit = microbit.Microbit(adapter_addr='B8:27:EB:89:3A:F3', device_addr='C5:2D:2F:88:DA:CD')
connect_to_microbit() 

try:
#
# Set up Microbit
#
  print(f'Services: { ubit.services_available() }')
  sleep(2)    # Wait for microbit to settle
  logit("Enable pin 0:")
  ubit.set_pin(0, True, True)

  ubit.subscribe_button_a(button_a_pressed)
  ubit.subscribe_button_b(button_b_pressed)
  ubit.subscribe_pins(pin_changed)

  sendmqtt("Connected", topic + "/" + "status", True)

  logit("Running loop")
  ubit.run_async()

  while False:
#  while True:
    sendmqtt(ubit.temperature, topic + "/" + "temperature", True)
    sendmqtt(light, topic + "/" + "light_level", True)
    sleep(5)    # Dont send too many messages
    if (not ubit.connected):
      connect_to_microbit() 

except KeyboardInterrupt:
  logit("Cancelled by user")

finally  :
  disconnect()
