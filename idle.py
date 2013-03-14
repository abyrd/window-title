# requires xscreensaver package
# ubuntu: sudo apt-get install libxss-dev
# http://thp.io/2007/09/x11-idle-time-and-focused-window-in.html
# http://coderrr.wordpress.com/2008/04/20/getting-idle-time-in-unix/

# XCB C version:
# http://stackoverflow.com/questions/9049087/with-x11-how-can-i-get-the-users-time-away-from-keyboard-while-ignoring-cert

import ctypes
import os
from xpybutil import conn, root

xlib = ctypes.cdll.LoadLibrary('libX11.so')
dpy = xlib.XOpenDisplay(os.environ['DISPLAY'])
root = xlib.XDefaultRootWindow(dpy)
xss = ctypes.cdll.LoadLibrary('libXss.so')
        
class XScreenSaverInfo(ctypes.Structure) :
  """ typedef struct { ... } XScreenSaverInfo; """
  _fields_ = [('window',      ctypes.c_ulong), # screen saver window
              ('state',       ctypes.c_int),   # off,on,disabled
              ('kind',        ctypes.c_int),   # blanked,internal,external
              ('since',       ctypes.c_ulong), # milliseconds
              ('idle',        ctypes.c_ulong), # milliseconds
              ('event_mask',  ctypes.c_ulong)] # events

class IdleInfo :
    def __init__ (self) :
        xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
        self.xss_info = xss.XScreenSaverAllocInfo()
    def idle_msec (self) :
        xss.XScreenSaverQueryInfo(dpy, root, self.xss_info)
        return self.xss_info.contents.idle
    def main (self) :
        ii = IdleInfo()
        while True :
            idle_time = ii.idle_msec()
            if idle_time % 1000 == 0 and idle_time > 0 :
                print "Idle time in milliseconds:", idle_time
        
