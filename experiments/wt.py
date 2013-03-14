import xpybutil.ewmh as ewmh
import time

count = 0
while True:
    # XCB allows async communication with the X server. return values are cookies 
    cookie = ewmh.get_active_window()
    # blocking wait for X server reply
    window = cookie.reply() 
    #print window
    count += 1
    if count % 100 == 0 :
        print window, count
    time.sleep(0.01)
