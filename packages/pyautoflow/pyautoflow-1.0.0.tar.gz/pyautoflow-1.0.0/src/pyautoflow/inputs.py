import keyboard
import mouse
import numpy as np
import cv2
import pyautogui
import threading

recording_thread = None
recording_stopping = False

def recording_thread_func(filename):
    screen_width, screen_height = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (screen_width, screen_height))
    while True:
        out.write(cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2RGB))
        if recording_stopping:
            out.release()
            break

def screenshot():
    img = pyautogui.screenshot()
    return(img)

def screenshot_area(x1, y1, x2, y2):
    img = pyautogui.screenshot(region=(x1,y1,x2,y2))
    return(img)

def save_img(img, filename):
    if (filename[-4:] != ".png") and (filename[-4:] != ".jpg"):
        raise ValueError("Must be a .png or .jpg file extension.")
    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, image)

def start_recording(filename):
    if filename[-4:] != ".mp4":
        raise ValueError("Must be a .mp4 file extension.")
    global recording_thread
    global recording_stopping
    recording_stopping = False
    recording_thread = threading.Thread(target = recording_thread_func, args = (filename,))
    recording_thread.start()    

def stop_recording():
    global recording_stopping
    recording_stopping = True
