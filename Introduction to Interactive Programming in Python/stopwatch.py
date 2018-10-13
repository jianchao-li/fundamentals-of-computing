# template for "Stopwatch: The Game"

import simplegui

# define global variables
tenthOfSeconds = 0
interval = 100
totalStops = 0
successfulStops = 0
isRunning = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    nTenthOfSeconds = t % 10
    t = (t - nTenthOfSeconds) // 10
    nSeconds = t % 60
    t = t - nSeconds
    nMinutes = t // 60
    nTenthOfSeconds = str(nTenthOfSeconds)
    if nSeconds >= 10:
        nSeconds = str(nSeconds)
    else:
        nSeconds = "0" + str(nSeconds)
    nMinutes = str(nMinutes)
    return nMinutes + ":" + nSeconds + "." + nTenthOfSeconds    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def watch_start():
    global isRunning
    timer.start()
    isRunning = True
    
def watch_stop():
    global totalStops, successfulStops, isRunning
    timer.stop()
    if isRunning == True:
        totalStops += 1
        if tenthOfSeconds % 10 == 0:
            successfulStops += 1
    isRunning = False
    
def watch_reset():
    global tenthOfSeconds, isRunning, totalStops, successfulStops
    timer.stop()
    isRunning = False
    tenthOfSeconds = 0
    totalStops = 0
    successfulStops = 0
    
# define event handler for timer with 0.1 sec interval
def watch():
    global tenthOfSeconds
    tenthOfSeconds += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(tenthOfSeconds), [10, 120], 60, "Red")
    canvas.draw_text(str(successfulStops) + "/" + str(totalStops), [150, 30], 30, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 200, 200)
timer = simplegui.create_timer(interval, watch)

# register event handlers
frame.add_button("Start", watch_start, 100)
frame.add_button("Stop", watch_stop, 100)
frame.add_button("Reset", watch_reset, 100)
frame.set_draw_handler(draw)

# start frame
frame.start()
# timer.start()

# Please remember to review the grading rubric
