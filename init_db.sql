DROP TABLE IF EXISTS propertydata;
CREATE TABLE IF NOT EXISTS "propertydata" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"current_appraised"	REAL,
	"current_assessed"	REAL,
	"current_tax"	REAL,
	"last_appraised" REAL,
	"last_assessed" REAL,
	"last_tax" REAL,
        "last_updated" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO propertydata (name) VALUES
('802 San Pedro'), ('800 San Pedro'),
('706 San Pedro'), ('704 San Pedro'),
('702 San Pedro'), ('700 San Pedro');
