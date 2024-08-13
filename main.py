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
# import all the patterns from the patterns.py file "*" means any objects, like variables and functions
from patterns import *
from support import *
app = flask.Flask(__name__)

pixels.fill((0, 0, 0))
pixels.show()
pattern_file = "../pattern.py"


if not os.path.exists(pattern_file):
    tvu.write(pattern_file, ["bounce", 0, 0, 0, 1, 1,*COLOR])


@app.route('/')
def index():
    heap_patterns = """"""
    for pattern in PATTERNS:
        heap_patterns += f'<option value="{pattern}">{pattern}</option><br>'
    return flask.render_template("index.html", patterns=heap_patterns,pattern=tvu.read(pattern_file)[0])


@app.route('/run', methods=["POST"])
def run_pattern():
    pattern_name = flask.request.form["pattern"]
    color = flask.request.form["color"]
    color = color[1:]
    color = [int(color[i:i+2], 16) for i in (0, 2, 4)]
    print(color)
    if pattern_name in PATTERNS:
        tvu.write(pattern_file, [pattern_name, 0, 0, 0, 1, 1, *color])
    return flask.redirect('/')


@app.route('/speed/<int:speed_>')
def set_speed(speed_):
    pattern = tvu.read(pattern_file)
    pattern[4] = speed_
    tvu.write(pattern_file, pattern)
    return flask.redirect('/')


@app.route('/pull')
def pull():
    os.system("git pull")
    return flask.redirect('/')


def loop():
    while True:
        pattern = tvu.read(pattern_file)
        pattern[0] = PATTERNS[pattern[0]]
        # this is the bit of code that made me question copilot for a moment
        pattern[0](*pattern[1:4], *pattern[5:])
        pattern[1] += pattern[4] * \
            pattern[5] if not pattern[0].__name__ in ["off", "blank"] else 0
        match pattern[0].__name__:
            case "chase":
                # take the remainder of the division of the current pixel position by num_pixels so we dont go out of bounds of the list
                pattern[1] %= num_pixels
            case "rainbow_cycle":
                # take the remainder of the division of the current pixel position by 256 so that we dont mess up the rainbow math
                pattern[1] %= 256
            case "bounce":
                if pattern[1] > num_pixels-1 or pattern[1] < 0:
                    pattern[5] *= -1

        pattern[0] = pattern[0].__name__
        tvu.write(pattern_file, pattern)
        time.sleep(0.1)


mainthread = threading.Thread(target=loop)
mainthread.start()
app.run('0.0.0.0', port=6060, debug=True)
