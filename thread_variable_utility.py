from main import bounce, chase, rainbow_cycle, off, blank
def read(file):
    with open(file, 'r') as f:
        return eval(f.read())
def write(file, data):
    with open(file, 'w') as f:
        f.write(str(data))