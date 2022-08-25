import multiprocessing

import board
import neopixel
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
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


def pulse_anim_light_ring(color):
    pulse = Pulse(pixels, speed=0.1, color=color, period=3)

    while True:
        pulse.animate()


def amnimate(colors):
    global t
    if t.is_alive():
        t.kill()

    t = multiprocessing.Process(target=change_anim_light_ring.main, args=colors)
    t.start()


# animation_thread = threading.Thread(target=change_anim_light_ring, name="anim_thread", args=colors)
# animation_thread.start()


def change_anim_light_ring(colors):
    colorcycle = ColorCycle(pixels, 0.5, colors=[colors[0], colors[1], colors[2]])

    while True:
        colorcycle.animate()


def sparkle_anim_light_ring(color):
    sparkle = Sparkle(pixels, speed=0.1, color=color, num_sparkles=3, mask=range(31))

    while True:
        sparkle.animate()


def sparklePulse_anim_light_ring(color):
    sparkle = SparklePulse(pixels, speed=0.1, color=color, period=10, min_intensity=0.0, max_intensity=1.0)

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
