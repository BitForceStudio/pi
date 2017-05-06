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

def buildMap1(w,h,fov,qbmap):
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
            print("Reading map")
            counter = 0
            for y in range(0,int(h)):
                for x in range(0,int(w*2)):
                    line =f.readline();
                    strnum = line.split(" ")
                    map_x.itemset((y,x),int(strnum[0]))
                    map_y.itemset((y,x),int(strnum[1]))
                    counter=counter+1
        f.close()
    return map_x, map_y

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
    
def readMap(f,h,w):
    print("Reading map...")
    map_x = np.zeros((h,w*2),np.float32)
    map_y = np.zeros((h,w*2),np.float32)

    for y in range(0,int(h)):
        for x in range(0,int(w*2)):
            line =f.readline();
            strnum = line.split(" ")
            map_x.itemset((y,x),int(strnum[0]))
            map_y.itemset((y,x),int(strnum[1]))

    return map_x, map_y

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
                r=w*180/fov-abs(r)

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

def smoothBound(img1, img2, dir):
    w,h = img1.shape[:2]
    rst = img1
    for i in range(0,h):
        for j in range(0,w):
            weight = 0.5*(np.cos(float(i)/float(h)*np.pi)+1)
            if dir==1:
                weight = 1- weight
            rst[j,i] = weight*img1[j,i]+(1.0-weight)*img2[j,i]

    return rst
def main():
    front_file = 'fr_ori.jpg'
    back_file  = 'bk_ori.jpg'
    # crop the images from the original image


    start = timeit.default_timer()

    print('Front file is: ', front_file)
    print('Back file is: ' , back_file)

    fr_img = cv2.imread(front_file,cv2.IMREAD_COLOR)
    bk_img = cv2.imread(back_file ,cv2.IMREAD_COLOR)

    w=1970
    h=1970
    fr_img = crop(fr_img,237,74,w,w)
    bk_img = crop(bk_img,352,29,w,w)

    cv2.imwrite("fr_crop.png",fr_img)
    cv2.imwrite("bk_crop.png",bk_img)

    print("cropped image size: %d*%d pixels " % (w,h))

    fov = 199

    mapstart = timeit.default_timer()
    mapx,mapy = buildMap(w,h,fov,False)
    mapstop = timeit.default_timer()

    print("MAP DONE cost %d sec" % (mapstop-mapstart))

    # do our dewarping and save/show the results

    fr_timg = unwarp(fr_img,mapx,mapy,'fr_pano.png')
    bk_timg = unwarp(bk_img,mapx,mapy,'bc_pano.png')

    delta = 75 
    fr_ttimg = crop(fr_timg,int(w/2)+delta,0,w-2*delta,h)
    bk_ttimg = crop(bk_timg,int(w/2)+delta,0,w-2*delta,h)

    fr_mid = crop(fr_timg,int(w/2)+w-delta,0,2*delta,h)
    bk_mid = crop(bk_timg,int(w/2)-delta  ,0,2*delta,h)

    fr_far = crop(fr_timg,int(w/2)-delta,0,2*delta,h)
    bk_far = crop(bk_timg,int(w/2)+w-delta,0,2*delta,h)

    pano_mid = smoothBound(fr_mid,bk_mid,0)
    pano_far = smoothBound(fr_far,bk_far,1)

    fr_far = crop(pano_far,delta,0,delta,h)
    bk_far = crop(pano_far,0,0,delta,h)

    cv2.imwrite("fr_180.png",fr_ttimg)
    cv2.imwrite("bk_180.png",bk_ttimg)

    vis = np.concatenate((fr_far, fr_ttimg, pano_mid, bk_ttimg, bk_far), axis=1)

    cv2.imwrite("pano.png",vis)
    
    stop = timeit.default_timer()
    print("Finished cost %d sec" % (stop-start))
if __name__ == "__main__":
   main()
