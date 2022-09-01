import os
import sys
import time
from subprocess import check_call

import vlc
from gpiozero import Button
from mfrc522 import SimpleMFRC522

import light_control
import media.media_list

# Settings
START_UP_SOUND = True
START_UP_ANIMATION = True
FORCE_ANALOG_SOUND = False
CONSOLE_OUTPUT = True
SLEEP_DELAY = 0.33  # Delay between RFID Scans

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

    # start playing video
    media_player.play()


def stop_media():
    print("Stopping all media")
    global media_player
    media_player.stop()
    global last_media_code
    last_media_code = -1
    clear_console()


def play_pause():
    global media_player

    print("Play/Pause")

    if media_player is not None:
        media_player.pause()
        #light_control.animate("pause")
    else:
        #light_control.animate("play")
    clear_console()


def reboot():
    print("Rebooting the Device")
    light_control.turn_off_lights()
    check_call(["sudo", "reboot"])


def shutdown():
    print("Shutting down the Device")
    light_control.turn_off_lights()
    check_call(["sudo", "poweroff"])


def clear_console():
    if not CONSOLE_OUTPUT:
        os.system("clear")


def main():
    try:

        # Simple start up Animation
        if START_UP_ANIMATION:
            light_control.animate("default")

        if START_UP_SOUND:
            global media_player
            play_media("startup.wav")
            print("\n RFID Player Ready")

        # Link to media list
        tag_list = media.media_list.media_IDs

        # Mapping functions to button presses
        power_button = Button(power_button_pin, hold_time=3)
        power_button.when_held = reboot
        power_button.when_released = shutdown

        reader = SimpleMFRC522()

        last_codes_lst = [-1, -1, -1]
        global last_media_code
        last_media_code = -1
        is_paused = False

        # Main Loop of the App: Constantly checking for new  RFID input
        while True:
            code = read_tag(reader)
            last_codes_lst.insert(0, code)
            last_codes_lst.pop()

            comp = sum(last_codes_lst)
            if comp == 0:  # if sum of last 5 codes =0 -> Pause Media
                if not is_paused:
                    play_pause()
                    is_paused = True

            elif (
                    comp == code
            ):  # Trigger Play Command if code occurs exactly once in list of last codes

                is_paused = False
                if comp == last_media_code:
                    play_pause()
                    print("resuming")
                else:
                    last_media_code = code
                    # Check if found code occurs in media list
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

            time.sleep(SLEEP_DELAY)  # resume after delay
    except KeyboardInterrupt:
        light_control.turn_off_lights()

        sys.exit()


def read_tag(reader):
    """returns id from rfid tag if null returns 0"""
    if reader.read_id_no_block():
        return reader.read_id()
    else:
        return 0


if __name__ == "__main__":
    main()
