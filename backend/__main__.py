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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def get_connection():
    return psycopg2.connect(
        database=settings.base.DATABASE,
        host=settings.base.DB_HOST,
        port=settings.base.DB_PORT,
        user=settings.base.DB_USER,
        password=settings.base.DB_PASSWORD,
    )


def get_insert_results_query(data):
    return f"""
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
    """


def get_insert_additional_info_query(data):
    return f"""
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
    """


def get_insert_kraje_query(kraj, details):
    return f"""
        INSERT INTO kraje VALUES 
        (
            '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}'::TIMESTAMP,
            '{kraj}',
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
    """


def save_data_to_db(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        logger.info("Successfully inserted data %s", query)
    except psycopg2.Error as error:
        logger.error("Failed to insert records into DB: %s", error)
        if connection:
            cursor.close()
            connection.close()
            logger.info("PostgreSQL connection is closed")


def get_kraje():
    time.sleep(1)
    try:
        resp = requests.get(
            url=settings.static.KRAJE_URL, headers=settings.static.EXTRA_HEADERS
        )
    except:
        time.sleep(1)
        resp = requests.get(
            url=settings.static.KRAJE_URL, headers=settings.static.EXTRA_HEADERS
        )
    parsed_response = xmltodict.parse(resp.content)
    result = {}
    kraje = parsed_response["VYSLEDKY_KRAJMESTA"]["KRAJ"]
    for kraj in kraje:
        candidates = kraj["CELKEM"]["HODN_KAND"]
        candidates_info = {}
        for candidate in candidates:
            key = strip_accents(
                settings.static.CANDIDATE_MAP[int(candidate["@PORADOVE_CISLO"])].lower()
            )
            candidates_info[key] = float(candidate["@HLASY"])
        zpracovano = float(kraj["CELKEM"]["UCAST"]["@OKRSKY_ZPRAC_PROC"])
        result[kraj["@NAZ_KRAJ"]] = candidates_info, zpracovano

    return result


def get_data() -> tuple[dict[str, Any], dict[str, str]]:
    time.sleep(1)
    try:
        resp = requests.get(
            url=settings.static.URL, headers=settings.static.EXTRA_HEADERS
        )
    except:
        time.sleep(1)
        resp = requests.get(
            url=settings.static.URL, headers=settings.static.EXTRA_HEADERS
        )
    parsed_response = xmltodict.parse(resp.content)
    candidates = parsed_response["VYSLEDKY"]["CR"]["KANDIDAT"]
    formatted_data = {}
    for candidate in candidates:
        key = strip_accents(candidate["@PRIJMENI"].lower())
        formatted_data[key] = float(candidate["@HLASY_PROC_1KOLO"])

    return formatted_data, parsed_response["VYSLEDKY"]["CR"]["UCAST"]


def main():
    results, additional_info = get_data()
    kraje = get_kraje()
    connection = get_connection()

    query1 = get_insert_results_query(results)
    save_data_to_db(connection, query1)

    query2 = get_insert_additional_info_query(additional_info)
    save_data_to_db(connection, query2)

    for kraj, details in kraje.items():
        query = get_insert_kraje_query(kraj, details)
        save_data_to_db(connection, query)

    connection.commit()
    logger.info("Commited")
    connection.close()
    logger.info("Closed")


if __name__ == "__main__":
    logger.info("Starting app...")
    while True:
        main()
        logger.info("Sleeping...")
        time.sleep(120)  # sleep 2 mins
