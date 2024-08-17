import thread_variable_utility as tvu
from configs import logfile
import code
import re
r=re.compile(r"(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))")
logs = tvu.read(logfile)
def parse(url):
    if o:=re.search(r,url):
        o=o.group()
        path = url.split(o)[1][3]
        return True
    return False

def clear_non_exploits(logs):
    for ip in logs['ips']:
        print(ip)
        for log in logs['ips'][ip]['logs']:
            print(log)
            if not parse(log['url']):
                print('removing',log)
                logs['ips'].remove(ip)
                break
    return logs

code.InteractiveConsole(locals=globals()).interact()