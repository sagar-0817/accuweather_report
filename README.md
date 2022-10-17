# Accuweather Report

## Description
An end to end Data Engineering project implemented on Google Cloud Platform that:
- scrapes the last 24 hours weather data of 5 Indian cities from the [Accuweather](https://www.accuweather.com/) API
- stores the weather data corresponding to each city in Google BigQuery
- combines and transforms the raw data to be able to power dashboards
- displays the weather report through various charts in a dashboard

## Architecture
![Architecture](https://github.com/sagar-0817/accuweather_report/blob/main/images/accuweather-architecture.png?raw=true)
- The last 24 hours weather data is scraped from the Accuweather API in a Cloud Function
- The scraped data in raw form is processed in the Cloud Function and written to tables (corresponding to each city) in Google BigQuery
- The data in BigQuery is combined and transformed further using a scheduled SQL query to be able to power dashboards
- The fully transformed data is then used to create a simple Weather Report in Google Data Studio

## Dashboard
[Accuweather Report](https://datastudio.google.com/reporting/faa637b5-de05-4d32-8cc6-0cb1bc996507)

![Dashboard - Sample Preview](https://github.com/sagar-0817/accuweather_report/blob/main/images/dashboard-sample-preview.png?raw=true)

## Project Contents

- [main.py](https://github.com/sagar-0817/accuweather_report/blob/main/main.py)
    - the python script implemented as an **HTTP triggered Cloud Function** scrapes the weather data, processes the raw data and stores the processed data in BigQuery
    - a detailed explanation of the Cloud Function is mentioned as comments in the script
- [requirements.txt](https://github.com/sagar-0817/accuweather_report/blob/main/requirements.txt)
   - contains the packages required to run the script
- [locations_combined.sql](https://github.com/sagar-0817/accuweather_report/blob/main/locations_combined.sql)
    - the SQL script contains the query that combines the weather data of all locations, performs deduplication and processes the data
    - the query is saved as a view which is materialized to power the dashboard

## Notes

- The Cloud Function is scheduled to run every **12 hours** using Cloud Scheduler
- The purpose of running the Cloud Function every 12 hours (instead of 24 hours) is to have sufficient time to handle any failure(s) in the pipeline
- The data pipeline is fully monitored using **Cloud Monitoring** and any failure is reported through an email in real time
- The Cloud Function can also be manually triggered
- The API key required to scrape the data is stored as a **secret** called **ACCUWEATHER_API_KEY** in Secret Manager
