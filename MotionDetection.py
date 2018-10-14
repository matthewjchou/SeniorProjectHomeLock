import cv2
import time
import numpy as np 
import imutils
#import RPi.GPIO as IO


#IO.setmode(IO.BOARD)
#IO.setup(14, IO.OUT, initial = IO.LOW)

#resizes, converts to gray, gaussian blurs, and saves the image to images
def process(num):
	#path = 'C:\\Users\\Matthew\\Desktop\\Senior Project\\images\\gray' + num + '.jpg'
	
	resizedImg = imutils.resize(camera.read()[1], width = 700)
	gray = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
	blurredGray = cv2.GaussianBlur(gray, (3, 3), 0)
	#cv2.imwrite(path, blurredGray)

	return blurredGray

#turn on the camera
camera = cv2.VideoCapture(0)
counter = 0

print('Preparing the environment...')
temp = camera.read()[1]
time.sleep(1)

print('Obtaining initial frame...')
gray1 = process('1')


while True:
	#img = camera.read()[1]
	gray2 = process('2')

	delta = cv2.absdiff(gray2, gray1)
	#cv2.imwrite('C:\\Users\\Matthew\\Desktop\\Senior Project\\images\\delta.jpg', delta)

	gray1 = gray2

	#applies adaptive thresholding on |gray2 - gray1|
	thresh = cv2.adaptiveThreshold(delta, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 3) 

	#erosion/dilation to reduce noise, store in thresh	
	cv2.erode(thresh, None, iterations = 3)
	cv2.dilate(thresh, None, iterations = 3)
	#cv2.imwrite('C:\\Users\\Matthew\\Desktop\\Senior Project\\images\\thresh.jpg', thresh)

	modImg, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	

	for c in contours:
		if cv2.contourArea(c)<450:
			movement = False	
			continue
		else:
			print (cv2.contourArea(c))
			movement = True		
			break

	statusFile = open('Status.txt', 'r')
	stat = statusFile.read()
	statusFile.close()
	if stat == '0':
		stat = False
	elif stat == '1':
		stat = True

	if movement:
		if stat:
			#IO.output(14, IO.LOW)
			cv2.putText(delta, 'Authorized Movement', (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,100,0), 3	)

		if not stat:
			counter += 1
			cv2.putText(delta, 'Unauthorized Movement', (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,100,0), 3)
			#If unauthorized movement is detected 3x, turn on the buzzer for 2 seconds and reset the counter
			if counter == 3:
				counter = 0
				#IO.output(14, IO.HIGH)

	elif not movement:
		counter += 1
		cv2.putText(delta, 'No Movement', (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,100,0), 3)
		if counter == 3:
			counter = 0
			#IO.output(14, IO.LOW)

	cv2.imshow('Feed', delta)
	cv2.waitKey(1)


