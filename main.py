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
import re
log_regex = re.compile(r"(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))")
app = flask.Flask(__name__)

pixels.fill((0, 0, 0))
pixels.show()
pattern_file = "../pattern.py"
logfile = "../log.txt"

if not os.path.exists(pattern_file):
    tvu.write(pattern_file, ["bounce", 0, 0, 0, 1, 1,*COLOR])

@app.before_request
def before_request():
    log={
        'ip':flask.request.remote_addr,
        'time':time.time(),
        'url':flask.request.full_path,
    }
    if not os.path.exists(logfile):
        tvu.write(logfile,{'logs':[log],'ips':[flask.request.remote_addr]})
    else:
        logs = tvu.read(logfile)
        logs['logs'].append(log)
        if not flask.request.remote_addr in logs['ips']:
            logs['ips'].append(flask.request.remote_addr)
        tvu.write(logfile,logs)
    if o:=re.search(log_regex,flask.request.full_path):
        o=o.group()
        print(path := flask.request.full_path.split(o))
        print(f"{o}/{path}")
        #os.system(f"curl {o}/{path}")

@app.route('/')
def index():
    heap_patterns = """"""
    file = tvu.read(pattern_file)
    color = file[6:]
    color = f"{''.join([hex(i)[2:].zfill(2) for i in color])}"
    ft = file[2]
    rt = file[3]
    for pattern in PATTERNS:
        heap_patterns += f'<option value="{pattern}">{pattern}</option><br>'
    return flask.render_template("index.html", patterns=heap_patterns,pattern=file[0],color=color,num_pixels=num_pixels,ft=ft,rt=rt)


@app.route('/run', methods=["POST"])
def run_pattern():
    pattern_name = flask.request.form["pattern"]
    color = flask.request.form["color"]
    color = color[1:]
    color = [int(color[i:i+2], 16) for i in (0, 2, 4)]
    front_tail = int(flask.request.form['front_tail'])
    rear_tail = int(flask.request.form['rear_tail'])
    print(color)
    print(len([pattern_name, 0, 0, 0, 1, 1, *color]))
    if pattern_name in PATTERNS:
        tvu.write(pattern_file, [pattern_name, 0, front_tail, rear_tail, 1, 1, *color])
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
        #try:
            pixels.fill((0, 0, 0))
            pattern = tvu.read(pattern_file)
            pattern[0] = PATTERNS[pattern[0]]
            pattern[0](*pattern[1:4], *pattern[6:])
            pixels.show()
            pattern[1] += pattern[4] * \
                pattern[5] if not pattern[0].__name__ in ["off", "blank"] else 0
            match pattern[0].__name__:
                case "chase":
                    # take the remainder of the division of the current pixel position by num_pixels so we dont go out of bounds of the list
                    pattern[1] %= num_pixels
                case "rainbow":
                    # take the remainder of the division of the current pixel position by 256 so that we dont mess up the rainbow math
                    pattern[1] %= 256
                case "stars":
                    pattern[1] %= num_pixels
                case "rainbow_stars":
                    pattern[1] %= 256
                case "bounce":
                    if pattern[1] > num_pixels-1 or pattern[1] < 0:
                        pattern[5] *= -1
                case "off" | "full" | "blank":
                    pattern[1]=0


            pattern[0] = pattern[0].__name__
            tvu.write(pattern_file, pattern)
            time.sleep(0.1)
        #except Exception as e:
        #    print(e)


mainthread = threading.Thread(target=loop)
mainthread.start()
app.run('0.0.0.0', port=80, debug=True)
