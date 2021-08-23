#!/bin/bash
echo "power off" | /usr/bin/bluetoothctl
sleep 2
echo "power on" | /usr/bin/bluetoothctl
sleep 2
/usr/bin/python3 /home/pi/bin/microbit_republish_pin0.py
