# mapas/mapa.py

import folium
import os
from typing import Optional, Tuple

from config import ZOOM_DEFAULT, GRADIENTE_CALOR
from data import (
    cargar_y_validar_datos,
    calcular_centro,
    unir_viviendas,
    cargar_municipios_desde_jsonld
)
from base import crear_mapa_base, agregar_capas_base
from layers import (
    crear_marcadores,
    crear_clusters,
    crear_mapa_calor,
    crear_info_municipios
)
from export import guardar_y_abrir
from ui import finalizar_ui


class Mapa:
    def __init__(self):
        self.mapa: Optional[folium.Map] = None

        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.csv_viviendas_path = os.path.normpath(
            os.path.join(base_dir, "..", "database", "viviendas_limpias.csv")
        )

        self.jsonld_path = os.path.normpath(
            os.path.join(base_dir, "..", "database", "viviendas_enriquecidas.jsonld")
        )

    # ========================================================
    # === CARGA DE DATOS =====================================
    # ========================================================

    def _cargar_df_viviendas(
        self,
        csv_coords_path: str,
        separador_coords: str,
        columna_lat: str,
        columna_lon: str
    ):
        df = cargar_y_validar_datos(
            csv_coords_path,
            separador_coords,
            columna_lat,
            columna_lon
        )

        if not os.path.exists(self.csv_viviendas_path):
            raise FileNotFoundError(
                f"❌ No se encontró viviendas_limpias.csv en: {self.csv_viviendas_path}"
            )

        df = unir_viviendas(df, self.csv_viviendas_path)

        return df

    def _cargar_df_municipios(self):
        if not os.path.exists(self.jsonld_path):
            print("⚠️ JSON-LD NO encontrado")
            return None

        df = cargar_municipios_desde_jsonld(self.jsonld_path)

        if df is None:
            print("❌ df_municipios es None")
            return None

        return df

    # ========================================================
    # === MAPA GENERAL =======================================
    # ========================================================

    def generar_mapa(
        self,
        csv_path: str,
        output_html: str = "mapa.html",
        centro: Optional[Tuple[float, float]] = None,
        zoom_inicial: int = ZOOM_DEFAULT,
        abrir_navegador: bool = True,
        columna_lat: str = "latitud",
        columna_lon: str = "longitud",
        columna_tooltip: Optional[str] = None,
        separador: str = ";"
    ) -> Optional[folium.Map]:

        df_viv = self._cargar_df_viviendas(
            csv_path, separador, columna_lat, columna_lon
        )

        if df_viv.empty:
            print("❌ No se encontraron coordenadas válidas")
            return None

        centro = calcular_centro(df_viv, centro, columna_lat, columna_lon)

        self.mapa = crear_mapa_base(centro, zoom_inicial, "relieve")
        agregar_capas_base(self.mapa, "relieve")

        crear_marcadores(
            df_viv,
            columna_lat,
            columna_lon,
            columna_tooltip,
            "Viviendas",
            True,
            "blue",
            "lightblue",
            5
        ).add_to(self.mapa)

        crear_clusters(
            df_viv,
            columna_lat,
            columna_lon,
            columna_tooltip,
            "Clusters",
            False,
            "blue",
            "lightblue",
            5
        ).add_to(self.mapa)

        df_municipios = self._cargar_df_municipios()

        crear_info_municipios(
            df_municipios if df_municipios is not None else [],
            nombre="Información del municipio",
            show=False
        ).add_to(self.mapa)

        finalizar_ui(self.mapa)

        guardar_y_abrir(
            self.mapa,
            output_html,
            abrir_navegador,
            len(df_viv),
            "Mapa de viviendas"
        )

        return self.mapa

    # ========================================================
    # === MAPA DE CALOR ======================================
    # ========================================================

    def generar_mapa_calor(
        self,
        csv_path: str,
        output_html: str = "mapa_calor.html",
        centro: Optional[Tuple[float, float]] = None,
        zoom_inicial: int = ZOOM_DEFAULT,
        abrir_navegador: bool = True,
        columna_lat: str = "latitud",
        columna_lon: str = "longitud",
        columna_tooltip: Optional[str] = None,
        separador: str = ";",
        radio_calor: int = 20,
        blur_calor: int = 15,
        mostrar_marcadores: bool = True
    ) -> Optional[folium.Map]:

        df_viv = self._cargar_df_viviendas(
            csv_path, separador, columna_lat, columna_lon
        )

        if df_viv.empty:
            print("❌ No se encontraron coordenadas válidas")
            return None

        centro = calcular_centro(df_viv, centro, columna_lat, columna_lon)

        self.mapa = crear_mapa_base(centro, zoom_inicial, "relieve")
        agregar_capas_base(self.mapa, "relieve")

        heat = crear_mapa_calor(
            df_viv,
            columna_lat,
            columna_lon,
            radio_calor,
            blur_calor,
            GRADIENTE_CALOR
        )

        folium.FeatureGroup(
            name="Mapa de Calor",
            show=True
        ).add_child(heat).add_to(self.mapa)

        if mostrar_marcadores:
            crear_marcadores(
                df_viv,
                columna_lat,
                columna_lon,
                columna_tooltip,
                "Viviendas",
                False,
                "darkred",
                "red",
                3
            ).add_to(self.mapa)

            crear_clusters(
                df_viv,
                columna_lat,
                columna_lon,
                columna_tooltip,
                "Clusters",
                False,
                "darkred",
                "red",
                3
            ).add_to(self.mapa)

        df_municipios = self._cargar_df_municipios()

        crear_info_municipios(
            df_municipios if df_municipios is not None else [],
            nombre="Información del municipio",
            show=False
        ).add_to(self.mapa)

        finalizar_ui(self.mapa)

        guardar_y_abrir(
            self.mapa,
            output_html,
            abrir_navegador,
            len(df_viv),
            "Mapa de calor"
        )

        return self.mapa
