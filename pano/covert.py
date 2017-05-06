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

_debug=1

def buildMap(w,h,fov,qbmap):
    # Build the fisheye mapping
    # read the map (map should be generated once)
    map_file = Path("defish.json")
    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)

    if not map_file.is_file() or qbmap:
        map_x,map_y = buildJsonMap(w,h,fov)
    else:
        with open('defish.json') as json_data:
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

    with open('defish.json', 'w') as outfile:
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

def smoothBound(img1, img2, w, h, delta):
    img1pi = img1[0:h, int(0.5*w):int(1.5*w)] 
    img2pi = img2[0:h, int(0.5*w):int(1.5*w)] 
    rst = np.concatenate((img1pi, img2pi), axis=1)
    # image matrix: height * width
    for j in range(w-delta,w+delta):
        weight = 1-0.5*(np.sin(float(j-w)/float(delta)*np.pi/2.0)+1)
        for i in range(0,h):
            #  img1 X img2
            rst[i,j] = weight*img1[i,j+int(0.5*w)]+(1.0-weight)*img2[i,j-int(0.5*w)]
            #  img2 X img1
            t = j-w
            if j<w:
                t=j+w
            rst[i,t] = (1.0-weight)*img1[i,j-int(0.5*w)]+weight*img2[i,j+int(0.5*w)]

    return rst

def main():
    master_file = 'fr_ori.jpg'
    slave_file  = 'bk_ori.jpg'

    start = timeit.default_timer()

    if _debug>=1:
        print('Front file is: ', master_file)
        print('Back file is: ' , slave_file)

    master_img = cv2.imread(master_file,cv2.IMREAD_COLOR)
    slave_img = cv2.imread(slave_file ,cv2.IMREAD_COLOR)

    w=1970
    h=1970
    ml = 237
    mt = 74
    sl = 352
    st = 29
    fov = 199
    delta = 75 
    
    with open('fisheyelens.conf') as json_data:
        if _debug>=1:
            print("Reading config from file...")
        jsonConf = json.load(json_data)
        w    =jsonConf["SIZE"]
        h    =jsonConf["SIZE"]
        ml   =jsonConf["MLEFT"]
        mt   =jsonConf["MTOP"]
        sl   =jsonConf["SLEFT"]
        st   =jsonConf["STOP"]
        fov  =jsonConf["FOV"]
        delta=jsonConf["DELTA"]

    master_img = crop(master_img,ml,mt,w,w)
    slave_img = crop(slave_img,sl,st,w,w)

    if _debug>=2:
        cv2.imwrite("fr_crop.png",master_img)
        cv2.imwrite("bk_crop.png",slave_img)

    if _debug>=1:
        print("cropped image size: %d*%d pixels " % (w,h))

    mapstart = timeit.default_timer()
    mapx,mapy = buildMap(w,h,fov,False)
    mapstop = timeit.default_timer()

    if _debug>=1:
        print("MAP DONE cost %d sec" % (mapstop-mapstart))

    # do our dewarping and save/show the results

    oImagestart = timeit.default_timer()
    master_img = unwarp(master_img,mapx,mapy,'pano_master.png')
    slave_img = unwarp(slave_img,mapx,mapy,'pano_slave.png')

    vis = smoothBound(master_img,slave_img,w,h,delta)

    cv2.imwrite("pano.png",vis)
    oImagestop = timeit.default_timer()
    stop = timeit.default_timer()

    if _debug>=1:
        print("Output Image DONE cost %d sec" % (oImagestop-oImagestart))

    if _debug>=1:
        print("Finished cost %d sec" % (stop-start))

if __name__ == "__main__":
   main()
