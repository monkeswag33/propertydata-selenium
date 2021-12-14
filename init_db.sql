DROP TABLE IF EXISTS propertydata;
CREATE TABLE IF NOT EXISTS "propertydata" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"appraised"	REAL,
	"assessed"	REAL,
	"tax"	REAL,
    "last_updated" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO propertydata (name) VALUES
('802 San Pedro'), ('800 San Pedro'),
('706 San Pedro'), ('704 San Pedro'),
('702 San Pedro'), ('700 San Pedro');