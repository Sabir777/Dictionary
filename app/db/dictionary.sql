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
INSERT INTO contexts VALUES(2,'You may assume that each input would have exactly one solution, and you may not use the same element twice.','Вы можете предположить, что у каждого входного значения будет ровно одно решение, и вы не можете использовать один и тот же элемент дважды.');
INSERT INTO contexts VALUES(3,'You can return the answer in any order.','Вы можете вернуть ответ в любом порядке.');
INSERT INTO contexts VALUES(4,'You are given two non-empty linked lists representing two non-negative integers.','Вам даны два непустых связанных списка, представляющих два неотрицательных целых числа.');
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
INSERT INTO translations VALUES(15,'dick','член',NULL,'***');
INSERT INTO translations VALUES(16,'you may assume','вы можете предположить',2,NULL);
INSERT INTO translations VALUES(17,'assume','предположить',2,NULL);
INSERT INTO translations VALUES(18,'each','каждый',2,NULL);
INSERT INTO translations VALUES(19,'input','входное значение',2,NULL);
INSERT INTO translations VALUES(20,'would have','будет',2,'would здесь указывает на предположение');
INSERT INTO translations VALUES(21,'exactly','ровно',2,NULL);
INSERT INTO translations VALUES(22,'one','один',2,NULL);
INSERT INTO translations VALUES(23,'solution','решение',2,NULL);
INSERT INTO translations VALUES(24,'you may not','вы не можете',2,'may not = запрет/невозможность');
INSERT INTO translations VALUES(25,'use','использовать',2,NULL);
INSERT INTO translations VALUES(26,'the same','тот же самый',2,NULL);
INSERT INTO translations VALUES(27,'element','элемент',2,NULL);
INSERT INTO translations VALUES(28,'twice','дважды',2,NULL);
INSERT INTO translations VALUES(29,'exactly one','ровно один',2,NULL);
INSERT INTO translations VALUES(30,'the same element','один и тот же элемент',2,NULL);
INSERT INTO translations VALUES(31,'use twice','использовать дважды',2,NULL);
INSERT INTO translations VALUES(32,'you can','вы можете',3,NULL);
INSERT INTO translations VALUES(33,'the answer','ответ',3,NULL);
INSERT INTO translations VALUES(34,'in any order','в любом порядке',3,NULL);
INSERT INTO translations VALUES(35,'any','любой',3,NULL);
INSERT INTO translations VALUES(36,'order','порядок',3,'in order = по порядку; in any order = в любом порядке');
INSERT INTO translations VALUES(37,'in','в',3,NULL);
INSERT INTO translations VALUES(38,'return the answer','вернуть ответ',3,NULL);
INSERT INTO translations VALUES(39,'any order','любой порядок',3,NULL);
INSERT INTO translations VALUES(40,'you are given','вам даны',4,'пассивная конструкция: вам дают / предоставлены на вход');
INSERT INTO translations VALUES(41,'given','данный',4,'в задачах: то, что подаётся на вход');
INSERT INTO translations VALUES(42,'non-empty','непустой',4,'non- = приставка отрицания');
INSERT INTO translations VALUES(43,'empty','пустой',4,NULL);
INSERT INTO translations VALUES(44,'linked list','связанный список',4,NULL);
INSERT INTO translations VALUES(45,'linked','связанный',4,NULL);
INSERT INTO translations VALUES(46,'list','список',4,NULL);
INSERT INTO translations VALUES(47,'representing','представляющий',4,'причастие от represent');
INSERT INTO translations VALUES(48,'represent','представлять',4,NULL);
INSERT INTO translations VALUES(49,'non-negative','неотрицательный',4,'включает ноль');
INSERT INTO translations VALUES(50,'negative','отрицательный',4,NULL);
INSERT INTO translations VALUES(51,'two non-empty linked lists','два непустых связанных списка',4,NULL);
INSERT INTO translations VALUES(52,'two non-negative integers','два неотрицательных целых числа',4,NULL);
INSERT INTO translations VALUES(53,'representing two integers','представляющий два целых числа',4,NULL);
COMMIT;
