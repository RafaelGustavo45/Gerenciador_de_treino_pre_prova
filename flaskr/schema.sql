-- flaskr/schema.sql
DROP TABLE IF EXISTS questoes_alternativas;
DROP TABLE IF EXISTS resultados;
DROP TABLE IF EXISTS questoes;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS provas;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0 -- 0 = normal, 1 = admin
);

CREATE TABLE provas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id_fk INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    titulo TEXT NOT NULL,
    serie TEXT NOT NULL,
    materia TEXT NOT NULL,
    FOREIGN KEY (author_id_fk) REFERENCES user (id)
);

CREATE TABLE questoes (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   prova_id_fk INTEGER NOT NULL,
   enunciado TEXT NOT NULL,
   resposta TEXT NOT NULL, -- Gabarito (texto da alternativa correta)
   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (prova_id_fk) REFERENCES provas (id) ON DELETE CASCADE
);

CREATE TABLE questoes_alternativas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  questao_id_fk INTEGER NOT NULL,
  alternativa TEXT NOT NULL,
  is_correct INTEGER NOT NULL DEFAULT 0, -- 0 = errada, 1 = correta
  FOREIGN KEY (questao_id_fk) REFERENCES questoes (id) ON DELETE CASCADE
);

CREATE TABLE resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prova_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    acertos INTEGER NOT NULL,
    total INTEGER NOT NULL,
    nota REAL NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prova_id) REFERENCES provas (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);