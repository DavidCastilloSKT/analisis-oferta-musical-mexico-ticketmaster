import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "ticketmaster_events_latam_raw.json"

ENRICHED_DATA_DIR = PROJECT_ROOT / "data" / "processed" / "enriched_latam"

FACT_EVENTS_PATH = ENRICHED_DATA_DIR / "fact_events.csv"
DIM_VENUES_PATH = ENRICHED_DATA_DIR / "dim_venues.csv"
DIM_ATTRACTIONS_PATH = ENRICHED_DATA_DIR / "dim_attractions.csv"
BRIDGE_EVENT_ATTRACTIONS_PATH = ENRICHED_DATA_DIR / "bridge_event_attractions.csv"


def get_nested_value(data, keys, default=None):
    current_value = data

    for key in keys:
        if not isinstance(current_value, dict):
            return default

        current_value = current_value.get(key)

        if current_value is None:
            return default

    return current_value


def load_raw_events():
    with RAW_DATA_PATH.open("r", encoding="utf-8") as raw_file:
        return json.load(raw_file)


def select_best_image_url(images):
    if not images:
        return None

    sorted_images = sorted(
        images,
        key=lambda image: image.get("width", 0),
        reverse=True,
    )

    return sorted_images[0].get("url")


def extract_external_link(external_links, platform):
    links = external_links.get(platform, [])

    if not links:
        return None

    return links[0].get("url")


def get_primary_classification(event):
    classifications = event.get("classifications", [])

    if not classifications:
        return {}

    for classification in classifications:
        if classification.get("primary"):
            return classification

    return classifications[0]


def detect_festival(event_name, event_subtype):
    text = f"{event_name or ''} {event_subtype or ''}".lower()
    return "festival" in text or "fest" in text


def detect_suspicious_event(event, venue):
    event_name = (event.get("name") or "").lower()
    venue_name = (venue.get("name") or "").lower()
    city_name = (get_nested_value(venue, ["city", "name"]) or "").lower()
    event_date = get_nested_value(event, ["dates", "start", "localDate"])

    suspicious_keywords = ["test", "teste"]
    suspicious_names = ["novenue", "nocity"]

    has_test_keyword = any(keyword in event_name for keyword in suspicious_keywords)
    has_placeholder_venue = venue_name in suspicious_names
    has_placeholder_city = city_name in suspicious_names
    has_extreme_future_date = event_date is not None and event_date > "2028-12-31"

    return (
        has_test_keyword
        or has_placeholder_venue
        or has_placeholder_city
        or has_extreme_future_date
    )


def get_first_venue(event):
    venues = get_nested_value(event, ["_embedded", "venues"], [])

    if not venues:
        return {}

    return venues[0]


