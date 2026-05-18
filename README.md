# Analisis de oferta musical en Mexico con Ticketmaster API

Dashboard en Power BI sobre eventos musicales disponibles en Ticketmaster entre mayo de 2026 y marzo de 2027.

![Vista general del dashboard](docs/screenshots/vista_general.png)

> Nota: este README usa texto sin acentos para evitar problemas de codificacion al visualizar el proyecto en distintos entornos, editores o plataformas.

## Objetivo

Analizar la oferta musical publicada en Ticketmaster Mexico para identificar en que ciudades, venues, meses y generos se concentra la actividad de eventos musicales.

El proyecto busca demostrar un flujo completo de analisis de datos:

- Extraccion de datos desde una API publica.
- Limpieza y normalizacion con Python.
- Preparacion de dataset para Power BI.
- Construccion de dashboard interactivo.
- Comunicacion de hallazgos para portafolio profesional.

## Fuente de datos

Los datos fueron obtenidos desde la Ticketmaster Discovery API v2.

Filtro principal utilizado:

- Pais: Mexico (`countryCode=MX`)
- Clasificacion: musica (`classificationName=music`)

La API devuelve informacion sobre eventos, fechas, venues, ciudades, coordenadas, artistas/atracciones, generos, estatus de venta y promotores.

## Herramientas utilizadas

- Python
- pandas
- requests
- python-dotenv
- Power BI Desktop
- Ticketmaster Discovery API
- VS Code

## Proceso

1. Se creo una cuenta de desarrollador en Ticketmaster para obtener una API key.
2. Se extrajeron eventos musicales de Mexico mediante la Discovery API.
3. Se guardo una version cruda de los datos en formato JSON.
4. Se transformaron los datos en un CSV limpio para analisis.
5. Se normalizaron campos como ciudad, estado, genero y clasificacion de festivales.
6. Se preparo un dataset final optimizado para Power BI.
7. Se construyo un dashboard con dos paginas:
   - Vista General
   - Explorador de Eventos

## Estructura del proyecto

```text
conciertos-festivales-mexico/
  assets/
  data/
    raw/
    processed/
  docs/
    screenshots/
  powerbi/
  scripts/
  themes/
  README.md
  requirements.txt
```

## Scripts principales

```text
scripts/test_ticketmaster_api.py
```

Prueba la conexion con la API de Ticketmaster y muestra una muestra inicial de eventos.

```text
scripts/extract_ticketmaster_events.py
```

Extrae eventos desde la API, guarda el JSON crudo y genera un CSV procesado.

```text
scripts/explore_ticketmaster_data.py
```

Genera un analisis exploratorio inicial del dataset.

```text
scripts/prepare_powerbi_dataset.py
```

Crea una version final del dataset con columnas seleccionadas y nombres amigables para Power BI.

## Dashboard

El dashboard contiene dos paginas principales.

### Vista General

Resume la oferta musical por ciudad, mes, venue, genero y ubicacion geografica.

Incluye:

- Total de eventos
- Total de ciudades
- Total de venues
- Porcentaje de festivales
- Eventos por ciudad
- Eventos por mes
- Top venues
- Generos principales
- Mapa de eventos

![Vista general](docs/screenshots/vista_general.png)

### Explorador de Eventos

Permite consultar eventos especificos usando filtros interactivos.

Incluye:

- Busqueda por artista o atraccion
- Filtros por anio, ciudad, genero, venue, estatus y festival
- KPIs dinamicos
- Tabla detallada de eventos

![Explorador de eventos](docs/screenshots/explorador_eventos.png)

## Principales hallazgos

- Ciudad de Mexico concentra la mayor parte de la oferta musical disponible en Ticketmaster.
- Monterrey y Zapopan aparecen como mercados relevantes despues de Ciudad de Mexico.
- Los generos con mayor presencia son Latin, Pop y Rock.
- Venues como Auditorio Nacional, Teatro Metropolitan, Palacio de los Deportes y Auditorio Telmex concentran un volumen importante de eventos.
- La mayoria de registros corresponden a conciertos o eventos individuales; los festivales representan una proporcion menor del total.

## Calidad y limpieza de datos

Durante el proceso se identificaron algunos retos comunes en datos reales:

- Ciudades con nombres inconsistentes, por ejemplo `Mexico`, `Mexico CDMX` y `Ciudad de Mexico`.
- Generos marcados como `Undefined`.
- Eventos sin coordenadas de latitud/longitud.
- Campos de precio no disponibles en la respuesta de la API.

Para resolverlo se agregaron columnas limpias como:

- `city_clean`
- `state_clean`
- `genre_clean`
- `is_festival`
- `has_price`

## Limitaciones

- La API no entrego precios disponibles para los eventos analizados.
- La clasificacion de festivales es aproximada y se basa en texto del nombre del evento y subtipo.
- El dataset representa eventos disponibles en Ticketmaster al momento de la extraccion.
- Si Ticketmaster agrega o elimina eventos, es necesario volver a ejecutar el script para actualizar el CSV.

## Como reproducir el proyecto

1. Crear un archivo `.env` con la API key:

```text
TICKETMASTER_API_KEY=tu_consumer_key
```

2. Crear y activar entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4. Extraer y procesar datos:

```powershell
python scripts/extract_ticketmaster_events.py
python scripts/prepare_powerbi_dataset.py
```

5. Cargar en Power BI el archivo:

```text
data/processed/ticketmaster_events_powerbi.csv
```

## Proximas mejoras

- Agregar detalle enriquecido por artista.
- Incluir links externos de artistas como Spotify, Instagram o YouTube cuando esten disponibles.
- Crear una pagina de analisis de venues.
- Automatizar la actualizacion del dataset.
- Expandir el analisis a otros paises de Latinoamerica.
