import os
import sys
import threading
import time
from subprocess import check_call

import vlc
from gpiozero import Button
from mfrc522 import SimpleMFRC522

import light_control

# Settings
SCREEN_TURN_OFF = False
START_UP_SOUND = True
START_UP_ANIMATION = False
FORCE_ANALOG_SOUND = False
CONSOLE_OUTPUT = False
SLEEP_DELAY = 0.2  # Delay between RFID Scans

FILEPATH = "/home/pi/rfid_service_table/assets/"

# light ring
LIGHT_COLOR = light_control.colors["Teal"]

# Button Pins
power_button_pin = 19
stop_button_pin = 13
pause_button_pin = 26
light_button_pin = 6

global media
last_media_code = -1


def play_media(filename):
    filename = FILEPATH + filename

    global media
    media = vlc.MediaPlayer(filename)
    media.set_fullscreen(True)

    # start playing video
    media.play()


def stop_media():
    global media
    media.stop()
    global last_media_code
    last_media_code = -1
    clear_console()


def play_pause():
    global media

    print("Play/Pause")

    if media is not None:
        media.pause()
    clear_console()


def power_button():
    print("Shutting down the Device")
    light_control.turn_off_lights()
    check_call(['sudo', 'poweroff'])


def stop_button():
    print("Stopping all Media")
    if not stop_media():
        print("NO")


def placeholder_button():
    print("Starting  lightring")

    fill_light(25, LIGHT_COLOR, 0)
    timed_thread1 = threading.Thread(fill_light(100, LIGHT_COLOR, 5 * 60))
    timed_thread2 = threading.Thread(fill_light(50, LIGHT_COLOR, 10 * 60))
    timed_thread1.start()
    timed_thread2.start()


def fill_light(percentage, color, delay):
    time.sleep(delay)
    light_control.fill_light_ring(
        percentage, color)


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
            global media
            play_media("startup.wav")
            print("\n RFID Player Ready")

        # Testvideo
        media_list = []
        test_video = "Testvideo", 524887201261, "testvideo.mp4"
        test_audio = "Testaudio", 252006438210, "testaudio.mp3"
        media_list.append(test_video)
        media_list.append(test_audio)

        # media_list = media.media_list.list

        button1 = Button(power_button_pin, hold_time=2)
        button2 = Button(stop_button_pin, bounce_time=0.1)
        button3 = Button(pause_button_pin, bounce_time=0.1)
        button4 = Button(light_button_pin, bounce_time=0.1)

        # Mapping functions to button presses
        button1.when_pressed = power_button
        button2.when_pressed = stop_button
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
                    for m in media_list:
                        if m[1] == code:
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
