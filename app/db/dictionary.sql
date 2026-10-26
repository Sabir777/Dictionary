PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE contexts (
	id INTEGER NOT NULL, 
	context_en TEXT NOT NULL, 
	context_ru TEXT NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_contexts_en_ru UNIQUE (context_en, context_ru)
);
INSERT INTO contexts VALUES(1,'You are given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.','Вам дан массив целых чисел nums и целое число target, верните индексы двух чисел так, чтобы их сумма была равна target.');
CREATE TABLE translations (
	id INTEGER NOT NULL, 
	word TEXT NOT NULL, 
	value TEXT NOT NULL, 
	context_id INTEGER, 
	comment TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_translates_word_value UNIQUE (word, value), 
	FOREIGN KEY(context_id) REFERENCES contexts (id)
);
INSERT INTO translations VALUES(1,'give','дать',1,'given: дан (страдательное причастие)');
INSERT INTO translations VALUES(2,'array','массив',1,NULL);
INSERT INTO translations VALUES(3,'integer','целое число',1,'мн. ч.: integers числа');
INSERT INTO translations VALUES(4,'and','и',1,NULL);
INSERT INTO translations VALUES(5,'return','вернуть',1,'в тексте: верните (повелительное наклонение)');
INSERT INTO translations VALUES(6,'index','индекс',1,'мн. ч.: indices');
INSERT INTO translations VALUES(7,'two','два',1,NULL);
INSERT INTO translations VALUES(8,'number','число',1,'мн. ч.: numbers');
INSERT INTO translations VALUES(9,'sum','сумма',1,NULL);
INSERT INTO translations VALUES(10,'equal','равный',1,'в тексте: была равна');
INSERT INTO translations VALUES(11,'you are given','вам дан',1,'в задачах: дан/дана/даны');
INSERT INTO translations VALUES(12,'add up to','в сумме давать',1,'в сумме равняться');
INSERT INTO translations VALUES(13,'add up to','равняться в сумме',1,NULL);
INSERT INTO translations VALUES(14,'such that','так, чтобы',1,'условие на выбор элементов');
INSERT INTO translations VALUES(15,'dick','член',NULL,NULL);
COMMIT;
