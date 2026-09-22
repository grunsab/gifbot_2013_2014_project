drop table if exists image;
CREATE table image (
  image_id INTEGER NOT NULL PRIMARY KEY autoincrement,
  vid_id INTEGER NOT NULL,
  name TEXT,
  description TEXT,
  file_path TEXT,
  signature TEXT NOT NULL
);

drop table if exists img_sig_words;
CREATE TABLE img_sig_words (
  image_id INTEGER NOT NULL,
  position INTEGER NOT NULL,
  sig_word TEXT NOT NULL
);

drop table if exists gif_table;
CREATE TABLE gif_table(
  vid_id INTEGER,
  source_url TEXT,
  frame_count INT NOT NULL,
  image_ids TEXT NOT NULL,
  signatures TEXT NOT NULL,
  category TEXT

);
drop table if exists gif_frame;
CREATE TABLE gif_frame(
  image_id INTEGER NOT NULL PRIMARY KEY autoincrement,
  gif_id INTEGER,
  signature TEXT NOT NULL

);
drop table if exists vid_table;
create table vid_table(
  vid_id INTEGER NOT NULL PRIMARY KEY autoincrement,
  url_id TEXT NOT NULL,
  category TEXT,
  frame_count INTEGER,
  image_id_set TEXT,
);

CREATE INDEX IF NOT EXISTS position_sig ON img_sig_words(sig_word,position);

