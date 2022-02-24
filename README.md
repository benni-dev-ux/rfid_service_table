# RFID service Table

Version #2 of the RFID Service Table
Controlled by a Raspberry PI

## Setup Guide

Connect Buttons, Lightring and RFID Reader

![image](doc/pinout_complete.png)

Install current version of Raspberry OS and run updates

    sudo apt update
    sudo apt upgrade

Setup Neopixel libraries for the Lightring

    sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
    sudo python3 -m pip install --force-reinstall adafruit-blinka

Install dependencies from requirements.txt

    sudo pip3 install requirements.txt
