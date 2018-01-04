window-title
============

## Automated time tracking using window titles

The objective is to track the title of the focused window and then apply rules to deduce which project is being worked on for how long.

## Implementation notes

For this kind of task, both sampling (polling) and event-driven approaches are possible. 

This project was inspired by Joachim Breitner's [ARBTT](https://www.joachim-breitner.de/blog/archives/336-The-Automatic-Rule-Based-Time-Tracker.html), which uses the polling approach.

ARBTT's default sampling frequency is rather low (but can be configured to be higher), and it saves a lot more window information than I need. My inital experiments with a simple polling script using external commands like [xprop](http://www.xfree86.org/4.0/xprop.1.html) fell short. 

This project adopts the event-driven approach. There are two common libraries for talking to the X server: [Xlib](https://en.wikipedia.org/wiki/Xlib) and [XCB](https://en.wikipedia.org/wiki/XCB). Both have Python wrappers. This project uses the `XCB` one, **[python-xpyb](http://xcb.freedesktop.org/XcbPythonBinding/)**.

Andrew Gallant's excellent **[xpybutil](https://github.com/BurntSushi/xpybutil)** provides a high-level API on top of `python-xpyb` for examining [EWMH hints](https://en.wikipedia.org/wiki/Extended_Window_Manager_Hints) and handling X messages. In [this post](https://bbs.archlinux.org/viewtopic.php?pid=919624#p919624), Andrew provides most of the necessary detail.

As long as the window manager supports EWMH hints, we can listen for [PropertyNotify events](http://tronche.com/gui/x/xlib/events/client-communication/property.html) on the [root window](https://en.wikipedia.org/wiki/Root_window) indicating that the [`_NET_ACTIVE_WINDOW`](http://standards.freedesktop.org/wm-spec/wm-spec-latest.html#idm140200472702304) property has been modified. This does not detect window name changes (e.g. changing tabs in a web browser or editor) so we need to listen for additional events on the active window.

## Installation

First, install the dependencies:

- XCB Python Binding (**`xpyb`**):
  ```bash
  sudo apt-get install python-xpyb
  ```

- Andrew Gallant's Python port of `xcb-util` (**`xpybutil`**):
  ```bash
  git clone https://github.com/BurntSushi/xpybutil
  cd xpybutil
  sudo python setup.py install
  ```

- Development headers for the X11 Screen Saver extension library (**`libxss-dev`**)
  ```bash
  sudo apt-get install libxss-dev
  ```

Then download and run window-title:

```bash
git clone https://github.com/abyrd/window-title
cd window-title
python window-title.py
```
