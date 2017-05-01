# covert circular image to rectangle

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


def unwarp(img,xmap,ymap):
    rst=cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    cv2.imwrite('result.png',rst)


def main():
    inputfile = 'test1.jpg'
    start = timeit.default_timer()

    print('Input file is: ', inputfile)

    img = cv2.imread(inputfile,0)

    height, width = img.shape

    w = width
    h = height

    print("image size: %d*%d pixels " % (width,height))

    fov = 220.0

    mapstart = timeit.default_timer()
    mapx,mapy = buildMap(w,h,fov,False)
    mapstop = timeit.default_timer()

    print("MAP DONE cost %d sec" % (mapstop-mapstart))

    # do our dewarping and save/show the results

    unwarp(img,mapx,mapy)

    stop = timeit.default_timer()
    print("Finished cost %d sec" % (stop-start))

if __name__ == "__main__":
   main()
