from PIL import Image
import sys
import os

def processImage(infile):
    try:
        im = Image.open(infile)
    except IOError:
        print "Cant load", infile
        sys.exit(1)
    i = 0
    mypalette = im.getpalette()

    try:
        while 1:
            im.putpalette(mypalette)
            new_im = Image.new("RGB", im.size)

            #new_im = Image.new("RGB", im.size)
            new_im.paste(im)
            new_im.save('foo'+str(i)+'.png')
            #if(os.stat('foo' + str(i)+'.png')):
               # os.remove('foo' + str(i) + '.jpg')
               #print("hello")
            i += 1
            mypalette = im.getpalette()
            im.seek(im.tell() + 1)

    except EOFError:
        pass # end of sequence

