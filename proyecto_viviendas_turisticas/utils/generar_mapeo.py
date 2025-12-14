# script_generar_mapeo.py
import json
import os
from SPARQLWrapper import SPARQLWrapper, JSON

def obtener_mapeo_wikidata():
    #
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_salida = os.path.join(base_dir, "mapeo_ine_wikidata.json")

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    # Consulta: Dame todos los municipios (Q2074737) de la Com. Valenciana (Q5720) 
    # con su URL y su código INE (P772)
    query = """
    SELECT ?item ?ine WHERE {
      ?item wdt:P31 wd:Q2074737;       # Es un municipio
            wdt:P131* wd:Q5720;        # Está en Comunidad Valenciana (recursivo)
            wdt:P772 ?ine.             # Tiene código INE
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    print("Consultando a Wikidata...")
    results = sparql.query().convert()

    mapeo = {}
    for result in results["results"]["bindings"]:
        ine = result["ine"]["value"]
        url_wikidata = result["item"]["value"]
        mapeo[ine] = url_wikidata

    # Guardar el mapeo en un archivo JSON
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(mapeo, f)
    
    print(f"Se han mapeado {len(mapeo)} municipios. Archivo guardado.")

if __name__ == "__main__":
    obtener_mapeo_wikidata()