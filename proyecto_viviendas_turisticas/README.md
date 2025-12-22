# Viviendas Turísticas – Comunidad Valenciana
Proyecto de Adquisición, Preparación y Visualización de Datos

Este repositorio implementa el flujo completo de **descarga, limpieza, normalización, enriquecimiento, geocodificación y visualización** de las viviendas turísticas registradas en la Comunidad Valenciana, utilizando exclusivamente **datos oficiales** de la Generalitat Valenciana y del INE.

---

## Estructura del proyecto

- database/
  - coords_cv.csv
  - info_por_cp.csv
  - info_por_municipio.csv
  - info_por_provincia.csv
  - output_turismoactivo_castellano.csv
  - turismoactivo.csv
  - viviendas_depuradas.csv
  - viviendas_enriquecidas.jsonld
  - viviendas_limpias.csv
  - viviendas_sucias.csv
  - pentaho_job.kjb
  - transformacion_csv_mun_prov.ktr
  - limpieza_viviendas.ktr
- mapas/
  - html/
    - mapa_viviendas_turisticas.html
    - README.md
  - base.py
  - config.py
  - data.py
  - layers.py
  - mapa.py
  - ui.py
  - export.py
  - main.py
- utils/
  - arreglos.py
  - coordenadas.py
  - generador.py
  - Viviendas_turisticas_GVA.ipynb
  - convertir_schema.py
  - generar_mapeo.py
  - mapeo_ine_wikidata.json
  - transformacion_provincia_val_a_cas.py
- modelos/
  - conceptual.drawio
  - conceptual.png
  - fisico.sql
  - logico.jpg
  - logico.mwb
- README.md

---

## Proceso de ejecución del proyecto

### Descarga de datos oficiales

Ejecutar el notebook:

utils/Viviendas_turisticas_GVA.ipynb

Este proceso:
- Descarga los CSV oficiales por municipio desde la GVA
- Unifica todos los ficheros en uno solo

Resultado:
- viviendas_sucias.csv

---

### Limpieza inicial con Pentaho

Ejecutar la **transformación principal de Pentaho Data Integration** limpieza_viviendas.ktr sobre viviendas_sucias.csv.

Acciones realizadas:
- Filtrado de registros erróneos
- Normalización de superficies
- Separación de campos de dirección
- Selección y renombrado de columnas relevantes

Resultado:
- viviendas_depuradas.csv

---

### Normalización administrativa (Python)

Ejecutar:

utils/arreglos.py

Este script:
- Corrige nombres de municipios mediante código oficial
- Asigna provincia a partir del prefijo del código INE
- Normaliza textos y elimina inconsistencias administrativas

Resultado:
- viviendas_limpias.csv

---

### Continuar con la ejecución del job de Pentaho

Ejecutar la **transformación de Pentaho Data Integration** transformacion_csv_mun_prov.ktr sobre viviendas_limpias.csv, ... .

Acciones realizadas:
- ...

Resultados:
- ...

---


### Geocodificación de viviendas

Ejecutar:

utils/generador.py

Proceso:
- Construcción de direcciones completas
- Obtención de latitud y longitud mediante ArcGIS
- Uso de caché para evitar consultas repetidas
- Guardado incremental y reanudable

Resultado:
- coords_cv.csv

---

### Schema

Ejecutar:

...

Proceso:
- ...

Resultado:
- ...

---

### Visualización geográfica

Ejecutar:

mapas/main.py

Este paso genera un **mapa interactivo en HTML** con:
- Mapa de calor de densidad
- Marcadores individuales de viviendas
- Clusters dinámicos
- Capas base intercambiables
- Información municipal enriquecida con Wikidata

El mapa se guarda automáticamente y se abre en el navegador.

---

## Tecnologías utilizadas

- Python (pandas, folium, geopy)
- Pentaho Data Integration
- ArcGIS Geocoding
- Wikidata (SPARQL)
- Leaflet / Folium

---

## Resultado final

Una herramienta reproducible que permite **analizar y visualizar la distribución,concentración y características de la vivienda turística** en la Comunidad Valenciana, facilitando el análisis territorial y la planificación urbana basada en datos oficiales.
