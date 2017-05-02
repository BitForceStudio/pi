# stitch images
import sys, getopt
import cv2
import numpy as np
import time, os
from pathlib import Path
import timeit

def extraFeature(image, surfThreshold=2000):
	surf = cv2.xfeatures2d.SIFT_create()
	kp,des=surf.detectAndCompute(image,None)
	print("keypoints: "+ str(len(kp)))
	return kp,des

def findCord(img1, img2, kp1,des1,kp2,des2):

	# FLANN parameters
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)   # or pass empty dictionary

	flann = cv2.FlannBasedMatcher(index_params,search_params)

	matches = flann.knnMatch(des1,des2,k=2)

	# Need to draw only good matches, so create a mask
	matchesMask = [[0,0] for i in range(len(matches))]

	# ratio test as per Lowe's paper
	for i,(m,n) in enumerate(matches):
	    if m.distance < 0.7*n.distance:
	        matchesMask[i]=[1,0]

	draw_params = dict(matchColor = (0,255,0),
	                   singlePointColor = (255,0,0),
	                   matchesMask = matchesMask,
	                   flags = 0)

	img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

	cv2.imwrite("correspondences.jpg", img3)

	print("match points:",len(matches))
	if len(matches) > 4:
		# construct the two sets of points
		pts1 = np.float32([kp1[i] for (_, i) in matches])
		pts2 = np.float32([kp2[i] for (i, _) in matches])
		return pts1,pts2

	return None

def draw_correspondences(image1, image2, points1, points2):
	'Connects corresponding features in the two images using yellow lines.'

	## Put images side-by-side into 'image'.
	(h1, w1) = image1.shape[:2]
	(h2, w2) = image2.shape[:2]
	image = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
	image[:h1, :w1] = image1
	image[:h2, w1:w1+w2] = image2

	## Draw yellow lines connecting corresponding features.
	for (x1, y1), (x2, y2) in zip(np.int32(points1), np.int32(points2)):
		cv2.line(image, (x1, y1), (x2+w1, y2), (0, 255, 255), lineType=cv2.CV_AA)

	return image

def match_flann(desc1, desc2, r_threshold = 0.06):
	## Adapted from <http://stackoverflow.com/a/8311498/72470>.

	## Build a kd-tree from the second feature vector.
	FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
	flann = cv2.flann_Index(desc2, {'algorithm': FLANN_INDEX_KDTREE, 'trees': 4})

	## For each feature in desc1, find the two closest ones in desc2.
	(idx2, dist) = flann.knnSearch(desc1, 2, params={}) # bug: need empty {}

	## Create a mask that indicates if the first-found item is sufficiently
	## closer than the second-found, to check if the match is robust.
	mask = dist[:,0] / dist[:,1] < r_threshold

	## Only return robust feature pairs.
	idx1  = np.arange(len(desc1))
	pairs = np.int32(zip(idx1, idx2[:,0]))
	return pairs[mask]


def main():
	right_file = 'bk_180.png'
	left_file  = 'fr_180.png'

	r_img = cv2.imread(right_file,0)
	l_img = cv2.imread(left_file ,0)



	## Detect features and compute descriptors.
	keypoints1, descriptors1 = extraFeature(r_img)
	keypoints2, descriptors2 = extraFeature(l_img)
	print(len(keypoints1), "features detected in r_img")
	print(len(keypoints2), "features detected in l_img")

	## Find corresponding features.
	points1, points2 = findCord(l_img, r_img, keypoints1, descriptors1, keypoints2, descriptors2)
	print(len(points1), "features matched")

	## Visualise corresponding features.
	correspondences = draw_correspondences(r_img, l_img, points1, points2)
	cv2.imwrite("correspondences.jpg", correspondences)
	cv2.imshow('correspondences', correspondences)
    
if __name__ == "__main__":
	main()