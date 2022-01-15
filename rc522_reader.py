import time
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
SLEEP_DELAY = 0.2

# Button Pins
black_button = 19
green_button = 13
blue_button = 26
yellow_button = 6


def power_button():
    print("Shutting down the Device")
    check_call(['sudo', 'poweroff'])


def pause_button():
    print("Play/Puse")

    try:
        player
    except NameError:
        print("No music player defined")
    else:
        player.play_pause()


def back_button():
    print("Stopping all Media")
    media_player.stop_all_media()


def forward_button():
    print("forward button pressed")
    if SCREEN_TURN_OFF:
        toggle_display(True)


def main():
    if START_UP_SOUND:
        media_player.play_feedback_sound()
    print("\n RFID Player Ready")

    global player

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

    last_codes_lst = [-1, -1, -1, -1, -1]
    last_media_code = -1
    is_paused = False

    # Main Loop of the App: Constantly checking for new  RFID input
    while True:
        code = read_tag(reader)
        last_codes_lst.insert(0, code)
        last_codes_lst.pop()
        # print(lastcode)

        comp = sum(last_codes_lst)
        if comp == 0:
            if not is_paused:
                pause_button()
                is_paused = True
        # Trigger Play Command if code occurs exactly once in list of last codes
        elif comp == code:
            media_player.play_feedback_sound()
            is_paused = False
            if comp == last_media_code:
                pause_button()
                print("resume")
            else:
                last_media_code = code
                # Check if found code occurs in media list
                for m in media_list:
                    if m[1] == code:
                        print("Playing " + m[0] + " at " + m[2])
                    player = media_player.play_media(m[2])

                print("starting" + str(code))

        time.sleep(SLEEP_DELAY)


def read_tag(reader):
    if reader.read_id_no_block():
        return reader.read_id()
    else:
        return 0


media_list = media.media_list.list

if __name__ == "__main__":
    main()
