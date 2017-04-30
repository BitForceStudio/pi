# covert circular image to rectangle

import sys, getopt
import cv2
import numpy as np
import time

def buildMap(Ws,Hs,Wd,Hd,hfovd,vfovd):
    # Build the fisheye mapping
    map_x = np.zeros((Hd,Wd),np.float32)
    map_y = np.zeros((Hd,Wd),np.float32)
    vfov = (vfovd/180.0)*np.pi
    hfov = (hfovd/180.0)*np.pi
    vstart = ((180.0-vfovd)/180.00)*np.pi/2.0
    hstart = ((180.0-hfovd)/180.00)*np.pi/2.0
    count = 0
    # need to scale to changed range from our
    # smaller cirlce traced by the fov
    xmax = np.sin(np.pi/2.0)*np.cos(vstart)
    xmin = np.sin(np.pi/2.0)*np.cos(vstart+vfov)
    xscale = xmax-xmin
    xoff = xscale/2.0
    zmax = np.cos(hstart)
    zmin = np.cos(hfov+hstart)
    zscale = zmax-zmin
    zoff = zscale/2.0

    print ("vfov=%f  hfov= %f  vstart=%f  hstart=%f  xmax=%f  xmin=%f  xscale=%f  xoff=%f  zmax=%f  zmin=%f  zscale=%f  zoff=%f "  % (vfov, hfov, vstart, hstart, xmax, xmin, xscale, xoff, zmax, zmin, zscale, zoff))
    
    # Fill in the map, this is slow but
    # we could probably speed it up
    # since we only calc it once, whatever
    for y in range(0,int(Hd)):
        for x in range(0,int(Wd)):
            count = count + 1
            phi = vstart+(vfov*((float(x)/float(Wd))))
            theta = hstart+(hfov*((float(y)/float(Hd))))
            xp = ((np.sin(theta)*np.cos(phi))+xoff)/zscale#
            zp = ((np.cos(theta))+zoff)/zscale#
            xS = Ws-(xp*Ws)
            yS = Hs-(zp*Hs)
            map_x.itemset((y,x),int(xS))
            map_y.itemset((y,x),int(yS))


    return map_x, map_y

def unwarp(img,xmap,ymap):
    rst=cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    cv2.imwrite('result.png',rst)


def main():
    inputfile = 'test1.jpg'

    print('Input file is: ', inputfile)

    img = cv2.imread(inputfile,0)

    height, width = img.shape

    Ws = width
    Hs = height
    Wd = width*2
    Hd = height
    print("image size: %d*%d pixels " % (width,height))
    print("BUILDING MAP...")
    fov = 220.0
    mapx,mapy = buildMap(Ws,Hs,Wd,Hd,fov,fov)
    print("MAP DONE")

    # do our dewarping and save/show the results

    unwarp(img,mapx,mapy)
 
    time.sleep(10)



if __name__ == "__main__":
   main()
