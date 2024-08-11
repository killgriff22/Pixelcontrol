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


def impose_color(t,value):
    return tuple(int((ele1 * value)//1) for ele1 in t)


COLOR = (153, 103, 52)
direction = 1
speed = 1
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


def rainbow_cycle(j):
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
    pixels[pos] = COLOR
    pixels.show() 

PATTERNS = {
    'rainbow': rainbow_cycle,
    'chase':chase,
    'bounce':bounce
}
pattern = [chase,0,3,3]

@app.route('/')
def index():
    heap_patterns = """"""
    for pattern in PATTERNS:
        heap_patterns += f'<a href="/run/{pattern}">{pattern}</a><br>'
    return flask.render_template('index.html',patterns=heap_patterns)

@app.route('/run/<pattern_name>')
def run_pattern(pattern_name):
    global pattern
    if pattern_name in PATTERNS:
        pattern = [PATTERNS[pattern_name],0]
    return flask.redirect('/')
def mainloop():
    while True:
        #at the top of the loop, we check to see if there has been an update in the git repo
        #first, make note of the files inside our containing folder, and a simplified description (or "hash") of the contents of each file
        #os.walk can be used to get a list of all files in a directory and its subdirectories
        #for consicesness, i will store the before and after as a dictionary
        before = {}
        for root, dirs, files in os.walk("."):
            for file in files:
                with open(os.path.join(root, file), "rb") as f:
                    before[os.path.join(root, file)] = hash(f.read())
        #pull the repo using git
        os.system("git pull")
        #check the files again
        after = {}
        for root, dirs, files in os.walk("."):
            for file in files:
                with open(os.path.join(root, file), "rb") as f:
                    after[os.path.join(root, file)] = hash(f.read())
        #compare the files
        #for speed, and "becuase i can", im gonna turn the hashes into sets and do some python magic to do a quick comparison
        diff = set(after.items()) - set(before.items())
        if diff:
            #if there is a difference, restart the system
            print("reboot")#os.system("sudo reboot")
        pattern[0](*pattern[1:])#this is the bit of code that made me question copilot for a moment
        pattern[1] += speed*direction
        match pattern[0].__name__:
            case "chase":
                pattern[1] %= num_pixels# take the remainder of the division of the current pixel position by num_pixels so we dont go out of bounds of the list
            case "rainbow_cycle":
                pattern[1] %= 256 # take the remainder of the division of the current pixel position by 256 so that we dont mess up the rainbow math
            case "bounce":
                direction *= -1
        time.sleep(0.1)
mainthread = threading.Thread(target=mainloop)
mainthread.start()
app.run('0.0.0.0',port=6060)