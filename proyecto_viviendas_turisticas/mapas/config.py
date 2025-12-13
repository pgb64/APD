# mapas/config.py

ZOOM_MIN = 1
ZOOM_MAX = 18
ZOOM_DEFAULT = 10

MAPAS_BASE = {
    'relieve': {
        'tiles': 'OpenTopoMap',
        'attr': 'OpenTopoMap',
        'name': 'Relieve'
    },
    'calles': {
        'tiles': 'OpenStreetMap',
        'attr': 'OpenStreetMap',
        'name': 'Calles'
    },
    'satelite': {
        'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        'attr': 'Esri',
        'name': 'Satélite'
    },
    'claro': {
        'tiles': 'CartoDB positron',
        'attr': 'CartoDB',
        'name': 'Claro'
    },
    'oscuro': {
        'tiles': 'CartoDB dark_matter',
        'attr': 'CartoDB',
        'name': 'Oscuro'
    }
}

GRADIENTE_CALOR = {
    '0.0': 'navy',
    '0.25': 'blue',
    '0.5': 'lime',
    '0.75': 'orange',
    '1.0': 'red'
}
