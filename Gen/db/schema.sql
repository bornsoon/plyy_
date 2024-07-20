-- SRC 테이블
CREATE TABLE IF NOT EXISTS 'TRACK' (
    'track_id' TEXT PRIMARY KEY,
    'track_title' TEXT NOT NULL,
    'track_artist' TEXT NOT NULL,
    'track_album' TEXT NOT NULL,
    'track_album_img' TEXT NOT NULL,
    'track_rtime' INTEGER NOT NULL
);

-- SONG 테이블
CREATE TABLE IF NOT EXISTS 'SONG' (
    'song_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'song_cmt' TEXT,
    'song_vid' TEXT NOT NULL,
    'song_index' INTEGER NOT NULL,
    'plyy_id' INTEGER NOT NULL,
    'track_id' TEXT NOT NULL,
    FOREIGN KEY ('plyy_id') REFERENCES 'PLYY.plyy_id' ON DELETE CASCADE,
    FOREIGN KEY ('track_id')  REFERENCES 'TRACK.track_id' ON DELETE CASCADE
);

-- PLYY 테이블
CREATE TABLE IF NOT EXISTS "PLYY"(
    "plyy_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "plyy_title" TEXT NOT NULL,
    "plyy_img" TEXT NOT NULL,
    "plyy_gen_date" DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "plyy_update_date" DATETIME,
    "plyy_cmt" TEXT NOT NULL,
    "c_id" INTEGER NOT NULL,
    "gtag_id" INTEGER NOT NULL,
    FOREIGN KEY ("c_id") REFERENCES "CURATOR.c_id",
    FOREIGN KEY ("gtag_id") REFERENCES "GENRE.gtag_id"
);

-- TAG_PLYY 테이블
CREATE TABLE IF NOT EXISTS "P_TAG"(
    "tp_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "tag_id" INTEGER NOT NULL,
    "plyy_id" INTEGER NOT NULL,
    FOREIGN KEY ("tag_id") REFERENCES "TAG.tag_id" ON DELETE CASCADE,
    FOREIGN KEY ("plyy_id") REFERENCES "PLYY.plyy_id" ON DELETE CASCADE
);

-- TAG_CURATOR 테이블
CREATE TABLE IF NOT EXISTS "C_TAG"(
    "tc_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "tag_id" INTEGER NOT NULL,
    "c_id" INTEGER NOT NULL,
    FOREIGN KEY ("tag_id") REFERENCES "TAG.tag_id" ON DELETE CASCADE,
    FOREIGN KEY ("c_id") REFERENCES "CURATOR.c_id" ON DELETE CASCADE
);

-- TAG 테이블
CREATE TABLE IF NOT EXISTS "TAG"(
    "tag_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "tag_name" TEXT NOT NULL UNIQUE
);

-- TAG_GENRE 테이블
CREATE TABLE IF NOT EXISTS "GENRE"(
    "gtag_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "gtag_name" TEXT NOT NULL UNIQUE
);

-- CURATOR 테이블
CREATE TABLE IF NOT EXISTS 'CURATOR' (
    'c_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'c_name' TEXT NOT NULL UNIQUE,
    'c_img' TEXT NOT NULL,
    'c_intro' TEXT NOT NULL
    );

-- USER 테이블
CREATE TABLE IF NOT EXISTS 'USER' (
    'u_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'u_email' TEXT NOT NULL UNIQUE,
    'u_pw' TEXT NOT NULL,
    'u_nickname' TEXT,
    'u_img' TEXT
);

-- PLYY_LIKE 테이블
CREATE TABLE IF NOT EXISTS 'P_LIKE' (
    'pl_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'u_id' INTEGER NOT NULL,
    'plyy_id' INTEGER NOT NULL,
    FOREIGN KEY ('u_id') REFERENCES 'USER.u_id' ON DELETE CASCADE,
    FOREIGN KEY ('plyy_id') REFERENCES 'PLYY.plyy_id' ON DELETE CASCADE
);

-- CURATOR_LIKE 테이블
CREATE TABLE IF NOT EXISTS 'C_LIKE' (
    'cl_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'u_id' INTEGER NOT NULL,
    'c_id' INTEGER NOT NULL,
    FOREIGN KEY ('u_id') REFERENCES 'USER.u_id' ON DELETE CASCADE,
    FOREIGN KEY ('c_id') REFERENCES 'CURATOR.c_id' ON DELETE CASCADE
);