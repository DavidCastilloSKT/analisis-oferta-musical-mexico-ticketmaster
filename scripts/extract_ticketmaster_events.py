import json
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "ticketmaster_events_raw.json"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "ticketmaster_events_mx_music.csv"


def get_nested_value(data, keys, default=None):
    current_value = data

    for key in keys:
        if not isinstance(current_value, dict):
            return default

        current_value = current_value.get(key)

        if current_value is None:
            return default

    return current_value


def get_primary_classification(event):
    classifications = event.get("classifications", [])

    if not classifications:
        return {}

    for classification in classifications:
        if classification.get("primary"):
            return classification

    return classifications[0]


def extract_artist_names(event):
    attractions = event.get("_embedded", {}).get("attractions", [])

    if not attractions:
        return None

    artist_names = [attraction.get("name") for attraction in attractions if attraction.get("name")]
    return ", ".join(artist_names)

def clean_city(city):
    if not city:
        return None

    city = city.strip()

    city_replacements = {
        "México": "Ciudad de México",
        "Mexico": "Ciudad de México",
        "México CDMX": "Ciudad de México",
        "Ciudad de Mexico": "Ciudad de México",
        "Col. Centro Monterrey": "Monterrey",
        "Ciudad De México": "Ciudad de México",
    }

    return city_replacements.get(city, city)


def clean_state(state):
    if not state:
        return None

    state = state.strip()

    state_replacements = {
        "Distrito Federal": "Ciudad de México",
        "Mexico City": "Ciudad de México",
    }

    return state_replacements.get(state, state)


def clean_genre(genre, subgenre):
    if genre and genre != "Undefined":
        return genre

    if subgenre and subgenre != "Undefined":
        return subgenre

    return "Sin clasificar"


def detect_festival(event_name, event_subtype):
    text = f"{event_name or ''} {event_subtype or ''}".lower()
    return "festival" in text or "fest" in text

def transform_event(event):
    venue = get_nested_value(event, ["_embedded", "venues"], [{}])[0]
    classification = get_primary_classification(event)

    return {
        "event_id": event.get("id"),
        "event_name": event.get("name"),
        "event_url": event.get("url"),
        "event_date": get_nested_value(event, ["dates", "start", "localDate"]),
        "event_time": get_nested_value(event, ["dates", "start", "localTime"]),
        "timezone": get_nested_value(event, ["dates", "timezone"]),
        "event_status": get_nested_value(event, ["dates", "status", "code"]),
        "artist_or_attraction": extract_artist_names(event),
        "venue": venue.get("name"),
        "city": get_nested_value(venue, ["city", "name"]),
        "state": get_nested_value(venue, ["state", "name"]),
        "state_code": get_nested_value(venue, ["state", "stateCode"]),
        "country": get_nested_value(venue, ["country", "name"]),
        "country_code": get_nested_value(venue, ["country", "countryCode"]),
        "latitude": get_nested_value(venue, ["location", "latitude"]),
        "longitude": get_nested_value(venue, ["location", "longitude"]),
        "segment": get_nested_value(classification, ["segment", "name"]),
        "genre": get_nested_value(classification, ["genre", "name"]),
        "subgenre": get_nested_value(classification, ["subGenre", "name"]),
        "event_type": get_nested_value(classification, ["type", "name"]),
        "event_subtype": get_nested_value(classification, ["subType", "name"]),
        "family": classification.get("family"),
        "promoter": get_nested_value(event, ["promoter", "name"]),
        "price_min": get_nested_value(event, ["priceRanges"], [{}])[0].get("min")
        if event.get("priceRanges")
        else None,
        "price_max": get_nested_value(event, ["priceRanges"], [{}])[0].get("max")
        if event.get("priceRanges")
        else None,
        "currency": get_nested_value(event, ["priceRanges"], [{}])[0].get("currency")
        if event.get("priceRanges")
        else None,
        "source": "Ticketmaster Discovery API",
    }


def fetch_events():
    if not API_KEY:
        raise ValueError("No se encontro TICKETMASTER_API_KEY en el archivo .env")

    all_events = []
    page = 0
    total_pages = 1

    while page < total_pages:
        params = {
            "apikey": API_KEY,
            "countryCode": "MX",
            "classificationName": "music",
            "size": 200,
            "page": page,
        }

        print(f"Descargando pagina {page + 1} de {total_pages}...")

        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        page_info = data.get("page", {})
        total_pages = page_info.get("totalPages", 1)

        events = data.get("_embedded", {}).get("events", [])
        all_events.extend(events)

        page += 1

    return all_events


def main():
    events = fetch_events()

    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with RAW_DATA_PATH.open("w", encoding="utf-8") as raw_file:
        json.dump(events, raw_file, ensure_ascii=False, indent=2)

    rows = [transform_event(event) for event in events]
    df = pd.DataFrame(rows)

    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df["year"] = df["event_date"].dt.year
    df["month"] = df["event_date"].dt.month
    df["month_name"] = df["event_date"].dt.month_name()
    df["event_count"] = 1
    df["city_clean"] = df["city"].apply(clean_city)
    df["state_clean"] = df["state"].apply(clean_state)
    df["genre_clean"] = df.apply(
        lambda row: clean_genre(row["genre"], row["subgenre"]),
        axis=1,
    )
    df["is_festival"] = df.apply(
        lambda row: detect_festival(row["event_name"], row["event_subtype"]),
        axis=1,
    )
    df["has_price"] = df["price_min"].notna() | df["price_max"].notna()

    df = df.sort_values(by=["event_date", "city", "event_name"])

    df.to_csv(PROCESSED_DATA_PATH, index=False, encoding="utf-8-sig")

    print("\nExtraccion terminada.")
    print(f"Eventos descargados: {len(events)}")
    print(f"Archivo raw: {RAW_DATA_PATH}")
    print(f"Archivo procesado: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    main()