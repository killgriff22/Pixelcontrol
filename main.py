"""
Important:
The auto-reloader restarts the Pi.
You will need to log back into the Pi after the auto-reloader restarts it.
startup takes 30 seconds to 2 minutes, if it still doesnt work, contact me.
the script will start up automatically after the pi restarts.
if you want to view the output of the script, you can do so by running the command "screen -x" when logged into the Pi
When in visual studio, the only module you shouldnt have is "board".
"board" is a module that is only available on the raspberry pi, and is only referenced once.
"""
import os
import flask
import time
import board
import neopixel
import threading

app = flask.Flask(__name__)
def impose_color(t,value):
    return tuple(int((ele1 * value)//1) for ele1 in t)
pixel_pin = board.D18
num_pixels = 60
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
)
pixels.fill((0, 0, 0))
pixels.show()
COLOR = (153, 103, 52)

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


def rainbow_cycle(j,*args):
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + j
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()

def chase(pos,front_tail_width=3,back_tail_width=3):
    pixels.fill((0, 0, 0))
    for i in range(1,front_tail_width+1):
        pixels[pos-i if pos-i >= 0 else 0] = impose_color(COLOR,1/i)
    for i in range(1,back_tail_width+1):
        pixels[pos+i if pos+i < num_pixels else -1] = impose_color(COLOR,1/i)
    pixels[pos] = COLOR
    pixels.show()
    
def bounce(pos,front_tail_width=3,back_tail_width=3):
    #this is literally just the chase function, called a different name
    pixels.fill((0, 0, 0))
    for i in range(1,front_tail_width+1):
        pixels[pos-i if pos-i >= 0 else 0] = impose_color(COLOR,1/i)
    for i in range(1,back_tail_width+1):
        pixels[pos+i if pos+i < num_pixels else -1] = impose_color(COLOR,1/i)
    pixels[pos if pos < num_pixels else -1] = COLOR
    pixels.show() 

import thread_variable_utility as tvu # this has to be imported after the functions are defined because the module relies on the above functions

def blank(*args):
    return

def off(*args):
    pixels.fill((0, 0, 0))
    pixels.show()
    return
PATTERNS = {
    'rainbow': rainbow_cycle,
    'chase':chase,
    'bounce':bounce,
    "off":off
}

@app.route('/')
def index():
    heap_patterns = """"""
    for pattern in PATTERNS:
        heap_patterns += f'<a href="/run/{pattern}">{pattern}</a><br>'
    heap_patterns += f"""<a href="/pull">Pull</a><br>"""
    return flask.render_template('index.html',patterns=heap_patterns)

@app.route('/run/<pattern_name>')
def run_pattern(pattern_name):
    if pattern_name in PATTERNS:
        tvu.write("pattern.py",[PATTERNS[pattern_name],0,0,0,1,1])
    return flask.redirect('/')

@app.route('/speed/<int:speed_>')
def set_speed(speed_):
    pattern = tvu.read("pattern.py")
    pattern[4] = speed_
    pattern[0] = pattern[0].__name__
    tvu.write("pattern.py",pattern)
    return flask.redirect('/')

@app.route('/pull')
def pull():
    os.system("git pull")
    return flask.redirect('/')
def loop():
    while True:
        pattern = tvu.read("pattern.py")
        pattern[0](*pattern[1:4])#this is the bit of code that made me question copilot for a moment
        pattern[1] += pattern[4]*pattern[5]
        match pattern[0].__name__:
            case "chase":
                pattern[1] %= num_pixels# take the remainder of the division of the current pixel position by num_pixels so we dont go out of bounds of the list
            case "rainbow_cycle":
                pattern[1] %= 256 # take the remainder of the division of the current pixel position by 256 so that we dont mess up the rainbow math
            case "bounce":
                if pattern[1] > num_pixels-1 or pattern[1] < 0:
                    pattern[5] *= -1
        print(pattern[4], pattern[1], pattern[5])
        pattern[0] = pattern[0].__name__
        tvu.write("pattern.py",pattern)
        time.sleep(0.1)
mainthread = threading.Thread(target=loop)
mainthread.start()
app.run('0.0.0.0',port=6060,debug=True)