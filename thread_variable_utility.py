def read(file, default=""):
        with open(file, 'r') as f:
            readin = f.read()
            f.close()
            try:
                return eval(readin)
            except:
                #print(readin+" Read "+str(default))
                return default
                if input():
                   with open(file, 'r') as f:
                       readin = f.read()
                       f.close()
                   if input(readin+" Read\n"):
                        return eval(readin)
                return ["bounce", 0, 3, 3, 1, 1, 255, 255, 255]
def write(file, data):
    with open(file, 'w') as f:
        f.write(str(data))
        f.close()