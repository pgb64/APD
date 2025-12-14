import pandas as pd
import json
import os

# Rutas de archivos
base_dir = os.path.dirname(os.path.abspath(__file__))
path_json_map = os.path.join(base_dir, "mapeo_ine_wikidata.json")
path_csv = os.path.join(base_dir, "..", "database", "viviendas_limpias.csv")
path_salida = os.path.join(base_dir, "..", "database", "viviendas_enriquecidas.jsonld")

# Cargar el mapeo
try:
    with open(path_json_map, "r", encoding="utf-8") as f:
        wikidata_map = json.load(f)
    print("Mapeo de Wikidata cargado")
except FileNotFoundError:
    wikidata_map = {}
    print(f"ADVERTENCIA: No se encontró '{path_json_map}'. Ejecuta 'generar_mapeo.py' primero.")

# Cargar CSV
try:
    df = pd.read_csv(path_csv, sep=";", dtype=str)
    print(f"CSV cargado correctamente ")
except FileNotFoundError:
    print(f"ERROR: No se encuentra el archivo CSV")
    exit()

def crear_direccion(row):
    partes = [str(row["calle"])] 
    if pd.notna(row["escalera"]) and str(row["escalera"]).strip():
        partes.append(f"Escalera {row['escalera']}")
    if pd.notna(row["planta"]) and str(row["planta"]).strip():
        partes.append(f"Planta {row['planta']}")
    if pd.notna(row["puerta"]) and str(row["puerta"]).strip():
        partes.append(f"Puerta {row['puerta']}")
    return ", ".join(partes)

def safe_int(value):
    if pd.isna(value): return None
    try: return int(float(value))
    except: return None

def safe_float(value):
    if pd.isna(value): return None
    try: return float(value)
    except: return None

salida = []

for _, row in df.iterrows():
    
    municipio_nombre = row["municipio"]
    codigo_ine = row["num_municipio"].strip() if pd.notna(row["num_municipio"]) else None
    
    localidad_obj = {
        "@type": "Place",
        "name": municipio_nombre
    }
    
    if codigo_ine and codigo_ine in wikidata_map:
        localidad_obj["sameAs"] = wikidata_map[codigo_ine]

    direccion = {
        "@type": "PostalAddress",
        "streetAddress": crear_direccion(row),
        "addressLocality": localidad_obj,
        "addressRegion": row["provincia"],
        "postalCode": row["cp"].strip() if pd.notna(row["cp"]) else None
    }

    if codigo_ine:
        direccion["identifier"] = {
            "@type": "PropertyValue",
            "name": "INE Municipality Code",
            "value": codigo_ine
        }

    entrada = {
        "@context": "https://schema.org",
        "@type": "TouristApartment",
        "@id": f"https://example.org/vivienda/{row['id_vivienda']}",
        "name": row["id_vivienda"],
        "dateCreated": row["fecha_alta"],
        "address": direccion
    }

    habitaciones = safe_int(row["habitaciones"])
    if habitaciones is not None:
        entrada["numberOfRooms"] = habitaciones

    plazas = safe_int(row["plazas"])
    if plazas is not None:
        entrada["occupancy"] = {
            "@type": "QuantitativeValue",
            "value": plazas
        }

    superficie = safe_float(row["superficie"])
    if superficie is not None:
        entrada["floorSize"] = {
            "@type": "QuantitativeValue",
            "value": superficie,
            "unitText": "m2"
        }

    salida.append(entrada)

# Guardar JSON-LD
with open(path_salida, "w", encoding="utf-8") as f:
    json.dump(salida, f, ensure_ascii=False, indent=2)

print(f"Se han generado {len(salida)} registros enriquecidos")