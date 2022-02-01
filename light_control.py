import board
import neopixel
import time


pixel_pin = board.D18
num_pixels = 32
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


pixels.fill((255,0,0))

#for i in range(32):
    
 #   pixels[i] = (0,255,0)
  #  time.sleep(1)
