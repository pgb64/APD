import pandas as pd
import os
import time
from coordenadas import Coordenadas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "..", "database")

PATH_IN = os.path.join(DATABASE_DIR, "viviendas_limpias.csv")
PATH_OUT = os.path.join(DATABASE_DIR, "coords_cv.csv")

SAVE_INTERVAL = 50

def generar_coords():
    df = pd.read_csv(PATH_IN, sep=";", encoding="utf-8")

    total = len(df)
    geo = Coordenadas()

    # Reanudar si existe
    if os.path.exists(PATH_OUT):
        df_existente = pd.read_csv(PATH_OUT, sep=";", encoding="utf-8")
        procesadas = set(df_existente["id_vivienda"].astype(str))
    else:
        df_existente = pd.DataFrame(columns=["id_vivienda", "latitud", "longitud"])
        procesadas = set()

    nuevas = []
    cache = {}

    for idx, row in df.iterrows():

        print(f"Procesando {idx+1} / {total}")

        id_viv = str(row["id_vivienda"])
        if id_viv in procesadas:
            continue

        calle = str(row["calle"]).strip()
        municipio = str(row["municipio"]).strip()
        cp = str(row["cp"]).strip()
        provincia = str(row["provincia"]).strip()

        direccion = f"{calle}, {cp} {municipio}, {provincia}, España"

        if direccion in cache:
            lat, lon = cache[direccion]
        else:
            coords = geo.obtener_coords(direccion)
            if coords is None:
                lat, lon = "", ""
            else:
                lat, lon = coords

            cache[direccion] = (lat, lon)

        nuevas.append({
            "id_vivienda": id_viv,
            "latitud": lat,
            "longitud": lon
        })

        time.sleep(1)

        # autosave cada 50
        if len(nuevas) % SAVE_INTERVAL == 0:
            temp = pd.concat([df_existente, pd.DataFrame(nuevas)], ignore_index=True)
            temp = temp.drop_duplicates(subset="id_vivienda", keep="last")

            orden = df["id_vivienda"].astype(str)
            temp = temp.set_index("id_vivienda").reindex(orden).reset_index()

            temp.to_csv(PATH_OUT, sep=";", index=False, encoding="utf-8")

    # guardado final
    df_final = pd.concat([df_existente, pd.DataFrame(nuevas)], ignore_index=True)
    df_final = df_final.drop_duplicates(subset="id_vivienda", keep="last")

    orden = df["id_vivienda"].astype(str)
    df_final = df_final.set_index("id_vivienda").reindex(orden).reset_index()

    df_final.to_csv(PATH_OUT, sep=";", index=False, encoding="utf-8")

if __name__ == "__main__":
    generar_coords()
