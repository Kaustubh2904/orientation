import tkinter as tk
import tkinter.font as tkFont
import subprocess
import cv2

class App:
    def __init__(self, root):
        #setting title
        root.title("Virtual Computer System")
        #setting window size
        width=671
        height=479
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.configure(bg="lightblue")
        root.resizable(width=False, height=False)

        GLabel_987=tk.Label(root)
        GLabel_987["activebackground"] = "#f80c0c"
        GLabel_987["activeforeground"] = "#132aff"
        ft = tkFont.Font(family='Times',size=22)
        GLabel_987["font"] = ft
        GLabel_987["fg"] = "#000000"
        GLabel_987["justify"] = "center"
        GLabel_987["text"] = "VIRTUAL COMPUTER SYSTEM"
        GLabel_987.place(x=100,y=20,width=437,height=114)

        GButton_752=tk.Button(root)
        GButton_752["bg"] = "#150de8"
        GButton_752["disabledforeground"] = "#6ffc10"
        ft = tkFont.Font(family='Times',size=16)
        GButton_752["font"] = ft
        GButton_752["fg"] = "#ffffff"
        GButton_752["justify"] = "center"
        GButton_752["text"] = "VIRTUAL KEYBOARD"
        GButton_752.place(x=200,y=140,width=255,height=151)
        GButton_752["command"] = self.GButton_752_command

        GButton_577=tk.Button(root)
        GButton_577["bg"] = "#000000"
        ft = tkFont.Font(family='Times',size=16)
        GButton_577["font"] = ft
        GButton_577["fg"] = "#ffffff"
        GButton_577["justify"] = "center"
        GButton_577["text"] = "VIRTUAL VOLUME CONTROL"
        GButton_577.place(x=180,y=310,width=288,height=134)
        GButton_577["command"] = self.GButton_577_command

    def GButton_752_click():
          import cv2
import time
import numpy as np
import hand_module as htm
import math
import pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

####################################
wCam, hcam = 640, 480
#####################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hcam)
pTime = 0
cTime = 0
detector = htm.handDetector(detectioncon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPos(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = ((x1 + x2) // 2), ((y1 + y2) // 2)

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        # Interpolate color from green to red based on volPer
        color = (0, int(255 - (volPer * 2.55)), int(volPer * 2.55))

        # Draw the volume bar with the interpolated color
        cv2.rectangle(img, (50, 150), (85, 400), color, 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), color, cv2.FILLED)

    cv2.putText(img, f'{int(volPer)} % ', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("IMG", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


def GButton_577_click():
        import cv2
import numpy as np
import time
import hand_module_mouse as ht
import autopy   # Install using "pip install autopy"

### Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 8         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)

detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max
screen_width, screen_height = autopy.screen.size()      # Getting the screen size
while True:
    success, img = cap.read()
    img = detector.findHands(img)                       # Finding the hand
    lmlist, bbox = detector.findPosition(img)           # Getting position of hand

    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]


        fingers = detector.fingersUp()      # Checking if fingers are upwards
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)   # Creating boundary box
        if fingers[1] == 1 and fingers[2] == 0:     # If fore finger is up and middle finger is down
            x3 = np.interp(x1, (frameR,width-frameR), (0,screen_width))
            y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

            curr_x = prev_x + (x3 - prev_x)/smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            autopy.mouse.move(screen_width - curr_x, curr_y)    # Moving the cursor
            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        if fingers[1] == 1 and fingers[2] == 1:     # If fore finger & middle finger both are up
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:     # If both fingers are really close to each other
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()    # Perform Click

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        break

        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

