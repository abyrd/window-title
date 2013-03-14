#!/usr/bin/python
import Xlib.display
import Xlib.X

def handle_event(event) :
    print event

display = Xlib.display.Display()
root = display.screen().root
focused = display.get_input_focus().focus

print focused
wmname = focused.get_wm_name()
wmclass = focused.get_wm_class()
if wmclass is None and wmname is None:
    focused = focused.query_tree().parent
    wmname = focused.get_wm_name()
    print "WM Name: %s" % ( wmname, )

# Tell the X server we want to catch KeyRelease events.
root.change_attributes(Xlib.X.PropertyChangeMask)

while True :
    event = root.display.next_event()
    print event	

