import board
import neopixel
import time


gpio_pin = board.D18
num_leds = 32
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    gpio_pin, num_leds, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def fill_light_ring(percentage, color):
    filled = round((percentage * num_leds)/100)

    for i in range(filled):

        pixels[i] = (color)
        time.sleep(0.1)
        pixels.show()


def turn_off_lights():
    pixels.fill((0,0,0))
    pixels.show()
    
fill_light_ring(100,(0,0,255))




