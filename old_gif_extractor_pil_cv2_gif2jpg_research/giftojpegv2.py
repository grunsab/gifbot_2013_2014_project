from PIL import Image

im = Image.open('4177.gif')
transparency = im.info['transparency'] 
p = im.palette.getdata()[1]
im.save('test1.png',"PNG", transparency=transparency)
im.seek(im.tell()+1)
im.palette.dirty = 1
im.palette.rawmode = "RGB"
im.putpalette(p)
transparency = im.info['transparency']
im.save('test2.png',"PNG", transparency=transparency)
