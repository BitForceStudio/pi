# covert circular image to rectangle

import sys, getopt
import cv2
import numpy as np
import time, os
from pathlib import Path
import timeit

def buildMap(Ws,Hs,Wd,Hd,hfovd,vfovd,mode,qbmap):
    # Build the fisheye mapping
    # read the map (map should be generated once)
    map_file = Path("map.m")
    map_x = np.zeros((Hd,Wd),np.float32)
    map_y = np.zeros((Hd,Wd),np.float32)

    if not map_file.is_file() or qbmap:
        map_x,map_y = buildCleanMap(Ws,Hs,Wd,Hd,hfovd,vfovd,mode)
    else:
        f = open('map.m','r')
        size=int(f.readline())
        if (size!=Hd*Wd):
            map_x,map_y = buildCleanMap(Ws,Hs,Wd,Hd,hfovd,vfovd,mode)
        else:
            print("Reading map")
            for y in range(0,int(Hd)):
                for x in range(0,int(Wd)):
                    line =f.readline();
                    strnum = line.split(" ")
                    map_x.itemset((y,x),int(strnum[0]))
                    map_y.itemset((y,x),int(strnum[1]))
        f.close()
    return map_x, map_y

def buildCleanMap(Ws,Hs,Wd,Hd,hfovd,vfovd,mode):
    print("Building map...")

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

    ylim = np.cos((vfovd/2-90)/180*np.pi);

    print ("ylim = %f " % (ylim))

    print ("vfov=%f  hfov= %f  vstart=%f  hstart=%f  xmax=%f  xmin=%f  xscale=%f  xoff=%f  zmax=%f  zmin=%f  zscale=%f  zoff=%f "  % (vfov, hfov, vstart, hstart, xmax, xmin, xscale, xoff, zmax, zmin, zscale, zoff))
    
    # Fill in the map, this is slow but
    # we could probably speed it up
    # since we only calc it once, whatever
    f = open('map.m','w')
    f.write(str(Hd*Wd)+'\n')
    # http://paulbourke.net/dome/fish2/

    for y in range(0,int(Hd)):
        for x in range(0,int(Wd)):
            xS=0
            yS=0
            if mode==1:
                phi = vstart+(vfov*((float(x)/float(Ws))))
                theta = hstart+(hfov*((float(y)/float(Hs))))

                xp = ((np.sin(theta)*np.cos(phi))+xoff)/zscale#
                zp = ((np.cos(theta))+zoff)/zscale#

                xS = int(Ws-(xp*Ws))
                yS = int(Hs-(zp*Hs))
            else:

                theta = np.pi*(float(x)/float(Ws)-1)
                phi   = np.pi*(float(y)/float(Hs)-0.5)

                spx=np.cos(phi)*np.sin(theta);
                spy=np.cos(phi)*np.cos(theta);
                spz=np.sin(phi)

                a_theta = np.arctan(spz/(spx+0.00000000001))
                a_phi   = np.arctan(np.sqrt(spx*spx+spz*spz)/(spy+0.00000000001))
                r=Ws*a_phi/vfov
                if spy<0:
                    r=Ws*180/220-abs(r)

                    if spx<0:
                        xS = int(0.5*Ws-r*np.cos(a_theta))
                        yS = int(0.5*Ws-r*np.sin(a_theta))
                    else:
                        xS = int(0.5*Ws+r*np.cos(a_theta))
                        yS = int(0.5*Ws+r*np.sin(a_theta))
                else:
                    if spx<0:
                        xS = int(0.5*Ws-r*np.cos(a_theta))
                        yS = int(0.5*Ws-r*np.sin(a_theta))
                    else:
                        xS = int(0.5*Ws+r*np.cos(a_theta))
                        yS = int(0.5*Ws+r*np.sin(a_theta))

            map_x.itemset((y,x),xS)
            map_y.itemset((y,x),yS)

            line = str(xS)+" "+str(yS)+'\n'
            f.write(line)

    return map_x, map_y


def unwarp(img,xmap,ymap):
    rst=cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    cv2.imwrite('results.png',rst)


def main():
    inputfile = 'tests.jpg'
    start = timeit.default_timer()
    mode = 0
    print('Input file is: ', inputfile)

    img = cv2.imread(inputfile,0)

    height, width = img.shape

    Ws = width
    Hs = height
    Wd = width
    Hd = height
    Wd = Wd*2

    print("image size: %d*%d pixels " % (width,height))

    fov = 220.0

    mapstart = timeit.default_timer()
    mapx,mapy = buildMap(Ws,Hs,Wd,Hd,fov,fov,mode,True)
    mapstop = timeit.default_timer()

    print("MAP DONE cost %d sec" % (mapstop-mapstart))

    # do our dewarping and save/show the results

    unwarp(img,mapx,mapy)

    stop = timeit.default_timer()
    print("Finished cost %d sec" % (stop-start))

if __name__ == "__main__":
   main()
