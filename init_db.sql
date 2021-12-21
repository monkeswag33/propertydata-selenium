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
	"zillow_fmv" REAL,
	"redfin_fmv" REAL,
	"avg_fmv" REAL,
	"last_updated" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO propertydata (name, cad) VALUES
('212 Cloud RD', 'w'), ('118 Brown ST', 'w'),
('103 Axis Deer TRL', 'w'), ('105 Orchard WAY', 'w'),
('6018 Andross CT', 'w'), ('118 Wegstrom ST', 'w'),
('313 Ross ST', 'w'), ('302 Quail CIR', 'w'),
('403 Kates WAY', 'w'), ('107 Orchard WAY', 'w'),
('116 Sylvan ST', 'w'), ('128 Flinn ST', 'w'),
('900 Stewart DR', 'w'),
('802 San Pedro', 'b'), ('800 San Pedro', 'b'),
('706 San Pedro', 'b'), ('704 San Pedro', 'b'),
('702 San Pedro', 'b'), ('700 San Pedro', 'b');
