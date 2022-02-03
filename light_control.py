import time

import board
import neopixel

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

    for i in range(filled):
        pixels[i] = color
        time.sleep(0.05)
        pixels.show()


def turn_off_lights():
    """turns off all leds"""
    pixels.fill((0, 0, 0))
    pixels.show()


colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (192, 192, 192),
    (128, 128, 128),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),
    (0, 0, 0),

]
