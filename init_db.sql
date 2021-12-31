DROP TABLE IF EXISTS propertydata;
CREATE TABLE "propertydata" (
	"id"	SERIAL PRIMARY KEY,
	"name"	TEXT NOT NULL,
	"cad" TEXT NOT NULL,
	"current_appraised"	INTEGER,
	"current_assessed"	INTEGER,
	"current_tax"	INTEGER,
	"last_appraised" INTEGER,
	"last_assessed" INTEGER,
	"last_tax" INTEGER,
	"zillow_fmv" INTEGER,
	"redfin_fmv" INTEGER,
	"avg_fmv" INTEGER,
	"last_updated" TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
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
