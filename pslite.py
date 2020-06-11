from PIL import Image,ImageDraw
import PIL
import time
from graphics import *
from player import minimax
import cv2
from tkinter import filedialog
import numpy as np
import os
from os import listdir
from os.path import isfile, join

colors = list([[0, 0, 0],[0, 64, 1],[64, 0, 2],[0, 128, 3],[128, 0, 4],[0, 169, 5],[169, 0, 6],[64, 64, 7],[192, 64, 8],[64, 192, 9],[128, 64, 10],[64, 128, 11],[128, 128, 12],[128, 169, 13],[128, 192, 14],[0, 192, 15],[169, 64, 16],[169, 128, 17],[169, 169, 18],[169, 192, 19],[192, 0, 20],[64, 169, 21],[192, 128, 22],[192, 169, 23],[192, 192, 24]])
onlyfiles = [f for f in listdir('./input') if isfile(join('./input', f))]


def getPoly(color,win):
    ptList=[]
    llList=[]
    pointList=[]
    c=1
    while(1):
        pt=win.getMouse()
        ptList.append(pt)
        pointList.append(pt.x)
        pointList.append(pt.y)
        pt.draw(win)
        if c:
            c=0
            continue
        ll=Line(pt,ptList[-2])
        ll.setOutline('red')
        llList.append(ll)
        ll.draw(win)
        if abs(pt.x-ptList[0].x)+abs(pt.y-ptList[0].y)<12:
            poly=Polygon(ptList[:-1])
            poly.setOutline(color_rgb(color[2],color[1],color[0]))
            poly.setFill(color_rgb(color[2],color[1],color[0]))
            poly.draw(win)
            hexcol='#%02x%02x%02x'%(color[2],color[1],color[0])
            print(pointList[:-2])
            img1 = ImageDraw.Draw(newImage)
            img1.polygon(pointList[:-2], fill =hexcol, outline =hexcol)
            for pts in ptList:
                pts.undraw()
            for lls in llList:
                lls.undraw()
            lx=10000
            ly=10000
            ux=-10000
            uy=-10000
            for pts in ptList:
                lx=min(lx,pts.x)
                ly=min(ly,pts.y)
                ux=max(ux,pts.x)
                uy=max(uy,pts.y)
            return([[lx,ly],[ux,uy]])


def go(fn):
    
    c=1
    reList=[]
    while 1:
        reList.append(getPoly(colors[c],win))
        c+=1
        if win.checkKey()=='b':
            myImage.undraw()
            win.setBackground("black")
            npar=np.array(reList)
            np.save(fn+'.npy', npar)
            newImage.save('./output/'+fn+"mod.png")
            break


for fname in onlyfiles:
    fn=fname[:-4]
    print(fn)
    filename='./input/'+fn+'.png'
    imag=PIL.Image.open(filename)
    imag.show()
    inp=input()
    if inp=='g':
        im=cv2.imread(filename)
        h, w, c = im.shape
        win = GraphWin("pslite",w,h)
        myImage = Image(Point(w/2,h/2), filename)
        myImage.draw(win)
        newImage=PIL.Image.new(mode="RGB",size=(w,h),color=(0,0,0))    
        go(fn)
    imag.close()
    