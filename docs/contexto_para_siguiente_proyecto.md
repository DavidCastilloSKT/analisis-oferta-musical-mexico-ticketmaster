# Contexto para siguiente proyecto de portafolio Data Analytics

Este archivo resume el proceso seguido para construir el proyecto **Analisis de oferta musical en Mexico con Ticketmaster API**. Su objetivo es servir como contexto inicial para un nuevo chat y replicar el mismo flujo con otro dataset, industria o tema.

## Objetivo general del portafolio

Construir un portafolio profesional de Data Analytics con proyectos completos, no solo dashboards aislados.

Cada proyecto debe demostrar:

- Eleccion de una pregunta de negocio o analisis.
- Obtencion de datos.
- Limpieza y transformacion.
- Analisis exploratorio.
- Dashboard en Power BI.
- Documentacion en GitHub.
- Caso de estudio visual en Notion.
- Publicacion en LinkedIn.

## Proyecto completado

**Titulo:** Analisis de oferta musical en Mexico con Ticketmaster API

**Industria:** entretenimiento / musica / eventos

**Pregunta principal:**

En que ciudades, venues, meses y generos se concentra la oferta musical disponible en Ticketmaster Mexico?

**Periodo analizado:** mayo de 2026 a marzo de 2027

**Fuente de datos:** Ticketmaster Discovery API v2

**Herramientas usadas:**

- Python
- pandas
- requests
- python-dotenv
- Power BI Desktop
- GitHub
- Notion
- LinkedIn
- VS Code

## Flujo completo seguido

### 1. Definicion del proyecto

Se eligio un tema atractivo para portafolio: eventos musicales en Mexico.

Se definio que el proyecto debia mostrar:

- Eventos por ciudad.
- Eventos por mes.
- Top venues.
- Generos principales.
- Mapa de eventos.
- Explorador de eventos.

### 2. Obtencion de API key

Se creo una cuenta en Ticketmaster Developer.

Se obtuvo el `Consumer Key`, usado como API key.

La API key se guardo en un archivo `.env`, nunca directamente en el codigo.

Ejemplo:

```text
TICKETMASTER_API_KEY=tu_consumer_key
```

Tambien se creo:

```text
.env.example
```

con una plantilla sin secretos.

### 3. Estructura del proyecto

Se creo una carpeta de proyecto con esta estructura:

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
  .env
  .env.example
  .gitignore
  README.md
  requirements.txt
