import keyboard
import mouse
import time

timer_start_time = time.time()

def press(key):
    keyboard.press_and_release(key)

def press_and_hold(key, duration):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

def type(text):
    keyboard.send(text)

def type_custom(text, delay):
    for q in text:
        press(q)
        time.sleep(delay)

def set_cursor(x, y):
    mouse.move(x, y)

def set_cursor_rel(x, y):
    mouse.move(x, y, False)

def move_cursor(x, y, time):
    mouse.move(x, y, duration=time)

def move_cursor_rel(x, y, time):
    mouse.move(x, y, False, duration=time)

def click():
    mouse.click()

def right_click():
    mouse.right_click()

def click_custom(count, delay, button=0):
    if button == 0: # Left button
        for q in range(count):
            click()
            time.sleep(delay)       
    if button == 1: # Right button
        for q in range(count):
            right_click()
            time.sleep(delay)

def press_mouse(button=0):
    if button == 0: # Left button
        mouse.press('left')
    if button == 1: # Right button
        mouse.press('right')

def release_mouse(button=0):
    if button == 0: # Left button
        mouse.release('left')
    if button == 1: # Right button
        mouse.release('right')

def drag(x1, y1, x2, y2, duration):
    set_cursor(x1, y1)
    press_mouse()
    move_cursor(x2, y2, duration)
    release_cursor()

def reset_timer():
    global timer_start_time
    timer_start_time = time.time()

def get_timer():
    global timer_start_time
    timer = time.time() - timer_start_time
    return timer

def clear_timer():
    global timer_start_time
    timer_start_time = 0
