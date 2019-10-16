PRAGMA foreign_keys = ON;

CREATE TABLE alunos (
id INTEGER PRIMARY KEY,
nome TEXT,
nacionalidade TEXT,
idade INTEGER
);

CREATE TABLE disciplina (
id INTEGER PRIMARY KEY,
designacao TEXT,
ano INTEGER,
semestre INTEGER
);

CREATE TABLE turma (
id INTEGER PRIMARY KEY,
id_disciplina INTEGER,
tipo TEXT,
designacao TEXT,
FOREIGN KEY(id_disciplina) REFERENCES disciplina(id) ON DELETE CASCADE
);

CREATE TABLE inscricoes (
id_aluno INTEGER,
id_turma INTEGER,
ano_letivo TEXT,
PRIMARY KEY (id_aluno, id_turma),
FOREIGN KEY(id_aluno) REFERENCES alunos(id) ON DELETE CASCADE,
FOREIGN KEY(id_turma) REFERENCES turma(id) ON DELETE CASCADE
);