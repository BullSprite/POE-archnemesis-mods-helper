from PIL import ImageGrab
import numpy as np
import win32gui
from time import sleep
import cv2
import math
import os


def cutImage(img):
    images = []
    for h in [2, 57, 111, 166, 221, 275, 330, 385]:
        for w in [2, 57, 111, 166, 221, 275, 330, 385]:
            images.append(img[h:h+55, w:w+55])
    return images

def collect_pictures():
    mods = []
    for img in os.listdir('picturedb'):
        mod = cv2.cvtColor(cv2.imread(f'picturedb\{img}'), cv2.COLOR_BGR2GRAY)
        mods.append([img[:-4], mod])
    return mods    

def capture():
    inv = []
    hwnd = win32gui.FindWindow(None, "Path of Exile")  
    win32gui.SetForegroundWindow(hwnd)
    sleep(0.5)
    img = ImageGrab.grab(bbox=(114, 324, 554, 764))
    img = np.array(img)

    mods = collect_pictures()
    imgs = cutImage(img)

    for img in imgs:
        test = cv2.cvtColor(img[:38, :52], cv2.COLOR_RGB2GRAY)
        maxres = 0
        for mod in mods:
            # res = cv2.matchTemplate(mod[1], test, cv2.TM_CCOEFF_NORMED)
            # res,_,_,_ = cv2.minMaxLoc(res)

            hist1 = cv2.calcHist([test], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([mod[1]], [0], None, [256], [0, 256])
            histres = cv2.compareHist(hist2, hist1, method = cv2.HISTCMP_CORREL)

            res = histres

            if res > maxres:
                maxres = res
                ans = [mod[0], img]
        inv.append(ans if maxres > 0.97 else ["", img])
    return inv
