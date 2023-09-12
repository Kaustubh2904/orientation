import tkinter as tk
from tkinter import *

# mouse to be executed when Button 1 is clicked
def button1_click():
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
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# keyboard to be executed when Button 2 is clicked
def button2_click():
    import cv2
    from cvzone.HandTrackingModule import HandDetector
    import time


    cap = cv2.VideoCapture(0)


    cap.set(3,1280) #width property is set at value 3
    cap.set(4,720) #height property is set at value 4

    detector = HandDetector(detectionCon=1) #by default it is 0.5 and on invokingit with a floating point value it goves error so had to settle with value 1



    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

    finalText = " "

    def draw(img, btnList):
        for button in btnList:
            x,y = button.pos
            w,h = button.size
            cv2.rectangle(img, button.pos, (x+w, y+h), (255,0,255), cv2.FILLED)
            cv2.putText(img, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)

        return img

    class Button():
        def __init__(self, pos, text, size=[85,85]):
            self.pos = pos
            self.size = size
            self.text = text

    btnList = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            btnList.append(Button([100 * j + 50, 100 * i + 50], key))


    while True:
        success, img = cap.read()
        #flip the frame by 180 degrees
        img = cv2.flip(img, 1)
        
    
        img = detector.findHands(img)
        lmList, bboxInfo = detector.findPosition(img)
        img = draw(img, btnList)

        if lmList:
            for button in btnList:
                x,y = button.pos
                w,h = button.size

                if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                    cv2.rectangle(img, button.pos, (x+w, y+h), (175,0,175), cv2.FILLED)
                    cv2.putText(img, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)

                    l,_,_ = detector.findDistance(8,12,img, draw=False) #we dont need to pass the points itself rather the indices. Here 8 represents the tip of the index finger and 12 represents the tip of the middle finger. Also the l variable is assigned the value of the length of the distance and the rest two parameters are to be ignored and hence has been replaced with an underscore.

                    #print(l)

                    # when clicked the letter is added to buttonText variable
                    if l<30:
                        cv2.rectangle(img, button.pos, (x+w, y+h), (0,255,0), cv2.FILLED)
                        cv2.putText(img, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
                        finalText += button.text
                        time.sleep(0.15)

        cv2.rectangle(img, (50,350), (700,450), (175,0,175), cv2.FILLED)
        cv2.putText(img, finalText , (60,430), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255), 5)
        if cv2.waitKey(1) == ord("  q"):  # Press 'e' key to exit the loop
            break

        cv2.imshow("Image",img)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()



# volume control to be executed when Button 3 is clicked
def button3_click():
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

            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])
            #print(int(length), vol)
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







# Create the main window
root = tk.Tk()
root.title("Virtual Computer System")
root.geometry("640x550")  # Set window dimensions

# Customize the main window background color
root.configure(bg="cyan")

# Create a custom font
custom_font = ("comic_sans", 16, "italic")


image = tk.PhotoImage(file="megalogowithstroke.png")
image_label = tk.Label(root, image=image, bg="cyan")
image_label.pack()

button1_style = tk.Button(root, text="Virtual mouse ", command=button1_click, font=custom_font, bg="blue", fg="white")
button1_style.pack(pady=20)  # Add vertical padding to center the button

# Create Button 2 with different colors and font and center it
button2_style = tk.Button(root, text="Virtual Keyboard", command=button2_click, font=custom_font, bg="blue", fg="white")
button2_style.pack(pady=20)

# Create Button 3 with another set of colors and font and center it
button3_style = tk.Button(root, text="Virtual volume control", command=button3_click, font=custom_font, bg="blue", fg="white")
button3_style.pack(pady=20)


# Start the GUI main loop
root.mainloop()
