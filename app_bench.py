import os
import tempfile
from collections import defaultdict
from sqlite3 import dbapi2 as sqlite3
import time
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash, _app_ctx_stack,\
    safe_join, escape
import timeit
import pypuzzle

# configuration
DATABASE = 'db/puzzle.db'
#PUZZLE_IMAGE_DIR = 'puzzle_images'
PUZZLE_IMAGE_DIR = './static/puzzle_images'

IMAGES_PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
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
    cursor.execute('select distinct image.file_path, image.name, image.description from image LIMIT 30')
    images = cursor.fetchall()
    cursor.close()
    return images


@app.route("/")
def index():
    return render_template('index.html', result_images=get_puzzle_images(), result_title='Popular Ones')


@app.route('/about')
def about():
    return '<p>about page</p>'


def benchmark():
    cursor = get_cursor()
    outputlst = []
    for image_name in os.listdir(PUZZLE_IMAGE_DIR):
        if not (image_name.endswith('.jpg') or image_name.endswith('.jpeg')): continue
        image_path = os.path.join(PUZZLE_IMAGE_DIR, image_name)
        vec = puzzle.get_cvec_from_file(image_path)
        vec_str = ''.join([str(i) for i in vec])
        vec_strs = [("%s" % (vec_str[i: 10+i])) for i in range(100)]
        #ot0 = [(("%s" % (i)) for i in range(100))]
        #ot1= [(("%s" % (vec_str[i: 10+i])) for i in range(100))]
        #ot =  [((("%s" % (i)), ("%s" % (vec_str[i: 10+i]))) for i in range(100))]
        ot = []
        for i in range(0,100):
            lst= vec_str[i:10+i]
            ot.append(("{i}".format(i=i),"{lst}".format(lst=lst)))          
        #place_holder = '?'
        #place_holders = ','.join(len(vec_strs)*[place_holder])
        similar_images=[]
        for i in range(100):
            req = "select image.file_path, image.name, image.description from img_sig_words isw left join image on isw.image_id=image.image_id where position = {p1} and sig_word ='{p2}'".format(p1 =ot[i][0], p2=str(ot[i][1]))
            #print(req)
            cursor.execute(req)
            temp_images = cursor.fetchall()
            for image in temp_images:
                similar_images.append(image)
        output = []
        table = defaultdict(int)
        inserted = defaultdict(lambda: False)
        for i in similar_images:
            table[i[1]] +=1
        for i in similar_images:
            if (table[i[1]] > 4) and (inserted[i] == False):
                inserted[i] = True
                output.append(i)
        #print(output)
        for e in output:
            outputlst.append(e)

    #return outputlst



def search_images(request):
    cursor = get_cursor()
    if request.files.get('image'):

        temp = tempfile.NamedTemporaryFile()
        image_file = request.files['image']
        temp.write(image_file.read())
        temp.flush()

        vec_str = ''.join(map(lambda n: str(n), puzzle.get_cvec_from_file(temp.name)))
        vec_strs = [("%s__%s" % (i, vec_str[i: 10+i])) for i in range(100)]

        place_holder = '?'
        place_holders = ','.join(len(vec_strs)*[place_holder])
        cursor.execute('select image.file_path, image.name, image.description from img_sig_words isw left join image on isw.image_id=image.image_id where sig_word in (%s)' % place_holders, vec_strs)
        similar_images = cursor.fetchall()
        output = []
        table = defaultdict(int)
        inserted = defaultdict(lambda: False)
        for i in similar_images:
            table[i[1]] +=1
        for i in similar_images:
            if (table[i[1]] > 4) and (inserted[i] == False):
                inserted[i] = True
                output.append(i)
        return output

              

    elif request.form.get('search_text'):
        cursor.execute("select * from image where description like ?", ['%' + request.form['search_text'] + '%'])
        print request.form['search_text']
        similar_images = cursor.fetchall()

    cursor.close()

    return similar_images


@app.route("/search", methods=['POST'])
def search():
    #similar_images = search_images(request)
    #time = timeit.timeit("benchmark()", number = 1000, setup="from search import benchmark")
    #print("Time to benchmark is {time}".format(time=time))
    time1 = time.time()
    for i in range(0,5):
        benchmark()
    time2 = time.time()
    print(str((time2 - time1)/5))



    similar_images = search_images(request)

    return render_template('index.html', result_images=similar_images, result_title="Search Result")


if __name__ == "__main__":
    app.run()
