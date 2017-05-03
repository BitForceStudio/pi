# covert circular image to rectangle
# image info: 1990*1990 center need to be set manuely
# since settled, everything will be fixed for the next time
# after initial, the config file will be generated, in formation of 
# crop location
# matrix size
# pairs of x and y 

import sys, getopt
import cv2
import numpy as np
import time, os
from pathlib import Path
import timeit

def buildMap(w,h,fov,qbmap):
    # Build the fisheye mapping
    # read the map (map should be generated once)
    map_file = Path("defish.mat")
    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)

    if not map_file.is_file() or qbmap:
        map_x,map_y = buildCleanMap(w,h,fov)
    else:
        f = open('defish.mat','r')
        size=int(f.readline())
        if (size!=h*w*2):
            map_x,map_y = buildCleanMap(w,h,fov)
        else:
            map_x,map_y = readMap(f,h,w)
        f.close()
    return map_x, map_y
	
def readMap(file,h,w):
	print("Reading map...")
	map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)
	# read the whole file for speeding up
	lines =file.readlines(h*w*2)
	for y in range(0,int(h)):
		for x in range(0,int(w*2)):
			line = lines[y*h+x]
			strnum = line.split(" ")
			map_x.itemset((y,x),int(strnum[0]))
			map_y.itemset((y,x),int(strnum[1]))
	return map_x, map_y
	
def readConfig():
	# get master & slave image config infomation
	# includes: 
	#     1 crop: left, top, size
	#     2 fov(field of view)
	# initially, these values are set by default, it need to be modified by user. 
	masterLeft = 240
	masterTop  = 10
	slaveLeft  = 240
	slaveTop   = 10
	imgSize    = 1970
	imgFov     = 200  # 1970 pixels, 5MP--> 200 degree, which was from the experience
	
	config_path = Path("fisheyelens.conf")
	if not config_path.is_file():
		print("No config file, the default setting will be applied:")
	else:
		print("Read config from file:")
		f = open('fisheyelens.conf','r')
		masterLeft = int(f.readline())
		masterTop  = int(f.readline())
		slaveLeft  = int(f.readline())
		slaveTop   = int(f.readline())
		imgSize    = int(f.readline())
		imgFov     = int(f.readline())
		
	print("** Master image left:",masterLeft)
	print("** Master image top :",masterTop)
	print("** Slave  image left:",slaveLeft)
	print("** Slave  image top :",slaveTop)
	print("** Image size       :",imgSize)
	print("** Field of view    :",imgFov)
		
	return masterLeft,masterTop,slaveLeft,slaveTop,imgSize,imgFov
		
	
	
def buildCleanMap(w,h,fov):
    print("Building map...")

    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)
    vfov=fov/180*np.pi

    f = open('defish.mat','w')
    f.write(str(h*w*2)+'\n')
    # http://paulbourke.net/dome/fish2/

    for y in range(0,int(h)):
        for x in range(0,int(w*2)):

            theta = np.pi*(float(x)/float(w)-1)
            phi   = np.pi*(float(y)/float(h)-0.5)

            spx=np.cos(phi)*np.sin(theta);
            spy=np.cos(phi)*np.cos(theta);
            spz=np.sin(phi)

            a_theta = np.arctan(spz/(spx+0.00000000001))
            a_phi   = np.arctan(np.sqrt(spx*spx+spz*spz)/(spy+0.00000000001))
            r=w*a_phi/vfov
            if spy<0:
                r=w*180/220-abs(r)

            if spx<0:
                xS = int(0.5*w-r*np.cos(a_theta))
                yS = int(0.5*w-r*np.sin(a_theta))
            else:
                xS = int(0.5*w+r*np.cos(a_theta))
                yS = int(0.5*w+r*np.sin(a_theta))

            map_x.itemset((y,x),xS)
            map_y.itemset((y,x),yS)

            line = str(xS)+" "+str(yS)+'\n'
            f.write(line)

    return map_x, map_y


def unwarp(img,xmap,ymap,name):
    rst=cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    cv2.imwrite(name,rst)
    return rst


def crop(img,left,top,w,h):
    crop_img = img[top:top+h, left:left+w] 
    # Crop from x, y, w, h
    # NOTE: its img[y: y + h, x: x + w]
    #cv2.waitKey(0)
    return crop_img

def main():
    front_file = 'fr_ori.jpg'
    back_file  = 'bk_ori.jpg'
    start = timeit.default_timer()

    print('Master image is: ', front_file)
    print('Slave image is: ' , back_file)

    fr_img = cv2.imread(front_file,0)
    bk_img = cv2.imread(back_file ,0)
	
	masterLeft,masterTop,slaveLeft,slaveTop,imgSize,imgFov=readConfig()

	# crop the images from the original image
    #w=1970
    #h=1970
    #fr_img = crop(fr_img,237,74,w,w)
    #bk_img = crop(bk_img,352,29,w,w)

	w=imgSize
    h=imgSize
    fr_img = crop(fr_img,masterLeft,masterTop,w,w)
    bk_img = crop(bk_img,slaveLeft,slaveTop,w,w)
	
    print("cropped image size: %d*%d pixels " % (w,h))

    #fov = 220.0 
	fov = imgFov

    mapstart = timeit.default_timer()
    mapx,mapy = buildMap(w,h,fov,False)
    mapstop = timeit.default_timer()

    print("Loading map cost %d sec" % (mapstop-mapstart))

    # do our dewarping and save/show the results

    fr_timg = unwarp(fr_img,mapx,mapy,'fr_pano.png')
    bk_timg = unwarp(bk_img,mapx,mapy,'bc_pano.png')

    stop = timeit.default_timer()
    print("Finished cost %d sec" % (stop-start))

    fr_timg = crop(fr_timg,766,0,2408,1970)
    bk_timg = crop(bk_timg,766,0,2408,1970)

    cv2.imwrite("fr_180.png",fr_timg)
    cv2.imwrite("bk_180.png",bk_timg)

if __name__ == "__main__":
   main()
