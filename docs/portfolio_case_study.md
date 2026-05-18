# Analisis de oferta musical en Mexico con Ticketmaster API

## Resumen

Proyecto de Data Analytics enfocado en analizar la oferta musical publicada en Ticketmaster Mexico entre mayo de 2026 y marzo de 2027.

El proyecto incluye extraccion de datos desde una API publica, limpieza con Python, preparacion de datasets y construccion de un dashboard interactivo en Power BI.

## Pregunta principal

En que ciudades, venues, meses y generos se concentra la oferta musical disponible en Ticketmaster Mexico?

## Herramientas

- Python
- pandas
- requests
- python-dotenv
- Ticketmaster Discovery API
- Power BI
- GitHub
- VS Code

## Proceso

1. Obtencion de API key desde Ticketmaster Developer.
2. Extraccion de eventos musicales usando la Ticketmaster Discovery API.
3. Limpieza y normalizacion de datos con Python.
4. Creacion de un dataset final para Power BI.
5. Construccion de dashboard con dos paginas:
   - Vista General
   - Explorador de Eventos
6. Documentacion del proyecto en GitHub.

## Dashboard

### Vista General

Vista ejecutiva para analizar rapidamente:

- Total de eventos
- Ciudades con mayor oferta musical
- Eventos por mes
- Top venues
- Generos principales
- Distribucion geografica de eventos

![Vista general](screenshots/vista_general.png)

### Explorador de Eventos

Vista de consulta para filtrar eventos por:

- Artista o atraccion
- Anio
- Ciudad
- Genero
- Venue
- Estatus
- Festival

![Explorador de eventos](screenshots/explorador_eventos.png)

## Hallazgos clave

- Ciudad de Mexico concentra la mayor parte de la oferta musical registrada.
- Monterrey y Zapopan aparecen como mercados relevantes despues de Ciudad de Mexico.
- Latin, Pop y Rock son los generos con mayor presencia.
- Auditorio Nacional, Teatro Metropolitan, Palacio de los Deportes y Auditorio Telmex destacan entre los venues con mayor actividad.
- Los festivales representan una proporcion menor frente a conciertos y eventos individuales.

## Limpieza de datos

Durante el analisis se detectaron inconsistencias tipicas de datos reales:

- Variaciones en nombres de ciudad.
- Generos sin clasificar.
- Registros sin coordenadas.
- Campos de precio no disponibles en la API.

Para mejorar el analisis se crearon campos normalizados:

- `city_clean`
- `state_clean`
- `genre_clean`
- `is_festival`
- `has_price`

## Aprendizajes

Este proyecto me permitio practicar un flujo completo de trabajo:

```text
API -> Python -> CSV limpio -> Power BI -> Storytelling -> GitHub
```

Tambien reforzo habilidades de:

- Consumo de APIs.
- Limpieza de datos.
- Modelado simple para dashboard.
- Visualizacion de datos.
- Documentacion de proyectos.
- Publicacion de portafolio profesional.

## Links

- GitHub: https://github.com/DavidCastilloSKT/analisis-oferta-musical-mexico-ticketmaster
- Fuente de datos: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/

## Proximas mejoras

- Enriquecer datos por artista con links externos como Spotify, Instagram y YouTube.
- Crear una pagina dedicada al analisis de venues.
- Automatizar actualizaciones del dataset.
- Expandir el analisis a paises de Latinoamerica.