```

### 4. Entorno de Python

Se creo un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se instalaron librerias:

```powershell
pip install requests python-dotenv pandas
```

Se genero:

```powershell
pip freeze > requirements.txt
```

### 5. Scripts creados

Se crearon estos scripts:

```text
scripts/test_ticketmaster_api.py
```

Prueba conexion con la API.

```text
scripts/extract_ticketmaster_events.py
```

Extrae datos desde la API, guarda JSON crudo y genera CSV procesado.

```text
scripts/explore_ticketmaster_data.py
```

Realiza analisis exploratorio inicial.

```text
scripts/prepare_powerbi_dataset.py
```

Genera el CSV final para Power BI con columnas seleccionadas y nombres amigables.

### 6. Dataset generado

Se obtuvieron 719 eventos y 36 columnas en el dataset procesado.

Archivos generados:

```text
data/raw/ticketmaster_events_raw.json
data/processed/ticketmaster_events_mx_music.csv
data/processed/ticketmaster_events_powerbi.csv
```

`data/raw/` se excluyo de GitHub.

El archivo usado por Power BI fue:

```text
data/processed/ticketmaster_events_powerbi.csv
```

### 7. Limpieza y normalizacion

Se detectaron problemas de calidad de datos:

- Ciudades inconsistentes: `Mexico`, `Mexico CDMX`, `Ciudad de Mexico`.
- Generos `Undefined`.
- Eventos sin coordenadas.
- Precios no disponibles en la API.

Se crearon columnas limpias:

```text
city_clean
state_clean
genre_clean
is_festival
has_price
```

### 8. Analisis exploratorio

Se revisaron:

- Total de filas y columnas.
- Periodo de fechas.
- Nulos por columna.
- Top ciudades.
- Top venues.
- Eventos por mes.
- Top generos.
- Porcentaje de festivales.
- Disponibilidad de precios.
- Paises detectados.

Hallazgos principales:

- Ciudad de Mexico concentra la mayor parte de eventos.
- Monterrey y Zapopan aparecen como mercados relevantes.
- Latin, Pop y Rock son los generos con mayor presencia.
- Auditorio Nacional, Teatro Metropolitan, Palacio de los Deportes y Auditorio Telmex destacan entre venues.
- Los festivales representan una proporcion menor.

### 9. Dashboard en Power BI

Se creo un archivo `.pbix` guardado localmente en:

```text
powerbi/dashboard_oferta_musical_mexico_ticketmaster.pbix
```

No se subio a GitHub por estar ignorado en `.gitignore`.

Paginas del dashboard:

#### Vista General

Incluye:

- KPIs:
  - Total Eventos
  - Total Ciudades
  - Total Venues
  - % Festivales
- Eventos por ciudad.
- Eventos por mes.
- Top venues.
- Generos principales.
- Azure Maps.
- Segmentadores.
- Boton para limpiar filtros.

#### Explorador de Eventos

Incluye:

- Buscador/filtro principal de Artista o Atraccion.
- Filtros por:
  - Anio
  - Ciudad
  - Genero
  - Es Festival
  - Estatus
  - Venue
- KPIs dinamicos.
- Tabla detallada de eventos.
- Boton para limpiar filtros.

### 10. Tema visual de Power BI

Se creo una carpeta:

```text
themes/
```

Con temas `.json`:

```text
oferta_musical_mexico_theme.json
oferta_musical_mexico_theme_v2.json
```

Paleta principal:

```text
Fondo general:    #F6F7FB
Tarjetas:         #FFFFFF
Texto principal:  #1F2937
Texto secundario: #6B7280
Bordes suaves:    #E5E7EB
Morado principal: #6D5BD0
Azul acento:      #2563EB
Naranja festival: #F59E0B
Verde acento:     #10B981
Rojo alerta:      #EF4444
```

### 11. Capturas

Se crearon capturas para documentacion:

```text
docs/screenshots/vista_general.png
docs/screenshots/explorador_eventos.png
```

### 12. README

Se creo un README profesional con:

- Objetivo.
- Fuente de datos.
- Herramientas.
- Proceso.
- Estructura del proyecto.
- Scripts principales.
- Capturas.
- Hallazgos.
- Calidad de datos.
- Limitaciones.
- Como reproducir el proyecto.
- Proximas mejoras.

Nota: el README se dejo sin acentos para evitar problemas de codificacion en distintos entornos.

### 13. GitHub

Se creo un repositorio publico:

```text
analisis-oferta-musical-mexico-ticketmaster
```

URL:

```text
https://github.com/DavidCastilloSKT/analisis-oferta-musical-mexico-ticketmaster
```

Se configuro `.gitignore` para excluir:

```text
.env
.venv/
data/raw/
powerbi/
__pycache__/
*.pyc
*.pyo
*.pbix
.DS_Store
Thumbs.db
```

Se subieron:

- README.
- Scripts.
- Datasets procesados.
- Capturas.
- Temas.
- Iconos.
- Archivo `.env.example`.

### 14. LinkedIn

Se publico un post con:

- Descripcion del proyecto.
- Herramientas usadas.
- Hallazgos principales.
- Link a GitHub.
- Capturas del dashboard.

Tambien se agrego el proyecto a la seccion **Destacado** del perfil usando el link publico de Notion.

### 15. Notion

Se creo una pagina de caso de estudio en Notion.

URL publica:

```text
https://wild-wealth-3d3.notion.site/An-lisis-de-oferta-musical-en-M-xico-con-Ticketmaster-API-364f0cff1eb9805894eed9ee2d682e37
```

Se creo el archivo:

```text
docs/portfolio_case_study.md
```

con una version resumida y visual del proyecto para Notion.

### 16. LinkedIn About

Se actualizo la seccion **Acerca de** del perfil con una descripcion orientada a Data Analytics y Business Intelligence.

## Patron para replicar en el siguiente proyecto

Para un nuevo proyecto, seguir este flujo:

1. Elegir industria y pregunta principal.
2. Identificar fuente de datos.
3. Crear estructura del proyecto.
4. Configurar entorno Python.
5. Crear script de extraccion.
6. Guardar datos crudos.
7. Limpiar y transformar.
8. Crear dataset final para Power BI.
9. Hacer analisis exploratorio.
10. Construir dashboard:
    - Vista General.
    - Explorador o Detalle.
11. Crear tema visual.
12. Tomar capturas.
13. Crear README.
14. Subir a GitHub.
15. Crear caso de estudio en Notion.
16. Publicar en LinkedIn.
17. Agregar a Destacado en LinkedIn.

## Recomendaciones para el siguiente proyecto

Mantener la misma estructura:

```text
nombre-del-proyecto/
  assets/
  data/
    raw/
    processed/
  docs/
    screenshots/
  powerbi/
  scripts/
  themes/
  .env.example
  .gitignore
  README.md
  requirements.txt
```

Crear siempre:

- Un README profesional.
- Un archivo `portfolio_case_study.md`.
- Un post de LinkedIn.
- Capturas del dashboard.
- Un `.gitignore` antes de subir a GitHub.

## Posibles proyectos siguientes

Opciones sugeridas:

1. Turismo en Mexico con datos de DataTur o INEGI.
2. Cerveza artesanal usando datos simulados o internos anonimizados.
3. Comparativo de oferta musical en Latinoamerica.
4. Analisis de ocupacion hotelera por estado.
5. Dashboard de consumo/ventas para una industria especifica.

## Instruccion para nuevo chat

Al iniciar el nuevo chat, compartir este archivo y pedir:

```text
Quiero iniciar un nuevo proyecto de portafolio de Data Analytics siguiendo el mismo proceso documentado en este archivo. Ayudame paso a paso, sin avanzar al siguiente paso hasta que confirme que termine el anterior.
```
