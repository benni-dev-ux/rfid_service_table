from subprocess import check_call

import pygame
from gpiozero import Button

import media.media_list
import media_player
from screen_toggle import *

# Settings
SCREEN_TURN_OFF = False
START_UP_SOUND = True
FORCE_ANALOG_SOUND = False


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
    if START_UP_SOUND:
        startup = pygame.mixer.Sound(
            "/home/pi/Raspi_RFID_player/assets/startup.wav")
        startup.play()

    print("\n RFID Player Ready")

    global player

    # GPIO   3, 4, 17 and 10
    button1 = Button(3, hold_time=2)
    button2 = Button(4, bounce_time=0.1)
    button3 = Button(17, bounce_time=0.1)
    button4 = Button(10, bounce_time=0.1)

    # Mapping functions to button presses
    button1.when_pressed = power_button
    button2.when_pressed = back_button
    button3.when_pressed = pause_button
    button4.when_pressed = forward_button

    # Main Loop of the App: Constantly checking for new  RFID input
    while True:
        code = check_for_input()
        # Check if found code occurs in media list
        for m in media_list:
            if m[1] == code:
                print("Playing " + m[0] + " at " + m[2])
                player = media_player.play_media(m[2])


# Testfiles
# video1 = ["testvideo", 6267256,
#          "/home/pi/Raspi_RFID_player/assets/testvideo.mp4"]
# audio1 = ["testaudio", 6268576,
#          "/home/pi/Raspi_RFID_player/assets/testaudio.mp3"]
#
# media_list = [video1, audio1]

media_list = media.media_list.list


def check_for_input():
    code = input('\n Scan RFID tag to Play Media \n')
    # Strip first three Characters to avoid escape characters
    code = code[3:]
    # Cast to int
    code = int(code)
    return code


if __name__ == "__main__":
    main()
