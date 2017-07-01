# convert circular image to rectangle
# since settled, everything will be fixed for the next time
# after initial, the config file will be generated
# The map will be saved for the next time

import sys, getopt
import cv2
import numpy as np
import time, os
from pathlib import Path
import timeit
import json

_debug=0

def buildVertMap(w,h,fov,qbmap):
    # Build the fisheye mapping
    # read the map (map should be generated once)
    map_file = Path("json/defishvert.json")
    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)

    if not map_file.is_file() or qbmap:
        map_x,map_y = buildVertJsonMap(w,h,fov)
    else:
        with open('json/defishvert.json') as json_data:
            jsonMap = json.load(json_data)
            mapSize = jsonMap["SIZE"]
            if (mapSize!=h*w*2):
                map_x,map_y = buildVertJsonMap(w,h,fov)
            else:
                map_x,map_y = readVertJsonMap(w,h,jsonMap)

    return map_x, map_y
    
def readVertJsonMap(w,h,jsonMap):
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

def buildVertJsonMap(w,h,fov):
    if _debug>=1:
        print("Building map...")

    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)
    vfov=fov/180*np.pi

    imgObj = {"SIZE":2*w*h}
    imgMapX = []
    imgMapY = []

    hfpi = 0.5 * np.pi
    
    for y in range(0,int(h)):
        phi    = np.pi*(float(y)/float(h))
        sinPhi = np.sin(phi)

        for x in range(0,int(w*2)):

            theta = np.pi*(float(x)/float(w)-1)
            r=w*phi/vfov

            if sinPhi<0:
                r=w*180/fov-abs(r)

            xS = int(0.5*w+r*np.cos(theta))
            yS = int(0.5*w+r*np.sin(theta))

            map_x.itemset((y,x),xS)
            map_y.itemset((y,x),yS)

            imgMapX.append(xS)
            imgMapY.append(yS)
    
    imgObj["MX"]=imgMapX
    imgObj["MY"]=imgMapY

    with open('json/defishvert.json', 'w') as outfile:
        json.dump(imgObj, outfile)

    return map_x, map_y
    


def unwarp(img,xmap,ymap,name):
    rst=cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    if _debug>=2:
        cv2.imwrite(name,rst)
    return rst


def crop(img,left,top,w,h):
    crop_img = img[top:top+h, left:left+w] 
    return crop_img

def main():

    w   = 394
    h   = 394
    ml  = 35
    mt  = 6
    fov = 199

    # crop image into square contain the usable sphere. 
    mapx,mapy = buildVertMap(w,h,fov,False)
    print("Finished reading map...")
    # do our dewarping and save/show the results
    img_file="cam.jpg"
    while(1):
        #img_file = 'img/vert_test.jpg'
        img = cv2.imread(img_file,cv2.IMREAD_COLOR)
        img = crop(img,ml,mt,w,w)
        img = unwarp(img,mapx,mapy,'img/pano_tvert.png')
        cv2.imwrite("img/tvertpano.png",img)
        time.sleep(0.5)

if __name__ == "__main__":
   main()
