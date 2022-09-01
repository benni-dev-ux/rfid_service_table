import threading

import board
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparklepulse import SparklePulse

gpio_pin = board.D18
num_leds = 32
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    gpio_pin, num_leds, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def fill_light_ring(percentage, color):
    """Fills up the tables lightring to given percentage"""
    if percentage > 100 or percentage < 0:
        percentage = 100

    filled = round((percentage * num_leds) / 100)

    for i in range(num_leds):
        if i <= filled:
            pixels[i] = color
        else:
            pixels[i] = (0, 0, 0)

        pixels.show()


def animate(state):
    def_thread = threading.Thread(name="default_animation", target=default_animation)
    play_thread = threading.Thread(name="play_animation", target=play_animation)
    pause_thread = threading.Thread(name="paused_animation", target=paused_animation)

    if state is "default":
        if play_thread.is_alive():
            play_thread.join()
        if pause_thread.is_alive():
            pause_thread.join()
        def_thread.start()

    elif state is "pause":
        if play_thread.is_alive():
            play_thread.join()
        if def_thread.is_alive():
            def_thread.join()
        pause_thread.start()
    elif state is "play":
        if def_thread.is_alive():
            def_thread.join()
        if pause_thread.is_alive():
            pause_thread.join()
        play_thread.start()


def default_animation():
    pulse = Pulse(pixels, speed=0.1, color=colors["Silver"], period=3)

    while True:
        pulse.animate()


def paused_animation():
    pulse = Pulse(pixels, speed=0.1, color=colors["Olive"], period=3)

    while True:
        pulse.animate()


def play_animation():
    sparkle = SparklePulse(pixels, speed=0.1, color=colors["Green"], period=10, min_intensity=0.0, max_intensity=1.0)

    while True:
        sparkle.animate()


def turn_off_lights():
    """turns off all leds"""
    pixels.fill((0, 0, 0))
    pixels.show()


colors = {
    "Red": (255, 0, 0),
    "Lime": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "Silver": (192, 192, 192),
    "Gray": (128, 128, 128),
    "Maroon": (128, 0, 0),
    "Olive": (128, 128, 0),
    "Green": (0, 128, 0),
    "Purple": (128, 0, 128),
    "Teal": (0, 128, 128),
    "Navy": (0, 0, 128),
    "off": (0, 0, 0)

}
