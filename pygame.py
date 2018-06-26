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



def process_img(original_img,lane_x2):
	# original_img is BGR
	lane_v = np.array([[0,200],[1,120],[140,100],[260,100],[400,120],[400,200]])

	p_img= cv2.cvtColor(original_img, cv2.COLOR_RGB2HSV)
	
	#                    H  S  V
	lane_lo = np.array([110,15,81])
	lane_hi = np.array([120,25,98])
	# HSV range is H:0-180 S:0-255 V:0-255 in opencv

	lane = cv2.inRange(p_img, lane_lo, lane_hi)
	lane = roi(lane,[lane_v])
	

	M_lane = cv2.moments(lane)
	# ar = np.count_nonzero(lane == 255)
	ar = int(M_lane['m00'] / 255)
	print "ar=",ar # area * (weight) = M_lane['m00']

	if M_lane['m00'] != 0 :
		lane_x = int(M_lane['m10']/M_lane['m00'])
		lane_y = int(M_lane['m01']/M_lane['m00'])

		print "x,y=", lane_x,lane_y
	
		if lane_x2 != 0 :
			dlane = lane_x - lane_x2
			print "dl=",dlane
		else:
			dlane = 0
		if lane_x>220 and dlane>0:
			n=2
		elif lane_x<180 and dlane<0:
			n=-2
		elif dlane>0:
			n=1
		elif dlane<0:
			n=-1
		else:
			n=0

		return n, lane_x
	else:
		return 10, lane_x2


def straight(): #p=0
	keyboard.release_key('v')
	keyboard.press_key('w')
	keyboard.release_key('a')
	keyboard.release_key('d')
	print "s"

def left(): #p=-2
	keyboard.press_key('a')
	keyboard.press_key('w')
	keyboard.release_key('d')
	print "l"

def right(): #p=2
	keyboard.press_key('d')
	keyboard.press_key('w')
	keyboard.release_key('a')
	print "r"


def sleft(): #p=-1
	keyboard.press_key('a')
	keyboard.press_key('w')
	keyboard.release_key('d')
	keyboard.release_key('a')
	print "sl"

def sright(): #p=1
	keyboard.press_key('d')
	keyboard.press_key('w')
	keyboard.release_key('a')
	keyboard.release_key('d')
	print "sr"


def hleft(): #p=-3
	keyboard.press_key('w')
	keyboard.release_key('d')
	keyboard.press_key('v')
	keyboard.press_key('a')
	keyboard.release_key('v')
	print "hl"
	
def hright(): #p=3
	keyboard.press_key('w')
	keyboard.release_key('a')
	keyboard.press_key('v')
	keyboard.press_key('d')
	keyboard.release_key('v')
	print "hr"
def pause(): #p=10
	keyboard.release_key('a')
	keyboard.release_key('w')
	keyboard.release_key('d')
	keyboard.release_key('v')
	i=0
	while(i<5):
		print (5-i)
		time.sleep(1)
		i=i+1

lane_x = 200
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
		p, lane_x = process_img(img ,lane_x)
		print('{} seconds'.format(time.time()-last_time))
		img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		# cv2.imshow('mask',mask)
		# cv2.imshow('mas',mas)
		last_time = time.time()

		if p == 0:
			straight()
		elif p== 2:
			right()
		elif p== -2:
			left()
		elif p== -1:
			sleft()
		elif p== 1:
			sright()
		elif p== 3:
			hright()
		elif p== -3:
			hleft()
		else:
			pause()
		# b = cv2.waitKey(5)
		# if b == 113: # value of q 
		# 	keyboard.release_key('w')
		# 	keyboard.release_key('a')
		# 	keyboard.release_key('d')
		# 	cv2.destroyAllWindows()
		# 	break
		# elif b == 112:  # value of p
		# 	print "pausing"
		# 	pause()