import cv2
import time
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]



wCam, hCam = 1280, 720

video = cv2.VideoCapture(0)
video.set(3, wCam)
video.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detectionCon=0.7)

while True:
    success, img = video.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[8], lmList[4])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FONT_HERSHEY_SIMPLEX)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FONT_HERSHEY_SIMPLEX)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FONT_HERSHEY_SIMPLEX)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # 40 - 300
        # -65 - 0

        vol = np.interp(length, [40, 300], [minVol, maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 40:
            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FONT_HERSHEY_SIMPLEX)




    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)