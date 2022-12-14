import os
import sys
from subprocess import check_call

import vlc
from gpiozero import Button
from mfrc522 import SimpleMFRC522

import media.media_list

# Settings
START_UP_SOUND = True
FORCE_ANALOG_SOUND = False
CONSOLE_OUTPUT = False
SLEEP_DELAY = 0.30  # Delay between RFID Scans

FILEPATH = "/home/pi/rfid_service_table/media/"

# Button Pins
power_button_pin = 19

global media_player
last_media_code = -1


def play_media(filename):
    filename = FILEPATH + filename

    global media_player

    media_player = vlc.MediaPlayer(filename)
    media_player.set_fullscreen(True)

    media_player.play()


def play_pause():
    global media_player

    if media_player is not None:
        media_player.pause()

    clear_console()


def reboot():
    print("Rebooting the Device")
    check_call(["sudo", "reboot"])


def shutdown():
    print("Shutting down the Device")
    check_call(["sudo", "poweroff"])


def clear_console():
    if not CONSOLE_OUTPUT:
        os.system("clear")


def main():
    try:

        if START_UP_SOUND:
            global media_player
            play_media("startup.wav")
            print("\n RFID Player Ready")

        # Link to media list
        tag_list = media.media_list.media_IDs

        # Mapping functions to button presses
        power_button = Button(power_button_pin, hold_time=2)
        power_button.when_held = reboot
        power_button.when_released = shutdown

        reader = SimpleMFRC522()

        # Main Loop of the App: Constantly checking for new  RFID input
        while True:
            code = read_tag(reader)
            for m in tag_list:
                if m[1] == code:
                    global media_player
                    if media_player is not None:
                        media_player.stop()

                    play_media("beep.mp3")
                    print("Playing " + m[0] + " at " + m[2])
                    play_media(m[2])

                    print("starting" + str(code))
                    clear_console()

                # time.sleep(SLEEP_DELAY)  # resume after delay
    except KeyboardInterrupt:
           sys.exit()


def read_tag(reader):
    """returns id from rfid tag if null returns 0"""
    if reader.read_id_no_block():
        return reader.read_id()
    else:
        return 0


if __name__ == "__main__":
    main()
