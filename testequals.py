import os

import pypuzzle

import sqlite3

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

    return output



PUZZLE_IMAGE_DIR = './static/puzzle_images'
#PUZZLE_IMAGE_DIR = './bench'
DATABASE = './db/puzzle.db'

puzzle = pypuzzle.Puzzle()

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
equal = 0
for image_name in os.listdir(PUZZLE_IMAGE_DIR):
    if not (image_name.endswith('.jpg') or image_name.endswith('.jpeg')): continue
    image_path = os.path.join(PUZZLE_IMAGE_DIR, image_name)
    vec = puzzle.get_cvec_from_file(image_path)
    #print(vec)
    cmp_vec_1 = puzzle.compress_cvec(vec)
    #print(cmp_vec_1)
    vec_str = ''.join([str(i) for i in vec])
    compare = dbsigtovec(vec_str)
    if(compare == vec):
        equal = equal + 1
    else:
        noteq = 0
        for i in xrange(max(len(vec),len(compare))):
            if(compare[i] != vec[i]):
                noteq = noteq + 1
        print(str(noteq))

print("equals" + str(equal))
