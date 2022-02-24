#!/usr/bin/env python3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
try:
    id, text = reader.read()
    print("TAG ID")
    print(id)

finally:
    GPIO.cleanup()
