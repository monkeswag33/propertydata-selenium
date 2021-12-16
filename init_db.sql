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
('212 Cloud', 'w'), ('118 Brown', 'w'),
('103 Axis Deer', 'w'), ('105 Orchard'),
('6018 Andross', 'w'), ('118 Wegstrom', 'w'),
('313 Ross', 'w'), ('302 Quail', 'w'),
('403 Kates', 'w'), ('107 Orchard', 'w'),
('116 Sylvan', 'w'), ('128 Flinn', 'w'),
('900 Stewart', 'w'),
('802 San Pedro', 'b'), ('800 San Pedro', 'b'),
('706 San Pedro', 'b'), ('704 San Pedro', 'b'),
('702 San Pedro', 'b'), ('700 San Pedro', 'b');
