# Accuweather Report

## Description
An end to end Data Engineering project that:
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

## Notes

- The Cloud Function is scheduled to run every **12 hours** using Cloud Scheduler
- The Cloud Function can also be manually triggered
- The API key required to scrape the data is stored as a secret called **ACCUWEATHER_API_KEY** in Secret Manager
