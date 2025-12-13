# mapas/ui.py

import folium


def agregar_estilos_css(mapa):
    css = """
    <style>
    /* Estilos para el control de capas */
    .leaflet-control-layers {
        font-size: 14px !important;
        min-width: 220px !important;
    }

    .leaflet-control-layers-base label,
    .leaflet-control-layers-overlays label {
        padding: 8px 10px !important;
        margin: 5px 0 !important;
        font-weight: 500 !important;
    }

    .leaflet-control-layers-expanded {
        padding: 10px 14px !important;
        background: rgba(255, 255, 255, 0.96) !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        border: 2px solid rgba(0,0,0,0.1) !important;
    }

    .leaflet-control-layers-toggle {
        width: 44px !important;
        height: 44px !important;
        background-size: 24px 24px !important;
    }

    .leaflet-control-layers-separator {
        margin: 8px 0 !important;
        border-top: 2px solid rgba(0,0,0,0.1) !important;
    }
    </style>
    """
    mapa.get_root().html.add_child(folium.Element(css))


def finalizar_ui(mapa):
    """
    Aplica la UI básica:
    - Control de capas
    - Estilos CSS
    """
    folium.LayerControl(collapsed=False, position="topright").add_to(mapa)
    agregar_estilos_css(mapa)
