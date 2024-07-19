import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

model_path = os.path.abspath("Gesture_Control.task")
recognizer = vision.GestureRecognizer.create_from_model_path(model_path)

capture = cv2.VideoCapture(0)

while capture.isOpened():
    ret, image = capture.read()
     
    #image = cv2.flip(image, 1)
    cv2.imshow('image.jpg', image)
    cv2.imwrite('image.jpg', image)

    # Load the input image.
    result = mp.Image.create_from_file('image.jpg')

    # Run gesture recognition.
    recognition_result = recognizer.recognize(result)

    # Check if there are any gestures recognized.
    if recognition_result.gestures:
        # Get the first gesture (which is a list of categories).
        top_gesture = recognition_result.gestures[0]

        # Check if there are categories in the first gesture.
        if top_gesture:
            # Extract the category names and scores.
            category_name = [category.category_name for category in top_gesture][0]
            score = [category.score for category in top_gesture][0]
            
            if score >= 0.90:
                # Display the category names and scores.
                print("Category Names:", category_name)
                print("Scores:", score)
        else:
            print("No categories found in the first gesture.")
    else:
        print("No gestures recognized.")


    # Display the most likely gesture.
    #top_gesture = recognition_result.gestures[-1]
    #gesture = [category.category_name for category in top_gesture]
    #score = [category.score for category in top_gesture]

    #for gesture in recognition_result.gestures:
        #print([category.category_name for category in gesture])
        #print([category.score for category in gesture])
    #print(top_gesture)
    #print(f"Gesture recognized: {gesture} ({score})")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()