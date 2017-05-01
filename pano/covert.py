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
    map_file = Path("map.m")
    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)

    if not map_file.is_file() or qbmap:
        map_x,map_y = buildCleanMap(w,h,fov)
    else:
        f = open('map.m','r')
        size=int(f.readline())
        if (size!=h*w*2):
            map_x,map_y = buildCleanMap(w,h,fov)
        else:
            print("Reading map")
            for y in range(0,int(h)):
                for x in range(0,int(w*2)):
                    line =f.readline();
                    strnum = line.split(" ")
                    map_x.itemset((y,x),int(strnum[0]))
                    map_y.itemset((y,x),int(strnum[1]))
        f.close()
    return map_x, map_y

def buildCleanMap(w,h,fov):
    print("Building map...")

    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)
    vfov=fov/180*np.pi

    f = open('map.m','w')
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
    # crop the images from the original image


    start = timeit.default_timer()

    print('Front file is: ', front_file)
    print('Back file is: ' , back_file)

    fr_img = cv2.imread(front_file,0)
    bk_img = cv2.imread(back_file ,0)

    w=1970
    h=1970
    fr_img = crop(fr_img,237,74,w,w)
    bk_img = crop(bk_img,352,29,w,w)

    print("cropped image size: %d*%d pixels " % (w,h))

    fov = 220.0

    mapstart = timeit.default_timer()
    mapx,mapy = buildMap(w,h,fov,False)
    mapstop = timeit.default_timer()

    print("MAP DONE cost %d sec" % (mapstop-mapstart))

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
