# mapas/layers.py

import folium
import pandas as pd
from folium.plugins import MarkerCluster, HeatMap
from folium import FeatureGroup


# ============================================================
# === POPUP DE VIVIENDAS =====================================
# ============================================================

def _popup_vivienda(row):
    def val(campo, sufijo=""):
        v = row.get(campo, None)
        return f"{v}{sufijo}" if pd.notna(v) else "N/D"

    return f"""
    <div style="font-size: 13px;">
        <b>ID vivienda:</b> {val("id_vivienda")}<br>
        <b>Fecha alta:</b> {val("fecha_alta")}<br>
        <b>Superficie:</b> {val("superficie", " m²")}<br>
        <b>Plazas:</b> {val("plazas")}<br>
        <b>Habitaciones:</b> {val("habitaciones")}
    </div>
    """


# ============================================================
# === CAPA DE MARCADORES (VIVIENDAS) =========================
# ============================================================

def crear_marcadores(
    df,
    columna_lat,
    columna_lon,
    columna_tooltip,
    nombre,
    show,
    color,
    fill,
    radio
):
    grupo = FeatureGroup(name=nombre, show=show)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row[columna_lat], row[columna_lon]],
            radius=radio,
            popup=_popup_vivienda(row),
            tooltip=f"ID: {row.get('id_vivienda', '')}",
            color=color,
            fill=True,
            fillColor=fill,
            fillOpacity=0.6,
            weight=2
        ).add_to(grupo)

    return grupo


# ============================================================
# === CAPA DE CLUSTERS ======================================
# ============================================================

def crear_clusters(
    df,
    columna_lat,
    columna_lon,
    columna_tooltip,
    nombre,
    show,
    color,
    fill,
    radio
):
    cluster = MarkerCluster(name=nombre, show=show)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row[columna_lat], row[columna_lon]],
            radius=radio,
            popup=_popup_vivienda(row),
            tooltip=f"ID: {row.get('id_vivienda', '')}",
            color=color,
            fill=True,
            fillColor=fill,
            fillOpacity=0.6,
            weight=2
        ).add_to(cluster)

    return cluster


# ============================================================
# === MAPA DE CALOR (GENÉRICO) ===============================
# ============================================================

def crear_mapa_calor(
    df,
    columna_lat,
    columna_lon,
    radio,
    blur,
    gradiente
):
    coords = df[[columna_lat, columna_lon]].dropna().values.tolist()

    return HeatMap(
        coords,
        radius=radio,
        blur=blur,
        min_opacity=0.3,
        max_opacity=0.9,
        gradient=gradiente
    )


# ============================================================
# === CAPA: INFORMACIÓN DEL MUNICIPIO ========================
# ============================================================

def crear_info_municipios(
    df_municipios,
    nombre="Información del municipio",
    show=False
):
    """
    Capa de municipios:
    - 1 marcador por municipio
    - Solo municipios con lat/lon
    - Popup con datos de Wikidata
    """
    grupo = FeatureGroup(name=nombre, show=show)

    if df_municipios is None or df_municipios.empty:
        return grupo

    for _, row in df_municipios.iterrows():

        lat = row.get("lat")
        lon = row.get("lon")

        if pd.isna(lat) or pd.isna(lon):
            continue

        popup = f"""
        <div style="font-size: 13px;">
            <b>Municipio:</b> {row.get("nombre", "N/D")}<br>
            <b>Código INE:</b> {row.get("codigo_ine", "N/D")}<br>
            <b>Población:</b> {row.get("poblacion", "N/D")}<br>
            <b>Wikidata:</b>
            <a href="https://www.wikidata.org/wiki/{row.get("qid")}"
               target="_blank">{row.get("qid")}</a>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=popup,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(grupo)

    return grupo
