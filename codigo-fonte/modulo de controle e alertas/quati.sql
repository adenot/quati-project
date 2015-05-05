
BEGIN TRANSACTION;

DROP TABLE IF EXISTS objects;

CREATE TABLE objects (
       id INTEGER PRIMARY KEY AUTOINCREMENT
     , name TEXT NOT NULL
     , value TEXT NOT NULL
);

DROP INDEX IF EXISTS object_value;

CREATE INDEX object_value ON objects (value);

DROP TABLE IF EXISTS rules;

CREATE TABLE rules (
       id INTEGER PRIMARY KEY AUTOINCREMENT
     , description TEXT
     , source_object INTEGER
     , source_port INTEGER
     , destination_ip TEXT
     , destination_port INTEGER
     , service TEXT DEFAULT "UNKNOWN"
     , parameters TEXT
     , enabled BIT NOT NULL DEFAULT 0
     , alert BIT NOT NULL DEFAULT 0
);


DROP TABLE IF EXISTS logs;

CREATE TABLE logs (
       id INTEGER PRIMARY KEY AUTOINCREMENT
	 , timestamp REAL
     , source_ip TEXT
     , source_port INTEGER
     , destination_ip TEXT
     , destination_port INTEGER
     , service TEXT DEFAULT "UNKNOWN"
     , parameters TEXT
);


INSERT INTO "rules" VALUES(1, 'acesso youtube secretaria', 1, 0, null, 80, 'HTTP', 'youtube.com', 1, 1);
INSERT INTO "rules" VALUES(2, 'acesso uol financeiro', 2, 0, null, 80, 'HTTP', 'uol.com.br', 1, 1);

INSERT INTO "objects" VALUES(1, 'secretaria', '10.211.55.3');
INSERT INTO "objects" VALUES(2, 'maq financeiro', '10.211.55.5');


COMMIT;