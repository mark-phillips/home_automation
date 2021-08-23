#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
PIR_PIN1 = 18
GPIO.setup(PIR_PIN1, GPIO.IN)

try:
  print "PIR Module Test (CTRL+C to exit)"
  time.sleep(2)
  print "Ready"
  while True:
    if GPIO.input(PIR_PIN1):
      print "Motion Detected!"
    time.sleep(1)
except KeyboardInterrupt:
  print " Quit"
  GPIO.cleanup()
