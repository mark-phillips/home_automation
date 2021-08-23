#!/usr/bin/env python

from time import time, sleep
import datetime
import os
import subprocess
import urlparse
import paho.mqtt.client as paho
import configparser
#=====================================================================================
#
#  Send message
#
def sendmqtt(mess,topic,retention):
  mqttc.publish(dashboard_topic + "/" + topic, mess, retain=retention)
#
#  Print message prepended by date
#
def logit(text):
  now = datetime.datetime.now()
  print str(now) + " - " + str(text)

#
# Define MQTT callbacks
#
def on_connect(client, userdata, flags, rc):
  if rc==0:
    sendmqtt("Connected", "status", True)
    logit("connected OK rc" + str(rc))
  else:
    logit("Bad connection Returned code=" + str(rc))

def on_disconnect(client, userdata, rc):
  logit("disconnecting reason  "  + str(rc))

def on_message(client, userdata, message):
  text = str(message.payload.decode("utf-8"))
  print("message received " , text)
  print("message topic=",message.topic)
  print("message qos=",message.qos)
  print("message retain flag=",message.retain)
  if "life" in text:
     subprocess.Popen(["/home/pi/bin/life.sh"]) # run in background
     return
  if "bedroom" in text:
#     subprocess.Popen(["/home/pi/bin/unicorn_hat_attention.py","5"]) 
     subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/bed-king.png"])
     return
  if "front_door" in text:
     subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/door-open.png"])
     return
  if "stairs" in text:
     subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/stairs-box.png"])
     return
  if "landing" in text:
     subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/landing.png"])
     return
  if text.startswith("Weather:"):
      if "rainy" in text.lower():
         subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/rain.png"])
         return
      if "partly cloudy" in text.lower():
         subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/partly-cloudy-day.png"])
         return
      if "partly cloudy" in text.lower():
        if "sun: above_horizon" in text.lower(): 
          subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/partly-cloudy-day.png"])
        else: 
         subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/partly-cloudy-night.png"])
        return
      if "sunny" in text.lower():
        if "sun: above_horizon" in text.lower(): 
          subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/clear-day.png"])
        else: 
         subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/clear-night.png"])
        return
      if "cloudy" in text.lower():
         subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/cloudy.png"])
         return
      if "windy" in text.lower():
         subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/windy.png"])
         return
      if "snow" in text.lower():
         subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/snow.png"])
         return
      if "fog" in text.lower():
         subprocess.Popen(["/home/pi/bin/unicorn_hat_show_png.py","/home/pi/bin/unicorn_hat_icons/fog.png"])
         return

  text_process = subprocess.Popen(["/home/pi/bin/unicorn_hat_dashboard_text.py",text])
  text_process.communicate()  # Will block for text to finish

#  os.system('~/bin/unicorn_hat_dashboard_text.py "' + text + '"')

#=====================================================================================
dashboard_topic="homeassistant/dashboard"
homedir = os.path.expanduser("~")
inifile = open(homedir + "/.pir.ini")
config = configparser.ConfigParser()
config.read_file(inifile)

if not config.has_section("mqtt_server"):
  print('Config file does not have section "mqtt_server" - exiting.')
  exit(1)

# Print config 
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
print "------------------------------------------------------------"

#
# Mqtt connection
#
mqttc = paho.Client()
url = urlparse.urlparse(url_str)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(url.hostname, url.port)
mqttc.subscribe(dashboard_topic + "/messages", qos=0)

try:
  mqttc.loop_forever()

except KeyboardInterrupt:
  logit("Cancel requested by keyboard")

finally  :
  sendmqtt("Disconnected", "status", True)
  mqttc.disconnect()
