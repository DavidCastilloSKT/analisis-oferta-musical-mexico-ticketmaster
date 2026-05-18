from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "ticketmaster_events_mx_music.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "ticketmaster_events_powerbi.csv"


POWERBI_COLUMNS = [
    "event_name",
    "event_url",
    "event_date",
    "event_time",
    "event_status",
    "artist_or_attraction",
    "venue",
    "city_clean",
    "state_clean",
    "country",
    "latitude",
    "longitude",
    "segment",
    "genre_clean",
    "is_festival",
    "has_price",
    "year",
    "month",
    "month_name",
    "event_count",
    "promoter",
]


def main():
    df = pd.read_csv(INPUT_PATH)

    df_powerbi = df[POWERBI_COLUMNS].copy()

    df_powerbi = df_powerbi.rename(
        columns={
            "event_name": "Evento",
            "event_url": "URL Evento",
            "event_date": "Fecha",
            "event_time": "Hora",
            "event_status": "Estatus",
            "artist_or_attraction": "Artista o Atraccion",
            "venue": "Venue",
            "city_clean": "Ciudad",
            "state_clean": "Estado",
            "country": "Pais",
            "latitude": "Latitud",
            "longitude": "Longitud",
            "segment": "Segmento",
            "genre_clean": "Genero",
            "is_festival": "Es Festival",
            "has_price": "Tiene Precio",
            "year": "Anio",
            "month": "Mes Numero",
            "month_name": "Mes Nombre",
            "event_count": "Conteo Eventos",
            "promoter": "Promotor",
        }
    )

    df_powerbi["Fecha"] = pd.to_datetime(df_powerbi["Fecha"], errors="coerce")
    df_powerbi = df_powerbi.sort_values(by=["Fecha", "Ciudad", "Evento"])

    df_powerbi.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Dataset para Power BI creado correctamente.")
    print(f"Filas: {len(df_powerbi)}")
    print(f"Columnas: {len(df_powerbi.columns)}")
    print(f"Archivo: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()