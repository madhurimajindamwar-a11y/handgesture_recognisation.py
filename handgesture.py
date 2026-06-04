import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mediapipe as mp
import pyttsx3
import urllib.request
import os

engine = pyttsx3.init()
engine.setProperty("rate", 150)
prev_gesture = ""

model_path = "hand_landmarker.task"
if not os.path.exists(model_path):
    print("odel is Downloading...")
    urllib.request.urlretrieve("https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task", model_path)
    print("Download complete!")

def fingers_up(landmarks):
    tips  = [4, 8, 12, 16, 20]
    bases = [2, 5,  9, 13, 17]
    fingers = []
    if landmarks[tips[0]].x < landmarks[bases[0]].x:
        fingers.append(1)
    else:
        fingers.append(0)
    for i in range(1, 5):
        if landmarks[tips[i]].y < landmarks[bases[i]].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def get_gesture(fingers):
    if   fingers == [0,0,0,0,0]: return "Be strong...!!"
    elif fingers == [1,1,1,1,1]: return "Hii..Madhurima Here.!!"
    elif fingers == [0,1,0,0,0]: return "Always work hard"
    elif fingers == [0,1,1,0,0]: return "HI.. Everyonee...!!"
    elif fingers == [1,0,0,0,0]: return "All the best"
    elif fingers == [1,0,0,0,1]: return "Have fun!!"
    elif fingers == [0,1,0,0,1]: return "Swagg...!!"
    else:                        return "Bye"

display_text = {
    "Be strong...!!":                      "Be strong...!!",
    "Hii..Madhuuuu.!!": "Hii..Madhuuuuuu...!!",
    "Hii..Madhurima Here.!!": "Hii..Madhurima Here...!!",
    "Always work hard":             "Always work hard!",
    "HI.. Everyonee...!!":          "HI.. Everyonee...!!",
    "All the best":                 "All The Best!",
    "Have fun!!":                    "Have fun!!",
    "Swagg...!!":                   "Swagg...!!",
    "Bye":                          "BYEeee...!!"
}

def draw_landmarks(frame, landmarks, w, h):
    connections = [
        (0,1),(1,2),(2,3),(3,4),
        (0,5),(5,6),(6,7),(7,8),
        (0,9),(9,10),(10,11),(11,12),
        (0,13),(13,14),(14,15),(15,16),
        (0,17),(17,18),(18,19),(19,20),
        (5,9),(9,13),(13,17)
    ]
    points = []
    for lm in landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        points.append((cx, cy))
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
    for a, b in connections:
        cv2.line(frame, points[a], points[b], (255, 255, 255), 2)

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
print("Camera is Running ! Show your Hand.To close camera press Q.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)
    gesture_text = "No hand detected"
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            draw_landmarks(frame, hand_landmarks, w, h)
            fingers = fingers_up(hand_landmarks)
            gesture_text = get_gesture(fingers)
            #if gesture_text != prev_gesture and gesture_text != "Bye":
             #   engine.say(gesture_text)
              #  engine.runAndWait()
               # prev_gesture = gesture_text
            if gesture_text != prev_gesture:
                engine.say(gesture_text)
                engine.runAndWait()
                prev_gesture = gesture_text
                if gesture_text == "No hand detected":
                    prev_gesture = ""
    cv2.putText(frame, display_text.get(gesture_text, gesture_text),
        (30, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5, (0, 255, 0), 3)
    cv2.imshow("Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()