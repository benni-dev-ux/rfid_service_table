import os

from omxplayer.player import OMXPlayer

from reader import SCREEN_TURN_OFF
from screen_toggle import *
import reader


def is_playing():
    """Check if OMX Player is playing a Video/Audio file
    (True if at least 2 OMX Processes)"""

    process_name = 'omxplayer'
    tmp = os.popen("ps -Af").read()
    process_count = tmp.count(process_name)

    is_currently_playing = False

    if process_count >= 1:
        is_currently_playing = True

    return is_currently_playing


def play_media(filename):
    """ Plays file (audio or video) in OMXPlayer"""
    if is_playing():
        print("Cancelling currently playing video/audio")

        # Kill existing OMX Processes
        command1 = "sudo killall -s 9 omxplayer.bin"
        os.system(command1)

    # toggle screen off for audio
    if SCREEN_TURN_OFF:
        if filename.endswith(".mp4"):
            toggle_display(True)
        elif filename.endswith(".mp3"):
            toggle_display(False)

    # starting OMXPlayer subprocess with video or audio file
    args = ""
    if (reader.FORCE_ANALOG_SOUND):
        args = "-o local"
    player = OMXPlayer(filename, args=args,
                       dbus_name='org.mpris.MediaPlayer2.omxplayer1')
    return player


def stop_all_media():
    """Kills all running OMX processes"""

    command = "sudo killall -s 9 omxplayer.bin"
    os.system(command)
