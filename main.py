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
import threading
import thread_variable_utility as tvu
from patterns import * #import all the patterns from the patterns.py file "*" means any objects, like variables and functions
app = flask.Flask(__name__)

pixels.fill((0, 0, 0))
pixels.show()


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
    tvu.write("pattern.py",pattern)
    return flask.redirect('/')

@app.route('/pull')
def pull():
    os.system("git pull")
    return flask.redirect('/')
def loop():
    while True:
        pattern = tvu.read("pattern.py")
        pattern[0] = PATTERNS[pattern[0]]
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