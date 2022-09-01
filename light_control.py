import multiprocessing

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


def animate_default():
    if t_pau.is_alive():
        t_pau.terminate()
    if t_pla.is_alive():
        t_pla.terminate()

    global t_def
    t_def = multiprocessing.Process(target=default_animation)
    t_def.start()


def animate_pause():
    if t_def.is_alive():
        t_def.terminate()
    if t_pla.is_alive():
        t_pla.terminate()

    global t_pau
    t_pau = multiprocessing.Process(target=default_animation)
    t_pau.start()


def animate_play():
    if t_pau.is_alive():
        t_pau.terminate()
    if t_def.is_alive():
        t_def.terminate()

    global t_pla
    t_pla = multiprocessing.Process(target=default_animation)
    t_pla.start()


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
