import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_covid_data(date):
    """
    Recover COVID data for a specific date.
    """

    url = "https://covid-api.com/api/reports"
    response = requests.get(url, params={"date": date})

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Erreur {response.status_code} pour la date {date}")
        return []

def get_latest_date_from_api():
    """
    Récupère la dernière date disponible dans l'API de la clé "date".
    """
    
    url = "https://covid-api.com/api/reports"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get("data", [])
        latest_date = max([entry.get("date") for entry in data])

        return pd.to_datetime(latest_date).date()
    else:
        print(f"Erreur {response.status_code} pour la récupération de la dernière date")

def extract_data(start_date: datetime.date):
    """
    Extract COVID data from January 22, 2020 to January 22, 2021.
    """

    if not isinstance(start_date, datetime):
        start_date = pd.to_datetime(start_date)

    start_date = pd.to_datetime(start_date).date()
    end_date = get_latest_date_from_api()

    current_date = start_date
    all_data = []

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        data = fetch_covid_data(date_str)

        for entry in data:
            all_data.append({
                "date": entry.get("date", date_str),
                "confirmed": entry.get("confirmed", 0),
                "deaths": entry.get("deaths", 0),
                "recovered": entry.get("recovered", 0),
                "confirmed_diff": entry.get("confirmed_diff", 0),
                "deaths_diff": entry.get("deaths_diff", 0),
                "recovered_diff": entry.get("recovered_diff", 0),
                "last_update": entry.get("last_update", "N/A"),
                "active": entry.get("active", 0),
                "active_diff": entry.get("active_diff", 0),
                "fatality_rate": entry.get("fatality_rate", 0.0),
                "iso": entry.get("region", {}).get("iso", "N/A"),
                "name": entry.get("region", {}).get("name", "N/A"),
                "province": entry.get("region", {}).get("province", "N/A"),
                "lat": entry.get("region", {}).get("lat", "N/A"),
                "long": entry.get("region", {}).get("long", "N/A"),
                "cities": entry.get("cities", [])
            })

        print(f"Données récupérées pour {date_str}")
        current_date += timedelta(days=1)

    df = pd.DataFrame(all_data)
    df.to_csv("covid_data.csv", index=False, encoding="utf-8")