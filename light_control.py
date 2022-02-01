import board
import neopixel
import time


gpio_pin = board.D18
num_leds = 32
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(
    gpio_pin, num_leds, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def fill_light_ring(percentage, color):
    filled = round((percentage * num_leds)/100)

    for i in range(filled):

        pixels[i] = (color)
