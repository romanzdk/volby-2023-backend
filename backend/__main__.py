import logging
import time

import data
import settings.base


logging.basicConfig(level = settings.base.LOG_LEVEL)
logger = logging.getLogger('volby-backend')


def main() -> None:
	logger.info('Downloading overall data...')
	overall_results, additional_info = data.get_overall_data()
	logger.info('Downloading regions data...')
	regions = data.get_regions_data()
	connection = data.get_connection()
	last_batch = data.get_last_batch(connection)
	cities = data.get_cities_data(last_batch)

	# overall results
	query = data.get_insert_overall_results_query(overall_results)
	data.save_data_to_db(connection, query, logger)

	# additional info data
	query = data.get_insert_additional_info_query(additional_info)
	data.save_data_to_db(connection, query, logger)

	# candidate vs. region
	for region, details in regions.items():
		query = data.get_insert_region_query(region, details)
		data.save_data_to_db(connection, query, logger)

	# candidate vs. city
	for city_details in cities:
		query = data.get_insert_city_query(city_details)
		data.save_data_to_db(connection, query, logger)

	# update last batch
	if cities:
		query = f'UPDATE last_batch SET last_batch = {last_batch+1}'
		data.save_data_to_db(connection, query, logger)

	connection.commit()
	connection.close()
	logger.info('PostgreSQL connection is closed')


if __name__ == '__main__':
	logger.info('Starting app...')
	while True:
		main()
		logger.info('Sleeping...')
		time.sleep(120)  # sleep 2 mins
