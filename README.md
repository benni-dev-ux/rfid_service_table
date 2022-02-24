# RFID service Table

Version #2 of the RFID Service Table Controlled by a Raspberry PI

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

Clone this repository into the home directory of the PI

    /home/pi/rfid_service_table

Run the table_reader.py script

    sudo python3 table_reader.py

## How to Input Media

1. Put all video and audio files into the media folder

   /home/pi/rfid_service_table/media

2. Add files and corresponding RFID Tag IDs into the [media list](media/media_list.py)

If the RFID Tag IDs are unclear, run this [script](util/simple_tag_reader.py) and swipe the card across the reader
