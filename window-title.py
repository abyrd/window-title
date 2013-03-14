#!/usr/bin/python
import signal, sys

import xcb
import xpybutil.event as event
import xpybutil.ewmh as ewmh
import xpybutil.util as util
import xpybutil.window as window
from xpybutil import conn, root

def sigint_handler(signal, frame):
    print 'received SIGINT, terminating'
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

active_window = None

def name_change_handler() :
    active_name = ewmh.get_wm_name(active_window).reply()
    print active_window, active_name

def active_window_handler() :
    global active_window
    # de-register all events (including 'PropertyChange' for name change notifications)
    # de-registering will fail if there is no active window:  
    # upon startup, or when the active window changed because a window was closed
    try :
        window.listen(active_window, )
    except :
        print 'failed to de-register events for active window'
    active_window = ewmh.get_active_window().reply()
    # register to listen for name changes on the active window
    try :
        window.listen(active_window, 'PropertyChange')
        # when the active window changes the title changes
        name_change_handler()
    except :
        print 'failed to register events for active window'

window.listen(root, 'PropertyChange')
while True:
    e = conn.wait_for_event() # SIGINT will be caught upon blocking call return
    if not isinstance(e, xcb.xproto.PropertyNotifyEvent):
        # print 'unexpected message type', e
        continue
    aname = util.get_atom_name(e.atom)
    if aname == '_NET_ACTIVE_WINDOW':
        active_window_handler()
    if aname == 'WM_NAME':
        name_change_handler()
    # else :
    #    print 'ignoring', aname
    
