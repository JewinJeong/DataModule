# USAGE
# python detect_bright_spots.py --image images/lights_01.png

# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
from dnn_gigi import *
from imagemark import *



'''

기본적인 구상
obj detect 한 것을 crop해 와서 던져줘서 받고 -->
light detect 한 후 --->
해당 light spot에서 노란색 빛 감지 후 -->
깜빡이 판단 후 ------>
던져준다

본 파일은 결국, CROP 이미지를 받고, LEFT RIGHT 판단 결과를 쏘는 것이다.

'''

def light(path, x1, y1, x2, y2):

	# construct the argument parse and parse the arguments
	#abe = []
	#ap = argparse.ArgumentParser()
	#ap.add_argument("-i", "--image", required=True,
	#	help="path to the image file")
	#args = vars(ap.parse_args())

	# load the image, convert it to grayscale, and blur it
	if x1<0 : x1 = 0
	if y1<0 : y1 = 0


	while True:
		text = ""
		left_y = 1
		right_y = 1
		print("path :: " + path)

		image = cv2.imread(path)
		height = y2 - y1
		width = x2 - x1

		image = image[y1:y1 + height, x1:x1 + width]

		onebon = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		if not image.all():


			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #흑백화 왜삑??

			blurred = cv2.GaussianBlur(gray, (31, 31), 0) #블러처리 .. 높으면 빡세게 블러질

			# threshold the image to reveal light regions in the
			# blurred image
			thresh = cv2.threshold(blurred, 190, 255, cv2.THRESH_BINARY)[1]
			# 이걸로 광원 판단 범위를 선택할수있다.

			# perform a series of erosions and dilations to remove
			# any small blobs of noise from the thresholded image
			thresh = cv2.erode(thresh, None, iterations=2)
			thresh = cv2.dilate(thresh, None, iterations=4)

			# perform a connected component analysis on the thresholded
			# image, then initialize a mask to store only the "large"
			# components
			labels = measure.label(thresh, neighbors=8, background=0)
			mask = np.zeros(thresh.shape, dtype="uint8")

			# loop over the unique components
			for label in np.unique(labels):
				# if this is the background label, ignore it
				if label == 0:
					continue

				# otherwise, construct the label mask and count the
				# number of pixels
				labelMask = np.zeros(thresh.shape, dtype="uint8")
				labelMask[labels == label] = 255
				numPixels = cv2.countNonZero(labelMask)

				# if the number of pixels in the component is sufficiently
				# large, then add it to our mask of "large blobs"
				if numPixels > 300:
					mask = cv2.add(mask, labelMask)

			# find the contours in the mask, then sort them from left to
			# right

			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			#print("cnts1 : " + cnts)

			print("cnet "+ str(len(cnts)))
			lala = []




			if len(cnts)>0:

				cnts = contours.sort_contours(cnts)[0] #삑, cnts가 너무 허벌이다

			print("GGG")
			for (i, c) in enumerate(cnts):
				#cv2.imshow("img", onebon)
				cv2.imwrite(f"ppap/{height}b.jpg", onebon)
				#print("\n\nloop starts")
				# draw the bright spot on the image
				(x, y, w, h) = cv2.boundingRect(c)
				g = getglcm(path, x, y)
				text = dnngo(g)
				print("text : " + text)


				#((cX, cY), radius) = cv2.minEnclosingCircle(c)
				#print("cx cy " + str(cX) +" " +  str(cY))


			#print("cnts 2 : " + cnts)










			#name = "output.jpg"


			# show the output image
			cv2.imwrite(f"lobsout/{height}b.jpg", image)
			#cv2.imshow("img", image)
			#cv2.imshow("gra", blurred)
			#cv2.imshow("Image", image)
			#cv2.destroyAllWindows()
			cv2.waitKey(0)

			return text