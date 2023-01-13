from typing import Any
import datetime
import logging
import time
import unicodedata

import psycopg2
import requests
import xmltodict

import settings.base
import settings.static


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger('volby-backend')


def get_connection():
	return psycopg2.connect(
		database = settings.base.DATABASE,
		host = settings.base.DB_HOST,
		port = settings.base.DB_PORT,
		user = settings.base.DB_USER,
		password = settings.base.DB_PASSWORD,
	)


def get_insert_overall_results_query(data):
	return f'''
        INSERT INTO overall_over_time VALUES 
        (
            '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}'::TIMESTAMP, 
            {data['babis']},
            {data['nerudova']},
            {data['pavel']},
            {data['basta']},
            {data['divis']},
            {data['fischer']},
            {data['hilser']},
            {data['zima']}
        );
    '''


def get_insert_additional_info_query(data):
	return f'''
        INSERT INTO additional_info VALUES 
        (
            '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}'::TIMESTAMP,
            {float(data['@KOLO'])},
            {float(data['@OKRSKY_CELKEM'])},
            {float(data['@OKRSKY_ZPRAC'])},
            {float(data['@OKRSKY_ZPRAC_PROC'])},
            {float(data['@ZAPSANI_VOLICI'])},
            {float(data['@VYDANE_OBALKY'])},
            {float(data['@UCAST_PROC'])},
            {float(data['@ODEVZDANE_OBALKY'])},
            {float(data['@PLATNE_HLASY'])},
            {float(data['@PLATNE_HLASY_PROC'])}
        );
    '''


def get_insert_region_query(region, details):
	return f'''
        INSERT INTO kraje VALUES 
        (
            '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}'::TIMESTAMP,
            '{region}',
            {details[0]['babis']},
            {details[0]['nerudova']},
            {details[0]['pavel']},
            {details[0]['basta']},
            {details[0]['divis']},
            {details[0]['fischer']},
            {details[0]['hilser']},
            {details[0]['zima']},
            {details[1]}
        );
    '''


def save_data_to_db(connection, query):
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		logger.info('Successfully inserted data %s', query)
	except psycopg2.Error as error:
		logger.error('Failed to insert records into DB: %s', error)
		if connection:
			cursor.close()
			connection.close()
			logger.info('PostgreSQL connection is closed')


def _send_request(url):
	time.sleep(1)  # there were some issues with sending requests

	def _try(url):
		return requests.get(url = url, headers = settings.static.EXTRA_HEADERS)

	try:
		resp = _try(url)
	except (ConnectionError, ConnectionResetError, requests.exceptions.ConnectionError) as error:
		logger.error('There was an error sending request: %s', error)
		time.sleep(1)
		logger.info('Requesting again ...')
		resp = _try(url)
	return xmltodict.parse(resp.content)


def get_regions_data():
	resp = _send_request(settings.static.KRAJE_URL)
	regions = resp['VYSLEDKY_KRAJMESTA']['KRAJ']
	result = {}
	for region in regions:
		candidates = region['CELKEM']['HODN_KAND']
		candidates_info = {}
		for candidate in candidates:
			candidate_name = settings.static.CANDIDATE_MAP[int(candidate['@PORADOVE_CISLO'])]
			candidates_info[candidate_name] = float(candidate['@HLASY'])
		zpracovano = float(region['CELKEM']['UCAST']['@OKRSKY_ZPRAC_PROC'])
		result[region['@NAZ_KRAJ']] = candidates_info, zpracovano

	return result


def get_overall_data() -> tuple[dict[str, Any], dict[str, str]]:
	resp = _send_request(settings.static.URL)
	candidates = resp['VYSLEDKY']['CR']['KANDIDAT']
	overall_results = {}
	for candidate in candidates:
		candidate_name = settings.static.CANDIDATE_MAP[int(candidate['@PORADOVE_CISLO'])]
		overall_results[candidate_name] = float(candidate['@HLASY_PROC_1KOLO'])

	return overall_results, resp['VYSLEDKY']['CR']['UCAST']


def main():
	overall_results, additional_info = get_overall_data()
	regions = get_regions_data()
	connection = get_connection()

	# overall results
	query = get_insert_overall_results_query(overall_results)
	save_data_to_db(connection, query)

	# additional info data
	query = get_insert_additional_info_query(additional_info)
	save_data_to_db(connection, query)

	# candidate vs. region
	for region, details in regions.items():
		query = get_insert_region_query(region, details)
		save_data_to_db(connection, query)

	connection.commit()
	connection.close()
	logger.info('PostgreSQL connection is closed')


if __name__ == '__main__':
	logger.info('Starting app...')
	while True:
		main()
		logger.info('Sleeping...')
		time.sleep(120)  # sleep 2 mins
