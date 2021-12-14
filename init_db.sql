DROP TABLE IF EXISTS propertydata;
CREATE TABLE IF NOT EXISTS "propertydata" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"appraised"	REAL,
	"assessed"	REAL,
	"tax"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO propertydata (name) VALUES ('802 San Pedro');