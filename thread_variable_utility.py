from patterns import *
def read(file):
        with open(file, 'r') as f:
            try:
                return eval(f.read())
            except:
                 print(f.read())
                 return ["bounce", 0, 3, 3, 1, 1, 255, 0, 0]
def write(file, data):
    with open(file, 'w') as f:
        f.write(str(data))