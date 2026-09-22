import pypuzzle
import time
import os
import phash


BENCH_DIR = os.path.join(os.getcwd(),"bench/")
print(os.getcwd())
os.chdir(BENCH_DIR)

for image_name in os.listdir(BENCH_DIR):
	if not (image_name.endswith('.gif')): continue
		#image_path = os.path.join(BENCH_DIR, image_name)
	gifalt = str(image_name + str(2) )
	inputstring = 'convert {gifname} -coalesce -set dispose previous {gifnamealt}'.format(gifname=image_name,gifnamealt=gifalt)
	os.system(inputstring)
	namejpeg = gifalt.partition(".")[0]
	inputstring = 'convert -strip {gifnamealt} {name}.jpg'.format(gifnamealt=gifalt,name=namejpeg)
	os.system(inputstring)




puzzle = pypuzzle.Puzzle()
cvecs = []
startTimefileLoad = time.time()




for image_name in os.listdir(BENCH_DIR):
    if not (image_name.endswith('.jpg') or image_name.endswith('.jpeg')): continue

    image_path = os.path.join(BENCH_DIR, image_name)
    vec = puzzle.get_cvec_from_file(image_path)
    cvecs.append([image_name,vec])
beginVecCompare = time.time()
count = 0
for x in xrange(0,2):
	distances = []
	for vec1 in cvecs:
		for vec2 in cvecs:
			if vec1==vec2: continue
			count = count+1
			distances.append([vec1[0],vec2[0],puzzle.get_distance_from_cvec(vec1[1],vec2[1])])
endVecCompare = time.time()



print("Number of items compared:" + str(count))
print("Time to load files and get cvec" + str(startTimefileLoad - beginVecCompare))
print("Time to compare Vectors" + str(beginVecCompare - endVecCompare))

for distance in distances:
	if distance[2] < .3:
		print("Distance is {distance}".format(distance = distance[2]))






