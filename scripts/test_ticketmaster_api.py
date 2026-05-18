import os

import requests
from dotenv import load_dotenv

    
load_dotenv()

API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def main():
    if not API_KEY:
        raise ValueError("No se encontro TICKETMASTER_API_KEY en el archivo .env")

    params = {
        "apikey": API_KEY,
        "countryCode": "MX",
        "classificationName": "music",
        "size": 10,
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    page_info = data.get("page", {})
    total_events = page_info.get("totalElements", 0)
    total_pages = page_info.get("totalPages", 0)

    print(f"Eventos encontrados: {total_events}")
    print(f"Paginas disponibles: {total_pages}")

    events = data.get("_embedded", {}).get("events", [])

    print("\nPrimeros eventos:")
    for event in events[:5]:
        event_name = event.get("name", "Sin nombre")
        event_date = event.get("dates", {}).get("start", {}).get("localDate", "Sin fecha")
        print(f"- {event_date} | {event_name}")


if __name__ == "__main__":
    main()