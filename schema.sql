drop table if exists image;
CREATE table image (
  image_id INTEGER NOT NULL PRIMARY KEY autoincrement,
  vid_id INTEGER NOT NULL,
  frame INTEGER NOT NULL,
  name TEXT,
  description TEXT,
  file_path TEXT,
  signature TEXT NOT NULL
);

drop table if exists vids;
CREATE table vids (
  vid_id INTEGER NOT NULL PRIMARY KEY autoincrement,
  url_id TEXT NOT NULL,
  frames INTEGER NOT NULL
);

