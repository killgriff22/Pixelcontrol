import board
import neopixel
import random
import os
import thread_variable_utility as tvu
COLOR = (153, 103, 52)


def impose_color(t, value):
    return tuple(int((ele1 * value)//1) for ele1 in t)


pixel_pin = board.D18
num_pixels = 50
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow(j, *args):
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + j
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()


def chase(pos, front_tail_width=3, back_tail_width=3, r=0, g=0, b=0):
    for i in range(1, front_tail_width+1):
        pixels[pos-i if pos-i >= 0 else 0] = impose_color((r,g,b), 1/i)
    for i in range(1, back_tail_width+1):
        pixels[pos+i if pos+i < num_pixels else -1] = impose_color((r,g,b), 1/i)
    pixels[pos] = (r,g,b)
    pixels.show()


def bounce(pos, front_tail_width=3, back_tail_width=3, r=0, g=0, b=0):
    # this is literally just the chase function, called a different name
    for i in range(1, front_tail_width+1):
        pixels[pos-i if pos-i >= 0 else 0] = impose_color((r,g,b), 1/i)
    for i in range(1, back_tail_width+1):
        pixels[pos+i if pos+i < num_pixels else -1] = impose_color((r,g,b), 1/i)
    pixels[pos if pos < num_pixels else -1] = (r,g,b)
    pixels.show()


def blank(*args):
    return


def off(*args):
    pixels.fill((0, 0, 0))
    pixels.show()
    return

def full(*args):
    r,g,b=args[3:6]
    pixels.fill((r,g,b))
    pixels.show()
    return

def star(pos, front_tail_width=3, back_tail_width=3, r=0, g=0, b=0, brightness=100):
    for i in range(1, front_tail_width+1):
        pixels[pos-i if pos-i >= 0 else 0] = impose_color((r,g,b), 1/i)
    for i in range(1, back_tail_width+1):
        pixels[pos+i if pos+i < num_pixels else -1] = impose_color((r,g,b), 1/i)
    pixels[pos] = impose_color((r,g,b), brightness/100)
    pixels.show()

def stars(*args):
    r,g,b=args[3:6]
    ft,rt = args[1],args[2]
    if not os.path.exists("stars.txt"):
        tvu.write("stars.txt", [[random.randint(0,num_pixels),100] for i in range(10)])
    else:
        stars_ = tvu.read("stars.txt")
        if 
        for i in range(len(stars_)):
            if stars_[i][1] <= 0:
                stars_[i] = [random.randint(0,num_pixels),100]
            else:
                stars[i][1] -= 1
                star(stars_[i][0],ft,rt,r,g,b,stars_[i][1])
        tvu.write("stars.txt", stars_)
PATTERNS = {
    'rainbow': rainbow,
    'full':full,
    'chase': chase,
    'bounce': bounce,
    'stars': stars,
    "off": off
}