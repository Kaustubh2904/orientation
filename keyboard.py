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