import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(3, 1280)  # width property is set at value 3
cap.set(4, 720)   # height property is set at value 4

detector = HandDetector(detectionCon=1)  # by default it is 0.5 and on invoking it with a floating point value it gives error, so had to settle with value 1

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText = " "

def draw(img, btnList):
    img_copy = np.array(img)  # Convert the tuple back to a NumPy array
    for button in btnList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img_copy, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img_copy, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    return img_copy



class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

btnList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        btnList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB format
    img = detector.findHands(imgRGB)
    lmList, _ = detector.findHands(imgRGB)  # Use the RGB image for hand detection
    img = draw(img, btnList)

    if lmList:
        for button in btnList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l, _, _ = detector.findDistance(8, 12, img, draw=False)

                if l < 30:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    time.sleep(0.15)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
