CREATE TABLE IF NOT EXISTS "PLYY"(
    "plyy_uuid" TEXT PRIMARY KEY,
    "plyy_title" TEXT NOT NULL,
    "plyy_img" TEXT NOT NULL,
    "plyy_gen_date" DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "plyy_update_date" DATETIME NOT NULL,
    "plyy_cmt" TEXT NOT NULL,
    "c_uuid" TEXT NOT NULL,
    "gtag_uuid" TEXT NOT NULL,
    FOREIGN KEY ("c_uuid") REFERENCES "CURATOR.c_uuid"
    FOREIGN KEY ("gtag_uuid") REFERENCES "GENRE_TAG.gtag_uuid"
);
CREATE TABLE IF NOT EXISTS "TAG"(
    "tag_uuid" TEXT PRIMARY KEY,
    "tag_name" TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "TAG_GENRE"(
    "gtag_uuid" TEXT PRIMARY KEY,
    "gtag_name" TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "TAG_PLYY"(
    "tp_uuid" TEXT PRIMARY KEY,
    "tag_uuid" TEXT NOT NULL,
    "plyy_uuid" TEXT,  -- foreign인데 NULL값일수도 있는가?
    "c_uuid" TEXT,  -- foreign인데 NULL값일수도 있는가?
    FOREIGN KEY ("tag_uuid") REFERENCES "TAG.tag_uuid",
    FOREIGN KEY ("plyy_uuid") REFERENCES "PLYY.plyy_uuid",
    FOREIGN KEY ("c_uuid") REFERENCES "CURATOR.c_uuid"
);
