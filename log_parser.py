import thread_variable_utility as tvu
from configs import logfile
logs = tvu.read(logfile)
import code

code.InteractiveConsole(locals=globals()).interact()