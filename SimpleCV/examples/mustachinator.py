#!/usr/bin/python 

import time, webbrowser
from operator import add
from SimpleCV import Color, ColorCurve, Camera, Image, pg, np, cv, HaarCascade
from SimpleCV.Display import Display

cam = Camera(0)
time.sleep(.1) # uhg
display = Display((800,600))
counter = 0
# load the cascades
face_cascade = HaarCascade("./../Features/HaarCascades/face.xml")
nose_cascade = HaarCascade("./../Features/HaarCascades/nose.xml")
stache = Image("./stache.png") # load the stache
mask = stache.createAlphaMask() # load the stache mask
count = 0
while( display.isNotDone() ):
    #count = count + 1
    img = cam.getImage()
    img = img.scale(.5) #use a smaller image
    faces = img.findHaarFeatures(face_cascade) #find faces
    if( faces is not None ): # if we have a face
        faces = faces.sortArea() #get the biggest one
        face = faces[-1]
        myFace = face.crop() # get the face image
        noses = myFace.findHaarFeatures(nose_cascade) #find the nose
        if( noses is not None ):# if we have a nose
            noses = noses.sortArea()
            nose = noses[0] # get the biggest
            # these get the upper left corner of the face/nose
            # with respect to original image
            xf = face.x -(face.width()/2)
            yf = face.y -(face.height()/2)
            xm = nose.x -(nose.width()/2)
            ym = nose.y -(nose.height()/2)
            #calculate the mustache position
            xmust = xf+xm-(stache.width/2)+(nose.width()/2)           
            ymust = yf+ym+(2*nose.height()/3)
            #blit the stache/mask onto the image
            img = img.blit(stache,pos=(xmust,ymust),mask = mask)
            #img.drawRectangle( xf+xm, yf+ym, nose.width(), nose.height() )
            #img.drawRectangle( xf, yf, face.width(), face.height() )
            #name = "mustach"+str(count)+".png"
            #img.save(name)
    img.scale(2) #rescale the stache
    img.save(display) #display
    time.sleep(0.01)
