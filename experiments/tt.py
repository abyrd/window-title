from subprocess import *
import re, time
from time import strftime

def isodatetime() :
    return strftime("%Y-%m-%d %H:%M:%S")

def isoparse(s) :
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

# using xprop
def active_window_title_old():
    root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)

    for line in root.stdout:
        m = re.search('^_NET_ACTIVE_WINDOW.* ([\w]+)$', line)
        if m != None:
            id_ = m.group(1)
            id_w = Popen(['xprop', '-id', id_, 'WM_NAME'], stdout=PIPE)
            break

    if id_w != None:
        for line in id_w.stdout:
            match = re.match("WM_NAME\(\w+\) = (?P<name>.+)$", line)
            if match != None:
                return match.group("name")

    return "Active window not found"

# using xprintidle package
def get_idle_time_seconds():
    root = Popen(['xprintidle'], stdout=PIPE)
    idle_msec = int(root.stdout.readline())
    return idle_msec / 1000.0


cumulative = {}
def checkpoint () :
    print "CHECKPOINT"
    for title, seconds in cumulative.iteritems() :
        print title, seconds    
    print " "


import Xlib.display
display = Xlib.display.Display()
# using xlib 
# just judging by how fast it runs in a loop, this is much more efficient than the other options
# tracking a hint rather than polling would be even more efficient
def active_window_title() :
    window = display.get_input_focus().focus
    wmname = window.get_wm_name()
    wmclass = window.get_wm_class()
    if wmclass is None and wmname is None:
        window = window.query_tree().parent
        wmname = window.get_wm_name()
    return wmname

IDLE_SEC = 30 # seconds

last_title = None
last_time = None
while True :
    if get_idle_time_seconds() > IDLE_SEC :
        current_title = '__IDLE__'
    else :
        current_title = active_window_title()
    if current_title != last_title :
        current_time = time.time()
        if last_time != None :
            elapsed = current_time - last_time
            print isodatetime(), '%f %s' % (elapsed, last_title)
            if last_title in cumulative :
                cumulative[last_title] += elapsed
            else :
                cumulative[last_title] = elapsed
        last_time = current_time
    last_title = current_title
    time.sleep(0.5)
    #checkpoint()    

