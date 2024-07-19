import os
import threading
import time
import psutil 
# Disable OneDNN optimizations for TensorFlow
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import mediapipe as mp
from mediapipe.tasks.python import vision
import cv2
from pynput.keyboard import Controller, Key
import tkinter as tk
import customtkinter as ctk


# Method used to simulate the press of a key on the keyboard
def press_multimedia_key(key):
    keyboard.press(key)
    keyboard.release(key)

# Checks to see if the Spotify app is running, returns true if it is
def is_spotify_running():
    # Iterate over all running processes
    for process in psutil.process_iter(['pid', 'name']):
        try:
            # Check if the process name contains "Spotify"
            if "Spotify" in process.info['name']:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Takes in the result from the model and presses the corresponding media key for that result
def chooser(result):
    global previous_result
    print("Result received in chooser:", result)

    # for a given result, it will press the key, set the previous result, and change the text to display what the result is
    if result == "pause-play":
        # checks to see if the previous result is the same as the current
        if previous_result != result:
            time.sleep(0.5)
            press_multimedia_key(Key.media_play_pause)
            previous_result = result
            text2.configure(text="PAUSE/PLAY")  
    else:
        if result == "volumeup":
            press_multimedia_key(Key.media_volume_up)
            previous_result = result
            text2.configure(text="VOLUME UP")
            time.sleep(0.8)
        elif result == "volumedown":
            press_multimedia_key(Key.media_volume_down)
            previous_result = result
            text2.configure(text="VOLUME DOWN")
            time.sleep(0.8)
        elif result == "mute-unmute":
            press_multimedia_key(Key.media_volume_mute)
            previous_result = result
            text2.configure(text="MUTE/UNMUTE")
            time.sleep(1)
        elif result == "skip":
            press_multimedia_key(Key.media_next)
            previous_result = result
            text2.configure(text="NEXT TRACK")
            time.sleep(1)
        elif result == "previous":
            press_multimedia_key(Key.media_previous)
            previous_result = result
            text2.configure(text="PREVIOUS TRACK")
            time.sleep(1)
        elif result == "idle":
            previous_result = result
            text2.configure(text="IDLE")
        else:
            previous_result = result
            text2.configure(text="IDLE")

# Starts the program loop with the button has hit on the GUI
def run():
    global run_flag, gesture_thread, cap
 
    # checks to see if the program is already running
    if run_flag == False:
        # checks to see if spotify is running
        if is_spotify_running():
            run_flag = True
            text.configure(text="Running")
            if os.path.exists(image_path):
                os.remove(image_path)
            cap = cv2.VideoCapture(0)  # initialize the camera
            gesture_thread = threading.Thread(target=runGestureControls) # creates a thread so that the program loop can run beside the tkinter loop
            gesture_thread.start() # starts the loop
        else:
            text.configure(text="Please open the Spotify desktop app to run")

# Stops the program loop and closes everything
def stop():
    global run_flag, gesture_thread, image_path, root
    #print("1") # used for debugging
    if run_flag:
        run_flag = False
        
        # closes the thread
        if gesture_thread is not None:
            gesture_thread.join(timeout=5)
            if gesture_thread.is_alive():
                print("is alive") # used to check if the thread has been closed
        
        # Release camera and destroy windows
        if cap and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()

        # Remove image file if it exists
        if os.path.exists(image_path):
            os.remove(image_path)

        # Destroy the popup window if it exists
        if popup and popup.winfo_exists():
            popup.destroy()

        # changes the text on the screen if it exists
        if root and root.winfo_exists():
            text.configure(text="Press start to activate gesture controls")
            text2.configure(text="[  Resulting command will be displayed here   ]")
        
# main program loop that takes in feed from the webcam and gets a gesture based on the results
def runGestureControls():
    global cap, run_flag, ret, panel, image_path
    while run_flag:
        time.sleep(0.05)
        
        # captures the webcam frame
        ret, img = cap.read()

        if not ret or img is None or img.size == 0:
            print("Failed to capture image")
            continue
    
        # Save the image temporarily
        cv2.imwrite(image_path, img)

        # converts the image into a format that the model can handle
        result = mp.Image.create_from_file(image_path)

        # classifies the image and returns the results
        recognition_result = recognizer.recognize(result)

        # cehcks to see if there is a gesture that is seen
        if recognition_result.gestures:
            top_gesture = recognition_result.gestures[0]

            # checks to see if there is a gesture at the index of 0
            if top_gesture:

                # gets the confidence of that gesture
                score = [category.score for category in top_gesture][0]
                
                # if the confidence is above the threshold, then get the gesture and run the chooser method
                if score >= 0.80:
                    category_name = [category.category_name for category in top_gesture][0].strip().lower()
                    chooser(category_name)
                else:
                    category_name = "idle"
                    chooser(category_name)
            else:
                category_name = "idle"
                chooser(category_name)
        else:
            category_name = "idle"
            chooser(category_name)

        if os.path.exists(image_path):
            os.remove(image_path)

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

# creates a popup window to give intrustions to the user
def show_popup(event):
    global popup  
    if popup is None or not popup.winfo_exists():
        popup = tk.Toplevel(root)
        popup.overrideredirect(True)  # Remove window decorations
        popup.geometry("+{}+{}".format(event.x_root + 10, event.y_root + 10))  # Position the popup
        
        # Loads and resizes the PNG image
        image = tk.PhotoImage(file="Tutorial.png")
        resized_image = image.subsample(10, 10)  
        image_label = tk.Label(popup, image=resized_image)
        image_label.image = resized_image  
        image_label.pack(padx=10, pady=10)

# closes the popup window
def hide_popup(event):
    global popup
    if popup and popup.winfo_exists():
        popup.destroy()
        popup = None

popup = None # variable used to keep track if the popup window exists

previous_result = "idle" # variable used to track the previous result
image_path = "screenshot.jpg" # the path used to save the image from the webcam

cap = cv2.VideoCapture(0) # initalizes the camera

model_path = os.path.abspath("Gesture_Control.task") # gets the path of the model
recognizer = vision.GestureRecognizer.create_from_model_path(model_path) # loads the model

keyboard = Controller() # initalizes the keyboard class so that it can simulate key presses

run_flag = False # variable used to track if the program is running
gesture_thread = None # variable used to track if the thread is running

root = ctk.CTk() # creates a custom tkinter window

root.title('Spotify Gesture Control') # changes the title of the window

# Adds text and buttons to the window
text = ctk.CTkLabel(root, text='Press start to activate gesture controls')
text.pack(side=tk.LEFT, padx=10, pady=10)

runbutton = ctk.CTkButton(root, text='Run', width=120, command=run)
runbutton.pack(side=tk.LEFT, padx=10, pady=10)

stopbutton = ctk.CTkButton(root, text='Stop', width=120, command=stop)
stopbutton.pack(side=tk.LEFT, padx=10, pady=10)

text2 = ctk.CTkLabel(root, text='[  Resulting command will be displayed here   ]')
text2.pack(side=tk.LEFT, padx=10, pady=10)

popbutton = ctk.CTkButton(root, text="?", width=10)
popbutton.pack(side=tk.RIGHT, padx=20, pady=20)

# Bind mouse events to the button
popbutton.bind("<Enter>", show_popup)  
popbutton.bind("<Leave>", hide_popup) 

# when the user closes the program, allows for clean shutdowns
def on_closing():
    stop()
    root.after(1000, root.destroy)  
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop() # runs the window
