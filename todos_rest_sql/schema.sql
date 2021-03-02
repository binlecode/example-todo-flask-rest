
DROP TABLE IF EXISTS todo;

CREATE TABLE todo (
	id TEXT(48) NOT NULL, 
	title VARCHAR(128), 
	complete BOOLEAN, 
	PRIMARY KEY (id), 
	CHECK (complete IN (0, 1))
);
