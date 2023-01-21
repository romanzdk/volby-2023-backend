CREATE TABLE overall_over_time (
	"last_update" TIMESTAMP,
	"Babiš" NUMERIC,
	"Nerudová" NUMERIC,
	"Pavel" NUMERIC,
	"Bašta" NUMERIC,
	"Diviš" NUMERIC,
	"Fischer" NUMERIC,
	"Hilšer" NUMERIC,
	"Zima" NUMERIC
);
CREATE TABLE additional_info (
	"last_update" TIMESTAMP,
	"KOLO" NUMERIC,
	"OKRSKY_CELKEM" NUMERIC,
	"OKRSKY_ZPRAC" NUMERIC,
	"OKRSKY_ZPRAC_PROC" NUMERIC,
	"ZAPSANI_VOLICI" NUMERIC,
	"VYDANE_OBALKY" NUMERIC,
	"UCAST_PROC" NUMERIC,
	"ODEVZDANE_OBALKY" NUMERIC,
	"PLATNE_HLASY" NUMERIC,
	"PLATNE_HLASY_PROC" NUMERIC
);
CREATE TABLE kraje (
	"last_update" TIMESTAMP,
	"Kraj" VARCHAR,
	"Babiš" NUMERIC,
	"Nerudová" NUMERIC,
	"Pavel" NUMERIC,
	"Bašta" NUMERIC,
	"Diviš" NUMERIC,
	"Fischer" NUMERIC,
	"Hilšer" NUMERIC,
	"Zima" NUMERIC,
	"Zpracováno" NUMERIC
);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Hlavní město Praha',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Královéhradecký kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Středočeský kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Pardubický kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Karlovarský kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Plzeňský kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Zlínský kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Liberecký kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Ústecký kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Jihočeský kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Moravskoslezský kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Jihomoravský kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Olomoucký kraj',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
INSERT INTO kraje
VALUES (
		'2023-01-28 10:00',
		'Kraj Vysočina',
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0
	);
CREATE TABLE cities (
	"Město" VARCHAR,
	"Jméno" VARCHAR,
	"Hlasů" NUMERIC
);
CREATE TABLE last_batch (last_batch INT);
INSERT INTO last_batch
VALUES (1);
CREATE TABLE city_mapping (OBEC VARCHAR, NAZEVOBCE VARCHAR);
\ COPY city_mapping
FROM 'data/obce.csv' DELIMITER ';' CSV HEADER;