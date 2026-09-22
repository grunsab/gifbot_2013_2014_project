Overview
===============
This is a test implementation of an image similarity search, that ultimately is designed to scale to a large number of
images. It currently uses the [Libpuzzle Library](http://www.pureftpd.org/project/libpuzzle), and a simple and
probably inefficient database schema outlined in a [stackoverflow post](http://stackoverflow.com/questions/9703762/libpuzzle-indexing-millions-of-pictures) and it uses the basic framework outlined by alsotang in this [demo project](https://github.com/alsotang/libpuzzle_demo).

The current protoype allows you to upload images and compare it to the available set of images. 
Though the protoype works, it is quite inefficient. It currently stores about 200,000 image frames per GB,
and though due to the small size of the database, there has not been a problem with performance, there may be 
quite soon.


Accessing Azure Test Installation
===============

To access the test install on Azure:

(1)  ssh -L 5000:localhost:5000 azureuser@gifprotoype.cloudapp.net    

(2) 




Installation Instructions
===============
To install on linux VM [Instructions for Ubuntu 13.04 version]

sudo apt-get install libpuzzle-dev

sudo apt-get install imagemagick libmagick++-dev

sudo apt-get install python-dev

sudo apt-get install sqlite3 libsqlite3-dev


then copy repository:

git clone https://github.com/grunsab/gitbot-protoype.git

Cd into new directory

Run the following

$ sqlite3 db/puzzle.db < schema.sql

Then run 
python init_db.py

then run python app.py

Now you should have a server running on localhost:5000


