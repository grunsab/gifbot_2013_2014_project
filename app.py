import os
import tempfile
from collections import defaultdict
from sqlite3 import dbapi2 as sqlite3
import videoparse
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash, _app_ctx_stack,\
    safe_join, escape
from subprocess import call
import re
import pypuzzle
#import youtube_dl
# configuration
DATABASE = 'db/puzzle.db'
#PUZZLE_IMAGE_DIR = 'puzzle_images'
PUZZLE_IMAGE_DIR = os.path.join(os.getcwd(),"static/puzzle_images/")
IMAGES_PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'


app = Flask(__name__)
app.config.from_object(__name__)

puzzle = pypuzzle.Puzzle()



def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


def get_cursor():
    return get_db().cursor()


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def get_puzzle_images():
    # return [safe_join(app.config['PUZZLE_IMAGE_DIR'], p)
    #         for p in os.listdir('./static/%s' % app.config['PUZZLE_IMAGE_DIR'])]
    cursor = get_cursor()
    cursor.execute('select distinct image.file_path, image.name, image.description from image LIMIT 3000')
    images = cursor.fetchall()
    cursor.close()
    return images


@app.route("/")
def index():
    return render_template('index.html', result_images=get_puzzle_images(), result_title='Popular Ones')


@app.route('/about')
def about():
    return '<p>A GifBot Product.</p>'

#Search images splits image sigs into blocks
def search_images(request):
    similar_images = []
    cursor = get_cursor()
    if request.files.get('image'):
        temp = tempfile.NamedTemporaryFile()
        image_file = request.files['image']
        temp.write(image_file.read())
        temp.flush()
        vector = puzzle.get_cvec_from_file(temp.name)
        vec_str = ''.join(map(lambda n: str(n), vector))
        vec_strs = [("%s" % (vec_str[i: 10+i])) for i in range(100)]
        ot = []
        for i in range(0,100):
            lst= vec_str[i:10+i]
            ot.append(("{i}".format(i=i),"{lst}".format(lst=lst)))
        similar_images=[]
        for i in range(100):
            req = "select image.file_path, image.name, image.description from img_sig_words isw left join image on isw.image_id=image.image_id where position = {p1} and sig_word ='{p2}'".format(p1 =ot[i][0], p2=str(ot[i][1]))
            cursor.execute(req)
            temp_images = cursor.fetchall()
            #print(temp_images)
            for image in temp_images:
                similar_images.append(image)
        output = []
        table = defaultdict(int)
        inserted = defaultdict(lambda: False)
        for i in similar_images:
            table[i[1]] +=1
        for i in similar_images:
            if (table[i[1]] > 5) and (inserted[i] == False):
                inserted[i] = True
                output.append(i)
        print(output)
        cursor.close()
        return output

    elif request.form.get('video_link'):
        urlid = request.form['video_link']
        conn = get_db()
        cursor.close()
        return videoparse.videoparse(urlid,cursor,conn)

    return similar_images




#Change db sig to cvec vec
def dbsigtovec(dbstring):
    output = []
    i = 0

    while True:
        try:
            if(dbstring[i] == "-"):
                current = int(dbstring[i] + dbstring[i+1])
                output.append(current)
                i = i+2
            else:
                current = int(dbstring[i])
                output.append(current)
                i=i+1
        except:
            break
            #print("End of list reached")

    return tuple(output)





def search_image_cvec(request):
    cursor = get_cursor()
    output = []
    cvecs = []
    if request.files.get('image'):
        temp = tempfile.NamedTemporaryFile()
        image_file = request.files['image']
        temp.write(image_file.read())
        temp.flush()
        vector = puzzle.get_cvec_from_file(temp.name)
        print(vector)
        print(len(vector))
        #print(vector)
        req = "select image.file_path, image.name, image.signature from image"
        cursor.execute(req)
        temp_images = cursor.fetchall()
        for image in temp_images:
            imagevec = dbsigtovec(image['signature'])
            if((puzzle.get_distance_from_cvec(imagevec,vector)) < .45):

                output.append(image)
        cursor.close()

        return output


    elif request.form.get('video_link'):
        urlid = request.form['video_link']
        conn = get_db()
        return videoparse.videoparse(urlid,cursor,conn)


    return output


@app.route("/search", methods=['POST'])
def search():
    #similar_images = search_images(request)
    similar_images = search_image_cvec(request)
    return render_template('index.html', result_images=similar_images, result_title="Search Result")


if __name__ == "__main__":
    app.run()
