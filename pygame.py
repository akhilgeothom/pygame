import cv2
import numpy as np
import time
import mss
from PIL import Image
from pykeyboard import PyKeyboard
keyboard = PyKeyboard()



def roi(img,vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked



def process_img(original_img,p,a):
    # original_img is BGR
    vertices = np.array([[0,200],[1,120],[140,100],[260,100],[400,120],[400,200]])
    
    p_img = original_img
    p_img= cv2.cvtColor(original_img, cv2.COLOR_RGB2HSV)

    # lo_rgb = np.array([75,76,83])
    # up_rgb = np.array([85,86,93])

    lo_hsv = np.array([110,15,81])
    up_hsv = np.array([120,25,98])
    mask = cv2.inRange(p_img, lo_hsv, up_hsv)
    
    mask = roi(mask,[vertices])
    M = cv2.moments(mask)
    n=0
    ar = np.count_nonzero(mask == 255)
    print "ar=",ar
    if M['m00'] != 0 and ar > 0:
        if ar<20000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print cx,cy

            
            if cx > 220 and p!=-1:
                n = 1
            elif cx < 180 and p!=1:
                n = -1;
            else:
                n = 0
        else:
            n = 0
    else:
        print "pausing1"
        keyboard.release_key('w')
        keyboard.release_key('a')
        keyboard.release_key('d')
        time.sleep(5)
        pass
    # print p
    return mask,n,ar



def straight():
    
    keyboard.press_key('w')
    keyboard.release_key('a')
    keyboard.release_key('d')
    print "w"
def left():
    keyboard.press_key('a')
    keyboard.press_key('w')
    keyboard.release_key('d')
    print "a"
def sleft():
    keyboard.tap_key('a')
    keyboard.press_key('w')
    keyboard.release_key('d')
    print "sa"
def right():
    keyboard.press_key('d')
    keyboard.press_key('w')
    keyboard.release_key('a')
    print "d"
def sright():
    keyboard.tap_key('d')
    keyboard.press_key('w')
    keyboard.release_key('a')
    print "sd"
def hleft():
    keyboard.press_key('a')
    keyboard.press_key('v')
    keyboard.press_key('w')
    keyboard.release_key('d')
    keyboard.release_key('v')
    keyboard.release_key('a')
def hright():
    keyboard.press_key('d')
    keyboard.press_key('v')
    keyboard.press_key('w')
    keyboard.release_key('a')
    keyboard.release_key('v')
    keyboard.release_key('d')
i=0
while(i<5):
    print (5-i)
    time.sleep(1)
    i=i+1
p=0
a=10000
last_time=time.time()
while(True):
    with mss.mss() as sct:
        monitor = {'top':80, 'left':5, 'width':800,'height':600}
        sct_img = sct.grab(monitor)
        img = Image.new('RGB', sct_img.size)
        pixels = zip(sct_img.raw[2::4],
                    sct_img.raw[1::4],
                    sct_img.raw[0::4])
        img.putdata(list(pixels))
        # the img is BGR 
        img=np.asarray(img)
        img=cv2.resize(img,(400,300))
        mask,p,a = process_img(img,p,a)
        print('{} seconds'.format(time.time()-last_time))
        # img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow('mask',mask)
        # cv2.imshow('mas',mas)
        last_time = time.time()

        if p == -1:
            left()
        elif p == 1:
            right()
        elif p == 0:
            straight()
        else:
            print "pausing2"
            time.sleep(5)
            keyboard.release_key('w')
            keyboard.release_key('a')
            keyboard.release_key('d')
        b = cv2.waitKey(5)
        if b == 113: # value of q is 113
            keyboard.release_key('w')
            keyboard.release_key('a')
            keyboard.release_key('d')
            cv2.destroyAllWindows()
            break
        elif b == 112:  # value of p is 112
            print "pausing3"
            time.sleep(5)
