from patterns import *
def read(file):
        with open(file, 'r') as f:
            readin = f.read()
            f.close()
            try:
                return eval(readin)
            except:
                 print(readin)
                 return ["bounce", 0, 3, 3, 1, 1, 255, 0, 0]
def write(file, data):
    with open(file, 'w') as f:
        f.write(str(data))
        f.close()