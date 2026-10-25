PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE contexts (
	id INTEGER NOT NULL, 
	context_en TEXT NOT NULL, 
	context_ru TEXT NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_contexts_en_ru UNIQUE (context_en, context_ru)
);
CREATE TABLE translations (
	id INTEGER NOT NULL, 
	word TEXT NOT NULL, 
	value TEXT NOT NULL, 
	comment TEXT, 
	context_id INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_translates_word_value UNIQUE (word, value), 
	FOREIGN KEY(context_id) REFERENCES contexts (id)
);
COMMIT;
