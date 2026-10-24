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
INSERT INTO translates VALUES(1,'hello','привет',NULL,NULL,NULL);
INSERT INTO translates VALUES(2,'goodbye','пока',NULL,NULL,NULL);
INSERT INTO translates VALUES(3,'hi','привет',NULL,NULL,NULL);
INSERT INTO translates VALUES(4,'bye','пока',NULL,NULL,NULL);
COMMIT;
