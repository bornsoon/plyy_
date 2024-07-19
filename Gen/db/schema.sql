
-- SRC 테이블
CREATE TABLE IF NOT EXISTS 'SRC' (
    'src_uuid' TEXT PRIMARY KEY,
    'src_title' TEXT NOT NULL,
    'src_artist' TEXT NOT NULL,
    'src_album' TEXT NOT NULL,
    'src_album_img' TEXT NOT NULL,
    'src_rtime' INTEGER NOT NULL
);

-- SONG 테이블
CREATE TABLE IF NOT EXISTS 'SONG' (
    'song_uuid' TEXT PRIMARY KEY,
    'song_cmt' TEXT,
    'song_vid' TEXT NOT NULL,
    'song_index' TEXT NOT NULL,
    'plyy_uuid' TEXT NOT NULL,
    'src_uuid' TEXT NOT NULL,
    FOREIGN KEY ('plyy_uuid') REFERENCES 'PLYY.plyy_uuid',
    FOREIGN KEY ('src_uuid')  REFERENCES 'SRC.src_uuid'
);

-- PLYY 테이블
CREATE TABLE IF NOT EXISTS "PLYY"(
    "plyy_uuid" TEXT PRIMARY KEY,
    "plyy_title" TEXT NOT NULL,
    "plyy_img" TEXT NOT NULL,
    "plyy_gen_date" DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "plyy_update_date" DATETIME,
    "plyy_cmt" TEXT NOT NULL,
    "c_uuid" TEXT NOT NULL,
    "gtag_uuid" TEXT NOT NULL,
    FOREIGN KEY ("c_uuid") REFERENCES "CURATOR.c_uuid"
    FOREIGN KEY ("gtag_uuid") REFERENCES "GENRE_TAG.gtag_uuid"
);

-- TAG_PLYY 테이블
CREATE TABLE IF NOT EXISTS "TAG_PLYY"(
    "tp_uuid" TEXT PRIMARY KEY,
    "tag_uuid" TEXT NOT NULL,
    "plyy_uuid" TEXT,
    FOREIGN KEY ("tag_uuid") REFERENCES "TAG.tag_uuid",
    FOREIGN KEY ("plyy_uuid") REFERENCES "PLYY.plyy_uuid"
);

-- TAG_CURATOR 테이블
CREATE TABLE IF NOT EXISTS "TAG_CURATOR"(
    "tc_uuid" TEXT PRIMARY KEY,
    "tag_uuid" TEXT NOT NULL,
    "c_uuid" TEXT,
    FOREIGN KEY ("tag_uuid") REFERENCES "TAG.tag_uuid",
    FOREIGN KEY ("c_uuid") REFERENCES "CURATOR.c_uuid"
);

-- TAG 테이블
CREATE TABLE IF NOT EXISTS "TAG"(
    "tag_uuid" TEXT PRIMARY KEY,
    "tag_name" TEXT NOT NULL UNIQUE
);

-- TAG_GENRE 테이블
CREATE TABLE IF NOT EXISTS "TAG_GENRE"(
    "gtag_uuid" TEXT PRIMARY KEY,
    "gtag_name" TEXT NOT NULL UNIQUE
);

-- CURATOR 테이블
CREATE TABLE IF NOT EXISTS 'CURATOR' (
    'c_uuid' PRIMARY KEY NOT NULL,
    'c_name' TEXT NOT NULL,
    'c_img' TEXT NOT NULL,
    'c_intro' TEXT NOT NULL
    );

-- USER 테이블
CREATE TABLE IF NOT EXISTS 'USER' (
    'u_uuid' PRIMARY KEY NOT NULL,
    'u_email' TEXT NOT NULL UNIQUE,
    'u_pw' TEXT NOT NULL,
    'u_nickname' TEXT NOT NULL,
    'u_img' TEXT
);

-- PLYY_LIKE 테이블
CREATE TABLE IF NOT EXISTS 'PLYY_LIKE' (
    'pl_uuid' PRIMARY KEY NOT NULL,
    'u_uuid' TEXT NOT NULL,
    'plyy_uuid' TEXT NOT NULL,
    FOREIGN KEY ('u_uuid') REFERENCES 'USER.u_uuid',
    FOREIGN KEY ('plyy_uuid') REFERENCES 'PLYY.plyy_uuid'
);

-- CURATOR_LIKE 테이블
CREATE TABLE IF NOT EXISTS 'CURATOR_LIKE' (
    'cl_uuid' PRIMARY KEY NOT NULL,
    'u_uuid' TEXT NOT NULL,
    'c_uuid' TEXT NOT NULL,
    FOREIGN KEY ('u_uuid') REFERENCES 'USER.u_uuid',
    FOREIGN KEY ('c_uuid') REFERENCES 'CURATOR.c_uuid'
);