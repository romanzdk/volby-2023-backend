from typing import Any
import datetime
import logging
import time

import psycopg2
import pytz
import requests
import xmltodict

import settings.base
import settings.static


logging.basicConfig(level = settings.base.LOG_LEVEL)
logger = logging.getLogger('volby-backend-data')

##### Get data


def _send_request(url: str) -> dict[Any, Any]:
	retries = 0
	while retries < settings.static.RETRIES:
		try:
			retries += 1
			logger.debug('Sending request, try no: %s', retries)
			resp = requests.get(url, timeout = 5)
			break
		except (requests.exceptions.ConnectionError) as error:
			logger.warning('Failed to send request, error: %s', error)
			time.sleep(3)

	return xmltodict.parse(resp.content)


def get_overall_data() -> tuple[dict[str, float], dict[str, float]]:
	resp = _send_request(settings.static.URL)
	candidates = resp['VYSLEDKY']['CR']['KANDIDAT']
	overall_results = {}
	for candidate in candidates:
		candidate_name = settings.static.CANDIDATE_MAP[int(candidate['@PORADOVE_CISLO'])]
		try:
			overall_results[candidate_name] = float(candidate['@HLASY_PROC_2KOLO']) / 100
		except KeyError:
			# not all candidates have `HLASY_PROC_2KOLO` attribute
			pass

	additional_data = {}
	for k, v in resp['VYSLEDKY']['CR']['UCAST'][1].items():
		additional_data[k] = float(v)

	return overall_results, additional_data


def get_regions_data() -> dict[str, tuple[dict[str, float], float]]:
	resp = _send_request(settings.static.KRAJE_URL)
	regions = resp['VYSLEDKY_KRAJMESTA']['KRAJ']
	result = {}
	for region in regions:
		candidates = region['CELKEM']['HODN_KAND']
		candidates_info = {}
		for candidate in candidates:
			candidate_name = settings.static.CANDIDATE_MAP[int(candidate['@PORADOVE_CISLO'])]
			candidates_info[candidate_name] = float(candidate['@HLASY'])
		zpracovano = float(region['CELKEM']['UCAST']['@OKRSKY_ZPRAC_PROC']) / 100
		result[region['@NAZ_KRAJ']] = candidates_info, zpracovano

	return result


##### Queries


def _get_current_timestamp() -> str:
	return datetime.datetime.now(tz = pytz.timezone('Europe/Prague')).strftime('%Y-%m-%d %H:%M:%S')


def get_insert_overall_results_query(data: dict[str, Any]) -> str:
	return f'''
        INSERT INTO overall_over_time VALUES 
        (
            '{_get_current_timestamp()}'::TIMESTAMP,
            {data.get('babis',0)},
            {data.get('nerudova',0)},
            {data.get('pavel',0)},
            {data.get('basta',0)},
            {data.get('divis',0)},
            {data.get('fischer',0)},
            {data.get('hilser',0)},
            {data.get('zima',0)}
        );
    '''


def get_insert_additional_info_query(data: dict[str, float]) -> str:
	return f'''
        INSERT INTO additional_info VALUES 
        (
            '{_get_current_timestamp()}'::TIMESTAMP,
            {data['@KOLO']},
            {data['@OKRSKY_CELKEM']},
            {data['@OKRSKY_ZPRAC']},
            {data['@OKRSKY_ZPRAC_PROC']},
            {data['@ZAPSANI_VOLICI']},
            {data['@VYDANE_OBALKY']},
            {data['@UCAST_PROC']},
            {data['@ODEVZDANE_OBALKY']},
            {data['@PLATNE_HLASY']},
            {data['@PLATNE_HLASY_PROC']}
        );
    '''


def get_insert_region_query(region: str, details: tuple[dict[str, float], float]):
	return f'''
        INSERT INTO kraje VALUES 
        (
            '{_get_current_timestamp()}'::TIMESTAMP,
            '{region}',
            {details[0].get('babis',0)},
            {details[0].get('nerudova',0)},
            {details[0].get('pavel',0)},
            {details[0].get('basta',0)},
            {details[0].get('divis',0)},
            {details[0].get('fischer',0)},
            {details[0].get('hilser',0)},
            {details[0].get('zima',0)},
            {details[1]}
        );
    '''


##### Save data


def get_connection():
	return psycopg2.connect(
		database = settings.base.DATABASE,
		host = settings.base.DB_HOST,
		port = settings.base.DB_PORT,
		user = settings.base.DB_USER,
		password = settings.base.DB_PASSWORD,
	)


def save_data_to_db(connection, query: str, logger: logging.Logger):
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		cursor.close()
	except psycopg2.Error as error:
		logger.error('Failed to insert records into DB: %s', error)
		if connection:
			cursor.close()
			connection.close()
			logger.info('PostgreSQL connection is closed')
