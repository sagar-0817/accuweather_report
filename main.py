# Import all necessary libraries
import requests
import logging
import datetime
import os
from google.cloud import secretmanager
from google.cloud import bigquery
import google.cloud.logging

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("DATASET_ID")

def send_request(location_code, api_key):

    params = {
    'apikey': api_key
    }

    response = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/{location_code}/historical/24", params=params)

    if response.status_code != 200:
        logging.error(f"Invalid status code : {response.status_code}\n{response.json()}")
        return None

    return response.json()


def process_records(data_24_hours_raw):

  # Initialise a list to store processed records
  data_24_hours_processed = list()

  for record_raw in data_24_hours_raw:
    # Initialise a dictionary for processing each raw record
    record_processed = dict()

    # Extract data from raw record

    record_processed["local_observation_datetime"] = record_raw.get("LocalObservationDateTime")
    record_processed["weather_text"] = record_raw.get("WeatherText")
    record_processed["has_precipitation"] = record_raw.get("HasPrecipitation")
    record_processed["precipitation_type"] = record_raw.get("PrecipitationType")
    record_processed["is_day_time"] = record_raw.get("IsDayTime")
    record_processed["temperature_celcius"] = record_raw.get("Temperature").get("Metric").get("Value")
    record_processed["temperature_fahrenheit"] = record_raw.get("Temperature").get("Imperial").get("Value")

    # Append processed record
    data_24_hours_processed.append(record_processed)

  return data_24_hours_processed


def write_processed_records_to_bq(data_24_hours_processed, location):

    client_bq = bigquery.Client()
    
    tables = client_bq.list_tables(f"{PROJECT_ID}.{DATASET_ID}")

    for table in tables:
        # Check if the table exists
        if table.table_id == location:
            ingestion_errors = client_bq.insert_rows_json(f"{PROJECT_ID}.{DATASET_ID}.{location}", data_24_hours_processed)

            if ingestion_errors:
                logging.error(f"There were some errors during ingestion :(\n{ingestion_errors}")

            else:
                logging.info(f"The {location} table exists!! {len(data_24_hours_processed)} records written to it....")
            
            break
    else:
        logging.warning(f"The {location} table does not exist....")

        # Create table
        schema = [
        bigquery.SchemaField("local_observation_datetime", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("weather_text", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("has_precipitation", "BOOLEAN", mode="NULLABLE"),
        bigquery.SchemaField("precipitation_type", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("is_day_time", "BOOLEAN", mode="NULLABLE"),
        bigquery.SchemaField("temperature_celcius", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("temperature_fahrenheit", "FLOAT", mode="NULLABLE"),
        ]

        table = bigquery.Table(f"{PROJECT_ID}.{DATASET_ID}.{location}", schema=schema)
        table = client_bq.create_table(table)

        logging.info(f"The table {table.project}.{table.dataset_id}.{table.table_id} has been created")

        write_processed_records_to_bq(data_24_hours_processed, location)


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # Instantiate a Cloud Logging client
    client_cl = google.cloud.logging.Client()

    # Retrieves a Cloud Logging handler based on the environment
	# you're running in and integrates the handler with the
	# Python logging module. By default this captures all logs
	# at INFO level and higher
    client_cl.get_default_handler()
    client_cl.setup_logging()

    # Create the Secret Manager client
    client_sm = secretmanager.SecretManagerServiceClient()

    # Secret ID of the Accuweather API Key
    name = "projects/395637812649/secrets/ACCUWEATHER_API_KEY/versions/1" 

    # Access the secret version
    response = client_sm.access_secret_version(request={"name": name})

    api_key = response.payload.data.decode("UTF-8")

    location_codes_mapper = {
        "chennai": 206671,
        "bengaluru": 204108,
        "mumbai": 204842,
        "delhi": 202396,
        "kolkata": 206690
    }

    for location, location_code in location_codes_mapper.items():

        data_24_hours_raw = send_request(location_code, api_key)

        if data_24_hours_raw is None:
            logging.error(f"No records returned while scraping the weather data of {location}")
            return "Something went wrong :("

        data_24_hours_processed = process_records(data_24_hours_raw)

        write_processed_records_to_bq(data_24_hours_processed, location)

    return "Success!"
