import board
import neopixel
import time


pixels = neopixel.NeoPixel(board.D18, 32)

for i in range(32):
    
    pixels[i] = (0,255,0)
    time.sleep(1)
