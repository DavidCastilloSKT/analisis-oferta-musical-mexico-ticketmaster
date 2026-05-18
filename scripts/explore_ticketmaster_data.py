from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "ticketmaster_events_mx_music.csv"


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main():
    df = pd.read_csv(DATA_PATH)

    print_section("Resumen general")
    print(f"Filas: {len(df)}")
    print(f"Columnas: {len(df.columns)}")
    print(f"Periodo: {df['event_date'].min()} a {df['event_date'].max()}")

    print_section("Calidad de datos")
    selected_columns = [
        "event_name",
        "event_date",
        "city_clean",
        "state_clean",
        "venue",
        "genre_clean",
        "latitude",
        "longitude",
        "price_min",
        "price_max",
    ]

    missing_values = df[selected_columns].isna().sum().sort_values(ascending=False)
    print(missing_values)

    print_section("Top 10 ciudades por numero de eventos")
    print(df["city_clean"].value_counts().head(10))

    print_section("Top 10 venues por numero de eventos")
    print(df["venue"].value_counts().head(10))

    print_section("Eventos por mes")
    events_by_month = (
        df.groupby(["year", "month", "month_name"])
        .size()
        .reset_index(name="events")
        .sort_values(["year", "month"])
    )
    print(events_by_month)

    print_section("Top generos")
    print(df["genre_clean"].value_counts().head(10))

    print_section("Festivales vs no festivales")
    print(df["is_festival"].value_counts())
    print(df["is_festival"].value_counts(normalize=True).mul(100).round(2))

    print_section("Eventos con precio disponible")
    print(df["has_price"].value_counts())
    print(df["has_price"].value_counts(normalize=True).mul(100).round(2))

    print_section("Paises detectados")
    print(df["country"].value_counts(dropna=False))


if __name__ == "__main__":
    main()