window-title
============

Automated time tracking using window titles
-------------------------------------------

The objective is to track the title of the focused window and then apply rules to deduce which project is being worked on for how long.

Both sampling (polling) and event-driven approaches are possible. 

This project was inspired by Joachim Breitner's ARBTT, which uses the polling approach:
https://www.joachim-breitner.de/blog/archives/336-The-Automatic-Rule-Based-Time-Tracker.html

ARBTT's sampling frequency is rather low, and it saves a lot more window information than I need. My inital experiments with a simple polling script using external commands like xprop fell short. 

This project adopts the event-driven approach. There are two common libraries for talking to the X server: Xlib and XCB. Both have Python wrappers. 

This project uses the xcb one: `sudo apt-get install python-xcb`

Andrew Gallant's excellent xpybutil provides a high-level API on top of python-xcb for examining EWMH hints and handling X messages. 

In this post, Andrew Gallant provides most of the necessary detail:
https://bbs.archlinux.org/viewtopic.php?pid=919624#p919624

As long as the window manager supports EWMH hints, we can listen for PropertyNotify events on the root window indicating that the `_NET_ACTIVE_WINDOW` property has been modified. This does not detect window name changes (e.g. changing tabs in a web browser or editor) so we need to listen for additional events on the active window.

Epydoc-generated docs are here:
http://burntsushi.net/xpybutil/docs/

It does not appear to be available as a prebuilt package, you can grab the latest source from Github:
```
git clone https://github.com/BurntSushi/xpybutil
cd xpybutil
sudo python setup.py install
```
