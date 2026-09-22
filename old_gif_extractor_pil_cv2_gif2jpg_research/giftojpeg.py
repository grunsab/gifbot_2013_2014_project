from PIL import Image
import sys
import cv2

def processImage(infile):
    try:
        im = Image.open(infile)
    except IOError:
        print "Cant load", infile
        sys.exit(1)
    #Identify whether black or white, and set mode
    #mode = L if black and white
    #else mode = RGB
    try:
        i= 0
        while 1:
            im.seek(i)
            imframe = im.copy()
            if i == 0: 
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass

for i, frame in enumerate(processImage('4177.gif')):
    frame.save('test%d.png' % i,**frame.info)

