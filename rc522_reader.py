from subprocess import check_call

from gpiozero import Button
from mfrc522 import SimpleMFRC522

import media.media_list
import media_player
from screen_toggle import *

# Settings
SCREEN_TURN_OFF = False
START_UP_SOUND = True
FORCE_ANALOG_SOUND = False

# Button Pins
black_button = 19
green_button = 13
blue_button = 26
yellow_button = 6


def power_button():
    print("\n Shutting down the Device")
    check_call(['sudo', 'poweroff'])


def pause_button():
    print("\n Pause button pressed")

    try:
        player
    except NameError:
        print("\n No music player defined")
    else:
        player.play_pause()


def back_button():
    print("\n Stopping all Media")
    media_player.stop_all_media()


def forward_button():
    print("\n forward button pressed")

    toggle_display(True)


def main():
    # if START_UP_SOUND:
    #     startup = pygame.mixer.Sound(
    #         "/home/pi/Raspi_RFID_player/assets/startup.wav")
    #     startup.play()

    print("\n RFID Player Ready")

    global player

    # GPIO   3, 4, 17 and 10
    button1 = Button(black_button, hold_time=2)
    button2 = Button(yellow_button, bounce_time=0.1)
    button3 = Button(blue_button, bounce_time=0.1)
    button4 = Button(green_button, bounce_time=0.1)

    # Mapping functions to button presses
    button1.when_pressed = power_button
    button2.when_pressed = back_button
    button3.when_pressed = pause_button
    button4.when_pressed = forward_button

    reader = SimpleMFRC522()

    # Main Loop of the App: Constantly checking for new  RFID input
    while True:
        code = check_for_input(reader)
        # Check if found code occurs in media list
    #  for m in media_list:
    #      if m[1] == code:
    #          print("Playing " + m[0] + " at " + m[2])
    #          player = media_player.play_media(m[2])


media_list = media.media_list.list


def check_for_input(reader):
    if reader.PICC_IsNewCardPresent():
        if reader.PICC_ReadCardSerial():
            print("RFID TAG ID:")
            for i in range(reader.uid.size):
                print(hex(reader.uid.uidByte[i]))
                print(" ")
                print()


if __name__ == "__main__":
    main()
