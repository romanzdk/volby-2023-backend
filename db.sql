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
)