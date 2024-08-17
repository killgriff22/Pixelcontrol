import thread_variable_utility as tvu
from configs import logfile
import code
import re
import copy
r=re.compile(r"(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))")
logs = tvu.read(logfile)
def parse(url):
    if o:=re.search(r,url):
        return True
    return False

def clear_non_exploits(logs):
    cp = copy.deepcopy(logs)
    for ip in cp['ips']:
        print(ip)
        if not any([parse(log['url']) for log in cp['ips'][ip]['logs']]):
            print('removing',ip)
            del logs['ips'][ip]
    return logs

code.InteractiveConsole(locals=globals()).interact()