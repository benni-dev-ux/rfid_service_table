import sys
import time
from subprocess import check_call

from gpiozero import Button
from mfrc522 import SimpleMFRC522

import light_control
import media_player

# Settings
SCREEN_TURN_OFF = False
START_UP_SOUND = True
START_UP_ANIMATION = True
FORCE_ANALOG_SOUND = False
SLEEP_DELAY = 0.2

# light ring
LIGHT_COLOR = light_control.colors["Teal"]
LIGHTRING_PERCENTAGE = 10

# Button Pins
power_button_pin = 19
stop_button_pin = 13
pause_button_pin = 26
light_button_pin = 6


def power_button():
    print("Shutting down the Device")
    light_control.turn_off_lights()
    check_call(['sudo', 'poweroff'])


def play_pause_button():
    print("Play/Pause")

    try:
        player
    except NameError:
        pass
    else:
        player.play_pause()


def stop_button():
    print("Stopping all Media")
    media_player.stop_all_media()


def placeholder_button():
    print("Adjusting lightring")

    global LIGHTRING_PERCENTAGE
    LIGHTRING_PERCENTAGE += 10
    if LIGHTRING_PERCENTAGE > 100:
        LIGHTRING_PERCENTAGE = 0

    light_control.fill_light_ring(
        LIGHTRING_PERCENTAGE, LIGHT_COLOR)


def main():
    try:

        # Simple start up Animation
        if START_UP_ANIMATION:
            light_control.fill_light_ring(100, light_control.colors["Navy"])
            light_control.fill_light_ring(LIGHTRING_PERCENTAGE, LIGHT_COLOR)

        if START_UP_SOUND:
            media_player.play_sound_effect("startup.wav")
            print("\n RFID Player Ready")

        global player

        # Testvideo
        media_list = []
        test_video = "Testvideo", 524887201261, "/home/pi/rfid_service_table/assets/testvideo.mp4"
        media_list.append(test_video)

        # media_list = media.media_list.list

        button1 = Button(power_button_pin, hold_time=2)
        button2 = Button(stop_button_pin, bounce_time=0.1)
        button3 = Button(pause_button_pin, bounce_time=0.1)
        button4 = Button(light_button_pin, bounce_time=0.1)

        # Mapping functions to button presses
        button1.when_pressed = power_button
        button2.when_pressed = stop_button
        button3.when_pressed = play_pause_button
        button4.when_pressed = placeholder_button

        reader = SimpleMFRC522()

        last_codes_lst = [-1, -1, -1, -1, -1]
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
                    play_pause_button()
                    is_paused = True

            elif comp == code:  # Trigger Play Command if code occurs exactly once in list of last codes
                media_player.play_sound_effect("beep.mp3")
                is_paused = False
                if comp == last_media_code:
                    play_pause_button()
                    print("resuming")
                else:
                    last_media_code = code
                    # Check if found code occurs in media list
                    for m in media_list:
                        if m[1] == code:
                            print("Playing " + m[0] + " at " + m[2])
                        player = media_player.play_media(m[2])

                    print("starting" + str(code))

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
