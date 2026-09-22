import os
import tempfile
from collections import defaultdict
from sqlite3 import dbapi2 as sqlite3
from subprocess import call
import re
import pypuzzle

staticpath = "//home/rishi/gitbot-protoype/static/puzzle_images"
shortstatic = './static/puzzle_images'
puzzle = pypuzzle.Puzzle()
DATABASE = 'db/puzzle.db'
THRESHOLD = .2

re_natural = re.compile('[0-9]+|[^0-9]+')
def natural_key(s):
    return [(1, int(c)) if c.isdigit() else (0, c.lower()) for c in re_natural.findall(s)] + [s]


#Validate url for video. If valid do nothing. If invalid, return a statement, halting video parse
def validateurl(url):
    egex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    good = True
    #do processing here
    #urlstatus = either good or bad
    if url is not good:
         print("Error: Things went deadly wrong. Halting video parsing")

#Get video from url using youtube-dl, and return the temp directory where the video is stored
def getVideo(url):
    urlid = url
    os.system("""youtube-dl -o "%(id)s" {vid}""".format(vid=url))
    return os.listdir(os.getcwd())

#Turn the "temp" video into frames. Store  frame count of video into db. Store frames in temp vid dir.
def getFrames(conn, urlid):
    print("This is the current directory {dir}".format(dir=os.getcwd()))
    for vid in os.listdir(os.getcwd()):
        print("This is the video file name{Filename}".format(Filename=vid))
        s = """avconv -r 10 -i {vidname} -f image2 image-%4d.jpeg""".format(vidname=vid)
        #print(s)
        os.system(s)
        frames = len(os.getcwd()) - 1
        if frames > 0:
            conn.execute('insert into \
                 vids (url_id, frames) \
                 values (?, ?)',
                 [urlid, frames]
                 )
            conn.commit()

#Store the sigs of each sufficiently different image in the tempvid directory into the database
def storeSigs( conn, cursor,urlid):

    cursor.execute('select * from vids where url_id=?', [urlid])
    vid_id = cursor.fetchone()['vid_id']

    lastsig = ""
    curdst = 0.00
    sortedimages = sorted(os.listdir(os.getcwd()), key = natural_key)
    lastsig = puzzle.get_cvec_from_file(sortedimages[0])
    #print(sortedimages)

    newdir = os.path.join(staticpath, "{vidid}".format(vidid=vid_id))
    os.system("mkdir {dir}".format(dir = newdir))

    insertedsigs=[]
    insertedsigs.append(lastsig)
    #reset  = 100   -- use this to reset the insertedsig list for
    #very large videos
    framenum = 0
    conn.execute('BEGIN TRANSACTION')

    for image in sortedimages[1:]:
        framenum  = framenum + 1
        if not (image.endswith('.jpeg')): continue
        image_path = os.path.join(os.getcwd(), image)

        sig = puzzle.get_cvec_from_file(image_path)

        counts = 0
        # Routine to cut out similar positions from db storage
        for insig in insertedsigs:
            dist = puzzle.get_distance_from_cvec(insig,sig)
            if dist < THRESHOLD:
                counts += 1
                break
        #Insert this image sig into database
        if counts == 0:
            vec_str = ''.join([str(p) for p in sig])
            name = str(vid_id + framenum)
            new_image_path = os.path.join(shortstatic, "{vidid}/{image}".format(vidid=vid_id, image=image))
            os.system("cp {file} {dir}".format(file=image, dir=newdir))
            conn.execute('insert into \
                image (vid_id, signature,frame,file_path, name) \
                values (?, ?, ?, ?, ?)',
                [vid_id, vec_str, framenum, new_image_path, name]
                )
            insertedsigs.append(sig)


    conn.commit()

def delete(file_path, top_dir):
    print("Deleted File at {file}".format(file=file_path))
    os.chdir(top_dir)
    os.system("rm -r {dir}".format(dir=file_path))



def videoparse(url,cursor,conn):
    #Change to temp directory
    curdir = os.getcwd()
    tempvid_dir = os.path.join(curdir,"tempvid/")
    os.chdir(tempvid_dir)

    validateurl(url)
    videoDir = getVideo(url)
    getFrames(conn,url)
    storeSigs( conn, cursor, url)
    delete(tempvid_dir,curdir)
    similar_images = []
    return similar_images
