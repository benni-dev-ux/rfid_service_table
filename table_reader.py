import os
import sys
import time
from datetime import timedelta
from subprocess import check_call

import vlc
from gpiozero import Button
from mfrc522 import SimpleMFRC522
from timeloop import Timeloop

import light_control
import media.media_list

# Settings
SCREEN_TURN_OFF = False
START_UP_SOUND = True
START_UP_ANIMATION = True
FORCE_ANALOG_SOUND = False
CONSOLE_OUTPUT = False
SLEEP_DELAY = 0.2  # Delay between RFID Scans

FILEPATH = "/home/pi/rfid_service_table/media/"

# light ring
LIGHT_COLOR = light_control.colors["Teal"]

# Button Pins
power_button_pin = 19
stop_button_pin = 13
pause_button_pin = 26
light_button_pin = 6

global media_player
last_media_code = -1

lightring_counter = 0
lightring_fill_amounts = [15, 100, 33, 63, 47, 30, 15, 33, 52, 55, 80, 100]

tl = Timeloop()


def play_media(filename):
    filename = FILEPATH + filename

    #global media_player

    #if media_player is not None:
     #   stop_media()
    global media_player
    #media_player.stop()
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
    clear_console()


def power_button():
    print("Shutting down the Device")
    light_control.turn_off_lights()
    check_call(['sudo', 'poweroff'])


@tl.job(interval=timedelta(minutes=2))
def fill_light():
    global lightring_counter
    global lightring_fill_amounts
    if lightring_counter == len(lightring_fill_amounts):
        lightring_counter = 0

    light_control.fill_light_ring(lightring_fill_amounts[lightring_counter], LIGHT_COLOR)
    lightring_counter += 1


def placeholder_button():
    global tl
    tl.start()
    clear_console()


def clear_console():
    if not CONSOLE_OUTPUT:
        os.system("clear")


def main():
    try:

        # Simple start up Animation
        if START_UP_ANIMATION:
            light_control.fill_light_ring(100, LIGHT_COLOR)
            light_control.fill_light_ring(0, LIGHT_COLOR)

        if START_UP_SOUND:
            global media_player
            play_media("startup.wav")
            print("\n RFID Player Ready")

        # Link to media list
        tag_list = media.media_list.list

        button1 = Button(power_button_pin, hold_time=2)
        button2 = Button(stop_button_pin, bounce_time=0.1)
        button3 = Button(pause_button_pin, bounce_time=0.1)
        button4 = Button(light_button_pin, bounce_time=0.1)

        # Mapping functions to button presses
        button1.when_pressed = power_button
        button2.when_pressed = stop_media
        button3.when_pressed = play_pause
        button4.when_pressed = placeholder_button

        reader = SimpleMFRC522()

        last_codes_lst = [-1, -1, -1, -1, -1]
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

            elif comp == code:  # Trigger Play Command if code occurs exactly once in list of last codes

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
        global tl
        tl.stop()
        sys.exit()


def read_tag(reader):
    """returns id from rfid tag if null returns 0"""
    if reader.read_id_no_block():
        return reader.read_id()
    else:
        return 0


if __name__ == "__main__":
    main()
