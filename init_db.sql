DROP TABLE IF EXISTS propertydata;
CREATE TABLE IF NOT EXISTS "propertydata" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"cad" TEXT NOT NULL,
	"current_appraised"	REAL,
	"current_assessed"	REAL,
	"current_tax"	REAL,
	"last_appraised" REAL,
	"last_assessed" REAL,
	"last_tax" REAL,
        "last_updated" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO propertydata (name, cad) VALUES
('802 San Pedro', 'bcad'), ('800 San Pedro', 'bcad'),
('706 San Pedro', 'bcad'), ('704 San Pedro', 'bcad'),
('702 San Pedro', 'bcad'), ('700 San Pedro', 'bcad');