def transform_event(event):
    venue = get_first_venue(event)
    classification = get_primary_classification(event)

    return {
        "event_id": event.get("id"),
        "event_key": (
            f"{event.get('query_country_code')}|"
            f"{event.get('id')}|"
            f"{venue.get('id')}|"
            f"{get_nested_value(event, ['dates', 'start', 'localDate'])}"
        ),
        "event_name": event.get("name"),
        "event_url": event.get("url"),
        "event_date": get_nested_value(event, ["dates", "start", "localDate"]),
        "event_time": get_nested_value(event, ["dates", "start", "localTime"]),
        "event_timezone": get_nested_value(event, ["dates", "timezone"]),
        "event_status": get_nested_value(event, ["dates", "status", "code"]),
        "event_info": event.get("info"),
        "event_notes": event.get("pleaseNote"),
        "event_image_url": select_best_image_url(event.get("images", [])),
        "seatmap_url": get_nested_value(event, ["seatmap", "staticUrl"]),
        "sales_start": get_nested_value(event, ["sales", "public", "startDateTime"]),
        "sales_end": get_nested_value(event, ["sales", "public", "endDateTime"]),
        "ticket_limit_info": get_nested_value(event, ["ticketLimit", "info"]),
        "legal_age_enforced": get_nested_value(event, ["ageRestrictions", "legalAgeEnforced"]),
        "safe_tix_enabled": get_nested_value(event, ["ticketing", "safeTix", "enabled"]),
        "all_inclusive_pricing": get_nested_value(
            event,
            ["ticketing", "allInclusivePricing", "enabled"],
        ),
        "query_country_code": event.get("query_country_code"),
        "venue_id": venue.get("id"),
        "venue_key": f"{event.get('query_country_code')}|{venue.get('id')}",
        "venue_name": venue.get("name"),
        "segment": get_nested_value(classification, ["segment", "name"]),
        "genre": get_nested_value(classification, ["genre", "name"]),
        "subgenre": get_nested_value(classification, ["subGenre", "name"]),
        "event_type": get_nested_value(classification, ["type", "name"]),
        "event_subtype": get_nested_value(classification, ["subType", "name"]),
        "is_family_event": classification.get("family"),
        "is_festival": detect_festival(
            event.get("name"),
            get_nested_value(classification, ["subType", "name"]),
        ),
        "promoter": get_nested_value(event, ["promoter", "name"]),
        "is_test": event.get("test"),
        "is_suspicious_event": detect_suspicious_event(event, venue),
    }


def transform_venue(event):
    venue = get_first_venue(event)

    return {
        "query_country_code": event.get("query_country_code"),
        "venue_id": venue.get("id"),
        "venue_key": f"{event.get('query_country_code')}|{venue.get('id')}",
        "venue_name": venue.get("name"),
        "venue_url": venue.get("url"),
        "venue_image_url": select_best_image_url(venue.get("images", [])),
        "postal_code": venue.get("postalCode"),
        "city": get_nested_value(venue, ["city", "name"]),
        "admin_area": get_nested_value(venue, ["state", "name"]),
        "admin_area_code": get_nested_value(venue, ["state", "stateCode"]),
        "country": get_nested_value(venue, ["country", "name"]),
        "country_code": get_nested_value(venue, ["country", "countryCode"]),
        "address_line_1": get_nested_value(venue, ["address", "line1"]),
        "address_line_2": get_nested_value(venue, ["address", "line2"]),
        "latitude": get_nested_value(venue, ["location", "latitude"]),
        "longitude": get_nested_value(venue, ["location", "longitude"]),
        "parking_detail": venue.get("parkingDetail"),
        "accessible_seating_detail": venue.get("accessibleSeatingDetail"),
        "box_office_phone": get_nested_value(venue, ["boxOfficeInfo", "phoneNumberDetail"]),
        "box_office_hours": get_nested_value(venue, ["boxOfficeInfo", "openHoursDetail"]),
        "accepted_payment_detail": get_nested_value(
            venue,
            ["boxOfficeInfo", "acceptedPaymentDetail"],
        ),
        "will_call_detail": get_nested_value(venue, ["boxOfficeInfo", "willCallDetail"]),
        "general_rule": get_nested_value(venue, ["generalInfo", "generalRule"]),
        "child_rule": get_nested_value(venue, ["generalInfo", "childRule"]),
        "venue_upcoming_events": get_nested_value(venue, ["upcomingEvents", "_total"]),
    }


