import cv2
import os

capture = cv2.VideoCapture(0)
image_file = ""
directory = "Data\Pause-Play"
counter = 1
os.chdir(directory) 

while capture.isOpened():
    ret, image = capture.read()
     
    image = cv2.flip(image, 1)
    cv2.imshow('Webcam', image)

    if cv2.waitKey(1) & 0xFF == ord('1'):
        image_file = str(counter) + ".jpg"
        cv2.imwrite(image_file, image)
        counter += 1 
        if counter > 100:
            break
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

capture.release()
cv2.destroyAllWindows()