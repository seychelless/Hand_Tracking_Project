import cv2
import time
import module as htm

pTime = 0
cTime = 0
vid = cv2.VideoCapture(0)
detector = htm.HandDetector()
while True:
    success, img = vid.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[20])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)