def transform_attraction(attraction):
    external_links = attraction.get("externalLinks", {})
    classification = get_primary_classification(attraction)

    return {
        "attraction_id": attraction.get("id"),
        "attraction_key": f"{attraction.get('id')}|{attraction.get('url')}",
        "attraction_name": attraction.get("name"),
        "attraction_type": attraction.get("type"),
        "attraction_url": attraction.get("url"),
        "attraction_image_url": select_best_image_url(attraction.get("images", [])),
        "spotify_url": extract_external_link(external_links, "spotify"),
        "instagram_url": extract_external_link(external_links, "instagram"),
        "youtube_url": extract_external_link(external_links, "youtube"),
        "facebook_url": extract_external_link(external_links, "facebook"),
        "homepage_url": extract_external_link(external_links, "homepage"),
        "twitter_url": extract_external_link(external_links, "twitter"),
        "itunes_url": extract_external_link(external_links, "itunes"),
        "wiki_url": extract_external_link(external_links, "wiki"),
        "lastfm_url": extract_external_link(external_links, "lastfm"),
        "musicbrainz_url": extract_external_link(external_links, "musicbrainz"),
        "segment": get_nested_value(classification, ["segment", "name"]),
        "genre": get_nested_value(classification, ["genre", "name"]),
        "subgenre": get_nested_value(classification, ["subGenre", "name"]),
        "attraction_upcoming_events": get_nested_value(attraction, ["upcomingEvents", "_total"]),
    }


def build_event_attraction_rows(event):
    event_id = event.get("id")
    venue = get_first_venue(event)
    attractions = get_nested_value(event, ["_embedded", "attractions"], [])

    rows = []

    for attraction in attractions:
        rows.append(
            {
                "event_id": event_id,
                "event_key": (
                    f"{event.get('query_country_code')}|"
                    f"{event_id}|"
                    f"{venue.get('id')}|"
                    f"{get_nested_value(event, ['dates', 'start', 'localDate'])}"
                ),
                "attraction_id": attraction.get("id"),
                "attraction_key": f"{attraction.get('id')}|{attraction.get('url')}",
            }
        )

    return rows


def main():
    events = load_raw_events()

    event_rows = []
    venue_rows = []
    attraction_rows = []
    event_attraction_rows = []

    for event in events:
        event_rows.append(transform_event(event))
        venue_rows.append(transform_venue(event))
        event_attraction_rows.extend(build_event_attraction_rows(event))

        attractions = get_nested_value(event, ["_embedded", "attractions"], [])

        for attraction in attractions:
            attraction_rows.append(transform_attraction(attraction))

    fact_events_df = pd.DataFrame(event_rows)
    dim_venues_df = pd.DataFrame(venue_rows)
    dim_attractions_df = pd.DataFrame(attraction_rows)
    bridge_event_attractions_df = pd.DataFrame(event_attraction_rows)

    fact_events_df = fact_events_df.drop_duplicates(subset=["event_key"])
    dim_venues_df = dim_venues_df.drop_duplicates(subset=["venue_key"])
    dim_attractions_df = dim_attractions_df.drop_duplicates(subset=["attraction_key"])
    bridge_event_attractions_df = bridge_event_attractions_df.drop_duplicates()

    fact_events_df["event_date"] = pd.to_datetime(
        fact_events_df["event_date"],
        errors="coerce",
    )
    fact_events_df["year"] = fact_events_df["event_date"].dt.year
    fact_events_df["month"] = fact_events_df["event_date"].dt.month
    fact_events_df["month_name"] = fact_events_df["event_date"].dt.month_name()
    fact_events_df["event_count"] = 1

    ENRICHED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    fact_events_df.to_csv(FACT_EVENTS_PATH, index=False, encoding="utf-8-sig")
    dim_venues_df.to_csv(DIM_VENUES_PATH, index=False, encoding="utf-8-sig")
    dim_attractions_df.to_csv(DIM_ATTRACTIONS_PATH, index=False, encoding="utf-8-sig")
    bridge_event_attractions_df.to_csv(
        BRIDGE_EVENT_ATTRACTIONS_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("Modelo enriquecido LATAM creado correctamente.")
    print(f"Eventos: {len(fact_events_df)}")
    print(f"Venues: {len(dim_venues_df)}")
    print(f"Atracciones: {len(dim_attractions_df)}")
    print(f"Relaciones evento-atraccion: {len(bridge_event_attractions_df)}")
    print(f"Carpeta de salida: {ENRICHED_DATA_DIR}")

if __name__ == "__main__":
    main()