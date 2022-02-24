import vlc

media = vlc.MediaPlayer()


def play_media(filename):
    # creating vlc media player object
    global media
    media = vlc.MediaPlayer(filename)

    # start playing video
    media.play()



def stop_media():
    global media
    media.stop()


def play_pause():
    global media
    media.pause()
