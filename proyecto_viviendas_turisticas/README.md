# Viviendas Turísticas – Comunidad Valenciana
Proyecto de Adquisición, Preparación y Visualización de Datos

Este repositorio implementa el flujo completo de **descarga, limpieza, normalización, enriquecimiento, geocodificación y visualización** de las viviendas turísticas registradas en la Comunidad Valenciana, utilizando exclusivamente **datos oficiales** de la Generalitat Valenciana y del INE.

**IMPORTANTE!**
Hay que ejecutar los códigos, estando dentro de la carpeta proyecto_viviendas_turisticas/

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

### Normalización

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

Ejecutar el script de python utils/transformacion_provincia_val_a_cas.py.
Ejecutar la **transformación de Pentaho Data Integration** transformacion_csv_mun_prov.ktr sobre viviendas_limpias.csv y output_turismoactivo_castellano.csv.

Acciones realizadas:
- Mapeo de comunidades de valenciano a castellano del archivo turismoactivo
- Agrupación de campos por CP, municipio y provincia respectivamente
- Realización de operaciones para obtener métricas de contexto
- Filtrado de columnas final

Resultados:
- info_por_cp.csv
- info_por_municipio.csv
- info_por_provincia.csv

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

### Mapeo de Schema

Ejecutar:

utils/generar_mapeo.py

Resultado:

mapeo_ine_wikidata.json


---

## Archivo de viviendas Schema

Ejecutar:

utils/convertir_schema.py

Resultado:

viviendas_enriquecidas.jsonld


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

Una herramienta reproducible que permite **analizar y visualizar la distribución, concentración y características de la vivienda turística** en la Comunidad Valenciana, facilitando el análisis territorial y la planificación urbana basada en datos oficiales.

---

## Licencia de uso

Este proyecto se distribuye bajo la licencia:

Creative Commons Atribución–NoComercial–CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)

Esta licencia permite:
- Compartir: copiar y redistribuir el material en cualquier medio o formato.
- Adaptar: remezclar, transformar y construir a partir del material.

Bajo las siguientes condiciones:
- Atribución: se debe reconocer adecuadamente la autoría del trabajo.
- No Comercial: no se permite el uso del material con fines comerciales.
- Compartir Igual: las obras derivadas deben distribuirse bajo la misma licencia.

Texto legal completo disponible en:
https://creativecommons.org/licenses/by-nc-sa/4.0/

---

## Referencias y fuentes de datos

Las principales fuentes y herramientas utilizadas para la realización del proyecto son:

- Generalitat Valenciana – Turisme Comunitat Valenciana  
  Registro Oficial de Viviendas Turísticas  
  https://www.gva.es  

- Instituto Nacional de Estadística (INE)  
  Códigos oficiales de municipios y provincias  
  https://www.ine.es  

- Wikidata  
  Enriquecimiento semántico y datos geográficos de municipios  
  https://www.wikidata.org  

- Schema.org  
  Modelo semántico utilizado para la representación de viviendas turísticas  
  https://schema.org/TouristApartment  

- ArcGIS Geocoding Service  
  Servicio de geocodificación de direcciones  
  https://developers.arcgis.com  

- Pentaho Data Integration  
  Herramienta ETL para limpieza y agregación de datos  
  https://www.pentaho.com  

- Folium / Leaflet  
  Librerías de visualización cartográfica interactiva  
  https://python-visualization.github.io/folium/  

---

## Nota académica

Este proyecto ha sido desarrollado con fines exclusivamente académicos, en el marco de la asignatura **Adquisición y Preparación de Datos** del **Grado en Ingeniería en Inteligencia Artificial** de la **Universidad de Alicante**.

Los datos empleados son de carácter público y oficial, y su tratamiento se ha realizado siguiendo criterios de calidad, reproducibilidad y uso responsable de la información.



