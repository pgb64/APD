# mapas/base.py

import folium
from config import MAPAS_BASE

def crear_mapa_base(centro, zoom, tipo_base):
    mapa = folium.Map(location=centro, zoom_start=zoom, tiles=None)
    cfg = MAPAS_BASE[tipo_base]

    folium.TileLayer(
        tiles=cfg['tiles'],
        attr=cfg['attr'],
        name=cfg['name']
    ).add_to(mapa)

    return mapa


def agregar_capas_base(mapa, excluir):
    for tipo, cfg in MAPAS_BASE.items():
        if tipo == excluir:
            continue

        folium.TileLayer(
            tiles=cfg['tiles'],
            attr=cfg['attr'],
            name=cfg['name'],
            overlay=False
        ).add_to(mapa)
