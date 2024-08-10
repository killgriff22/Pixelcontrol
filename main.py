import flask
import time
import board
import neopixel

def impose_color(t,value):
    return tuple(ele1 * value for ele1 in t)


COLOR = (255, 0, 0)
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 60
app = flask.Flask(__name__)
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)
pixels.fill((0, 0, 0))
pixels.show()

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


def rainbow_cycle(wait,j):
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + j
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()
    time.sleep(wait)

def chase(pos,front_tail_width=3,back_tail_width=3):
    pixels[pos] = COLOR
    for i in range(1,front_tail_width+1):
        pixels[pos-i] = impose_color(COLOR,1/i)
    for i in range(1,back_tail_width+1):
        pixels[pos+i] = impose_color(COLOR,1/i)
    pixels.show()
    


PATTERNS = {
    'rainbow': rainbow_cycle,
    'chase':chase,
}


@app.route('/')
def index():
    heap_patterns = """"""
    for pattern in PATTERNS:
        heap_patterns += f'<a href="/run/{pattern}">{pattern}</a><br>'
    return flask.render_template('index.html',patterns=heap_patterns)

while True:
    for i in range(num_pixels):
        chase(i,3,3)
        time.sleep(0.1)