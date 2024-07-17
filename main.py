import os
import threading
import time
# Disable OneDNN optimizations for TensorFlow
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from teachable_machine import TeachableMachine
import cv2
from pynput.keyboard import Controller, Key
import tkinter as tk
from PIL import ImageTk, Image


def press_multimedia_key(key):
    keyboard.press(key)
    keyboard.release(key)


""" WORK ON CONTINOUSLY DECREASING VOLUME, MAKE MODEL BETTER, BE ABLE TO RUN THE PROGRAM AGAIN WHEN AFTER HITTING STOP, QUALITY OF LIFE CHANGES"""
def chooser(result):
    global previous_result
    print("Result received in chooser:", result)

    if result == "pause/play":
        if previous_result != result:
            press_multimedia_key(Key.media_play_pause)
            previous_result = result
            text2.config(text="PAUSE/PLAY")  
    else:
        if result == "volumeup":
            press_multimedia_key(Key.media_volume_up)
            previous_result = result
            text2.config(text="VOLUME DOING UP")
            time.sleep(0.8)
        elif result == "volumedown":
            press_multimedia_key(Key.media_volume_down)
            previous_result = result
            text2.config(text="VOLUME GOING DOWN")
            time.sleep(0.8)
        elif result == "mute/unmute":
            press_multimedia_key(Key.media_volume_mute)
            previous_result = result
            text2.config(text="MUTE/UNMUTE")
            time.sleep(1)
        elif result == "next":
            press_multimedia_key(Key.media_next)
            previous_result = result
            text2.config(text="NEXT TRACK")
            time.sleep(1)
        elif result == "previous":
            press_multimedia_key(Key.media_previous)
            previous_result = result
            text2.config(text="PREVIOUS TRACK")
            time.sleep(1)
        elif result == "idle":
            previous_result = result
            text2.config(text="IDLE")

def run():
    global run_flag, gesture_thread, cap
    if run_flag == False:
        run_flag = True
        text.config(text="Running")
        cap = cv2.VideoCapture(0)  # Re-initialize the camera
        gesture_thread = threading.Thread(target=runGestureControls)
        gesture_thread.start()

def stop():
    global run_flag, gesture_thread, image_path
    if run_flag == True:
        run_flag = False
        text.config(text="Press start to activate gesture controls")
        if gesture_thread is not None:
            gesture_thread.join()
        cap.release()
        cv2.destroyAllWindows()
        os.remove(image_path)


def runGestureControls():
    global cap, run_flag, ret, panel, image_path
    while run_flag:

        # Capture frame-by-frame
        ret, img = cap.read()

        if not ret or img is None or img.size == 0:
            print("Failed to capture image")
            continue
    
        # Save the image temporarily
        cv2.imwrite(image_path, img)
        # Classify the captured image
        result = model.classify_image(image_path)
        if result["class_confidence"] >= 0.98:
            prediction = result["class_name"].strip().lower()
            chooser(prediction)
        """        else:
            prediction = "idle"
            chooser(prediction)"""
        # Display the frame
        #cv2.imshow("Video Stream", img)

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

previous_result = "idle"
model_path = "keras_model.h5"
labels_file_path = "labels.txt"
image_path = "screenshot.jpg"

cap = cv2.VideoCapture(0)
model = TeachableMachine(model_path=model_path, labels_file_path=labels_file_path)
keyboard = Controller()

run_flag = False
gesture_thread = None

root = tk.Tk()
root.title('Spotify Gesture Control')

text = tk.Label(root, text='Press start to activate gesture controls')
text.pack()

runbutton = tk.Button(root, text='Run', width=25, command=run)
runbutton.pack()

stopbutton = tk.Button(root, text='Stop', width=25, command=stop)
stopbutton.pack()

text2 = tk.Label(root, text='____')
text2.pack()



root.mainloop()

cap.release()
cv2.destroyAllWindows()
os.remove(image_path)
