# mapas/data.py

import json
import os
import requests
import time
import pandas as pd
from typing import Optional, Tuple, Dict, List


# ============================================================
# === FUNCIONES BASE (YA EXISTENTES) =========================
# ============================================================

def cargar_y_validar_datos(
    csv_path: str,
    separador: str,
    columna_lat: str,
    columna_lon: str
) -> pd.DataFrame:
    df = pd.read_csv(csv_path, sep=separador, encoding="utf-8")

    df = df[
        df[columna_lat].notna() &
        df[columna_lon].notna() &
        (df[columna_lat] != "") &
        (df[columna_lon] != "")
    ].copy()

    df[columna_lat] = pd.to_numeric(df[columna_lat], errors="coerce")
    df[columna_lon] = pd.to_numeric(df[columna_lon], errors="coerce")

    return df.dropna(subset=[columna_lat, columna_lon])


def calcular_centro(
    df: pd.DataFrame,
    centro: Optional[Tuple[float, float]],
    columna_lat: str,
    columna_lon: str
) -> Tuple[float, float]:
    if centro is None:
        return df[columna_lat].mean(), df[columna_lon].mean()
    return centro


def unir_viviendas(
    df_coords: pd.DataFrame,
    csv_viviendas: str,
    separador: str = ";"
) -> pd.DataFrame:
    df_viv = pd.read_csv(
        csv_viviendas,
        sep=separador,
        encoding="utf-8",
        low_memory=False
    )

    columnas = [
        "id_vivienda",
        "fecha_alta",
        "superficie",
        "plazas",
        "habitaciones"
    ]

    return df_coords.merge(
        df_viv[columnas],
        on="id_vivienda",
        how="left"
    )


# ============================================================
# === MUNICIPIOS: JSON-LD + WIKIDATA =========================
# ============================================================

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"


def _extraer_municipios_desde_jsonld(path_jsonld: str) -> pd.DataFrame:
    """
    Extrae municipios únicos desde viviendas_enriquecidas.jsonld
    sin consultar Wikidata.
    """
    with open(path_jsonld, "r", encoding="utf-8") as f:
        data = json.load(f)

    municipios: Dict[str, Dict] = {}

    for viv in data:
        addr = viv.get("address", {})
        locality = addr.get("addressLocality", {})

        qid_url = locality.get("sameAs")
        if not qid_url:
            continue

        qid = qid_url.rsplit("/", 1)[-1]

        if qid in municipios:
            continue

        municipios[qid] = {
            "qid": qid,
            "nombre": locality.get("name"),
            "codigo_ine": addr.get("identifier", {}).get("value")
        }

    return pd.DataFrame(municipios.values())


def _consultar_wikidata_en_bloque(qids: List[str]) -> Dict[str, Dict]:
    """
    Consulta Wikidata EN BLOQUE para un lote pequeño de QID.
    Devuelve dict: qid -> {lat, lon, poblacion}

    Nota:
    - Evitamos geof:latitude/longitude (a veces provoca 500 en Wikidata).
    - Pedimos P625 como WKT (Point(lon lat)) y lo parseamos en Python.
    - Incluye reintentos básicos ante 429/5xx.
    """
    qids = [q for q in qids if q]
    if not qids:
        return {}

    values = " ".join(f"wd:{qid}" for qid in qids)

    query = f"""
    SELECT ?item ?coord ?poblacion WHERE {{
      VALUES ?item {{ {values} }}
      OPTIONAL {{ ?item wdt:P625 ?coord . }}
      OPTIONAL {{ ?item wdt:P1082 ?poblacion . }}
    }}
    """

    headers = {
        "Accept": "application/sparql+json",
        "User-Agent": "MapaMunicipios-UA/1.0"
    }

    params = {"query": query, "format": "json"}

    last_err = None
    for intento in range(3):
        try:
            r = requests.get(
                WIKIDATA_ENDPOINT,
                params=params,
                headers=headers,
                timeout=60
            )

            if r.status_code in (429, 500, 502, 503, 504):
                last_err = f"HTTP {r.status_code}"
                time.sleep(1.5 * (intento + 1))
                continue

            r.raise_for_status()

            if not r.text.strip():
                return {}

            results = r.json().get("results", {}).get("bindings", [])
            salida: Dict[str, Dict] = {}

            for res in results:
                qid = res["item"]["value"].rsplit("/", 1)[-1]

                lat = None
                lon = None
                if "coord" in res:
                    coord = res["coord"]["value"]  # "Point(lon lat)"
                    if coord.startswith("Point(") and coord.endswith(")"):
                        try:
                            lon_s, lat_s = coord.replace("Point(", "").replace(")", "").split(" ")
                            lon = float(lon_s)
                            lat = float(lat_s)
                        except Exception:
                            lat = None
                            lon = None

                pobl = None
                if "poblacion" in res:
                    try:
                        pobl = int(float(res["poblacion"]["value"]))
                    except Exception:
                        pobl = None

                salida[qid] = {"lat": lat, "lon": lon, "poblacion": pobl}

            return salida

        except Exception as e:
            last_err = str(e)
            time.sleep(1.5 * (intento + 1))

    print(f"⚠️ Wikidata sin respuesta válida para bloque ({len(qids)} qids). Último error: {last_err}")
    return {}


def _chunked(lista: List[str], n: int):
    for i in range(0, len(lista), n):
        yield lista[i:i + n]


def cargar_municipios_desde_jsonld(path_jsonld: str) -> pd.DataFrame:
    """
    Pipeline completo:
    1) Extrae municipios únicos desde JSON-LD
    2) Consulta Wikidata en BLOQUES
    3) Devuelve TODOS los municipios (aunque no tengan lat/lon)
    """
    if not os.path.exists(path_jsonld):
        raise FileNotFoundError(f"❌ No existe el archivo: {path_jsonld}")

    df_mun = _extraer_municipios_desde_jsonld(path_jsonld)

    if df_mun.empty:
        return df_mun

    qids = df_mun["qid"].tolist()
    wikidata_total: Dict[str, Dict] = {}

    # 👇 Bloques más pequeños para evitar 500
    for bloque in _chunked(qids, 10):
        datos = _consultar_wikidata_en_bloque(bloque)
        wikidata_total.update(datos)

    if not wikidata_total:
        return df_mun

    df_wiki = (
        pd.DataFrame.from_dict(wikidata_total, orient="index")
        .reset_index()
        .rename(columns={"index": "qid"})
    )

    df_final = df_mun.merge(df_wiki, on="qid", how="left")
    return df_final
