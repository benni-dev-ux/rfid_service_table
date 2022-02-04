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
    (255, 0, 0),    	# Red
    (0, 255, 0),        # Lime
    (0, 0, 255),        # Blue
    (255, 255, 0),      # Yellow
    (0, 255, 255),      # Cyan
    (255, 0, 255),      # Magenta
    (192, 192, 192),    # Silver
    (128, 128, 128),    # Gray
    (128, 0, 0),        # Maroon
    (128, 128, 0),      # Olive
    (0, 128, 0),        # Green
    (128, 0, 128),      # Purple
    (0, 128, 128),      # Teal
    (0, 0, 128),        # Navy
    (0, 0, 0),          # off

]
