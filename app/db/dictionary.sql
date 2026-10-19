PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE translates (
	id INTEGER NOT NULL, 
	word TEXT NOT NULL, 
	value TEXT NOT NULL, 
	context_en TEXT, 
	context_ru TEXT, 
	comment TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_translates_word_value UNIQUE (word, value)
);
INSERT INTO translates VALUES(1,'Hello','Привет',NULL,NULL,NULL);
INSERT INTO translates VALUES(2,'Goodbye','Пока',NULL,NULL,NULL);
INSERT INTO translates VALUES(3,'Hi','Привет',NULL,NULL,NULL);
INSERT INTO translates VALUES(4,'Bye','Пока',NULL,NULL,NULL);
COMMIT;
