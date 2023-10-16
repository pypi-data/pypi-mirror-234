# pyautoflow

This library can control your keyboard and mouse to automate everyday tasks. It can take screenshots and screen recordings for you to check back in on later. 

## Examples
```python
# Import the two base modules
from pyautoflow import controls, inputs


# CONTROLS
# Press the "a" key
controls.press("a")

# Press and hold the "a" key for 5 seconds
controls.press_and_hold("a", 5)

# Type the string "Hello, world!"
controls.type("Hello, world!")

# Set the cursor location to 10, 11
controls.set_cursor(10, 11)

# Set the cursor location to the current location plus 10, 11
controls.set_cursor_rel(10, 11)

# Moves the cursor location to 10, 11 over 5 seconds
controls.move_cursor(10, 11, 5)

# Moves the cursor location to the current location plus 10, 11 over 5 seconds
controls.move_cursor_rel(10, 11, 5)

# Clicks at the current location
controls.click()

# Right clicks at the current location
controls.right_click()

# Presses and holds the left mouse button until released
controls.press_mouse(0)

# Presses and holds the right mouse button until released
controls.press_mouse(1)

# Releases the left mouse button
controls.release_mouse(0)

# Releases the left mouse button
controls.release_mouse(1)

# Drags the cursor from 10, 11 to 100, 101 over 1 second
controls.drag(10, 11, 100, 101, 1)

# Resets timer
reset_timer()

# Gets the time since the last timer reset
delta = get_timer()


# INPUTS
# Takes a screenshot
screen = screenshot()

# Takes a screenshot of the area 10, 11, 100, 101
screen = screenshot_area(10, 11, 100, 101)

# Saves the given image as "foo.png"
save_img(screen, "foobar.png")

# Starts recording the screen as "bar.mp4"
start_recording("bar.mp4")

# Stops the screen recording
stop_recording()
```

## TODO:
- Text recognition
- System information
- Microphone and camera input