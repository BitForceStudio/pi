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
import json

_debug=2

def buildMap(w,h,fov,qbmap):
    # Build the fisheye mapping
    # read the map (map should be generated once)
    map_file = Path("test.json")
    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)

    if not map_file.is_file() or qbmap:
        map_x,map_y = buildJsonMap(w,h,fov)
    else:
        with open('test.json') as json_data:
            jsonMap = json.load(json_data)
            mapSize = jsonMap["SIZE"]
            if (mapSize!=h*w*2):
                map_x,map_y = buildJsonMap(w,h,fov)
            else:
                map_x,map_y = readJsonMap(w,h,jsonMap)

    return map_x, map_y
    
def readJsonMap(w,h,jsonMap):
    if _debug>=1:
        print("Reading map...")
    mx = jsonMap["MX"]
    my = jsonMap["MY"]
    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)
    counter = 0
    for y in range(0,int(h)):
        for x in range(0,int(w*2)):
            map_x.itemset((y,x),mx[counter])
            map_y.itemset((y,x),my[counter])
            counter=counter+1

    return map_x, map_y

def buildJsonMap(w,h,fov):
    if _debug>=1:
        print("Building map...")

    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)
    vfov=fov/180*np.pi

    imgObj = {"SIZE":2*w*h}
    imgMapX = []
    imgMapY = []
    
    for y in range(0,int(h)):
        phi    = np.pi*(float(y)/float(h)-0.5)
        cosPhi = np.cos(phi)
        spz    = np.sin(phi)

        for x in range(0,int(w*2)):

            theta = np.pi*(float(x)/float(w)-1)
            spx   =cosPhi*np.sin(theta);
            spy   =cosPhi*np.cos(theta);

            a_theta = np.arctan(spz/(spx+0.00000000001))
            a_phi   = np.arctan(np.sqrt(spx*spx+spz*spz)/(spy+0.00000000001))
            r=w*a_phi/vfov

            if spy<0:
                r=w*180/fov-abs(r)

            if spx<0:
                r=-r

            xS = int(0.5*w+r*np.cos(a_theta))
            yS = int(0.5*w+r*np.sin(a_theta))

            map_x.itemset((y,x),xS)
            map_y.itemset((y,x),yS)

            imgMapX.append(xS)
            imgMapY.append(yS)
    
    imgObj["MX"]=imgMapX
    imgObj["MY"]=imgMapY

    with open('test.json', 'w') as outfile:
        json.dump(imgObj, outfile)

    return map_x, map_y
    


def unwarp(img,xmap,ymap,name):
    rst=cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    if _debug>=2:
        cv2.imwrite(name,rst)
    return rst


def crop(img,left,top,w,h):
    crop_img = img[top:top+h, left:left+w] 
    # Crop from x, y, w, h
    # NOTE: its img[y: y + h, x: x + w]
    #cv2.waitKey(0)
    return crop_img


def main():
    master_file = 'test1.jpg'

    start = timeit.default_timer()

    if _debug>=1:
        print('Front file is: ', master_file)

    master_img = cv2.imread(master_file,cv2.IMREAD_COLOR)

    w=1861
    h=1861
    ml = 351
    mt = 83
    fov = 185
    delta = 75 


    master_img = crop(master_img,ml,mt,w,w)

    if _debug>=2:
        cv2.imwrite("convert.png",master_img)

    if _debug>=1:
        print("cropped image size: %d*%d pixels " % (w,h))

    mapstart = timeit.default_timer()
    mapx,mapy = buildMap(w,h,fov,True)
    mapstop = timeit.default_timer()

    if _debug>=1:
        print("MAP DONE cost %d sec" % (mapstop-mapstart))

    # do our dewarping and save/show the results

    oImagestart = timeit.default_timer()
    master_img = unwarp(master_img,mapx,mapy,'convertpano.png')

    oImagestop = timeit.default_timer()
    stop = timeit.default_timer()

    onepi_img = crop(master_img,int(w/2),0,w,w)
    cv2.imwrite("onepi.png",onepi_img)

    if _debug>=1:
        print("Output Image DONE cost %d sec" % (oImagestop-oImagestart))

    if _debug>=1:
        print("Finished cost %d sec" % (stop-start))

if __name__ == "__main__":
   main()
