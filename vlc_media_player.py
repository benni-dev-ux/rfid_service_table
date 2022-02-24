import vlc



def play_media(filename):
    # creating vlc media player object
    filename = "/home/pi/rfid_service_table/assets/" + filename

    #if media.is_playing():
     #   media.stop()
    media = vlc.MediaPlayer(filename)

    # start playing video
    media.play()
    
    return media



def stop_media(media):
    
    media.stop()


def play_pause(media):

    media.pause()
