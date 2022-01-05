# function derived from:
# https://www.youtube.com/watch?v=lETqSCimcyM

from subprocess import run


def toggle_display(active):
    if active:
        run('vcgencmd display_power 1', shell=True)
    else:
        run('vcgencmd display_power 0', shell=True)
