-- flaskr/schema.sql
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS provas;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE provas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    titulo TEXT NOT NULL,
    serie TEXT NOT NULL,
    materia TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);