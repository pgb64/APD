from geopy.geocoders import ArcGIS
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut
import time

class Coordenadas:
    def __init__(self, timeout=10):
        self.geolocator = ArcGIS(timeout=timeout)

    def obtener_coords(self, address: str, reintentos=3):
        """Devuelve (lat, lon) o None."""
        for _ in range(reintentos):
            try:
                localizacion = self.geolocator.geocode(address)
                if not localizacion:
                    return None
                return (localizacion.latitude, localizacion.longitude)
            except (GeocoderTimedOut, GeocoderUnavailable, Exception):
                time.sleep(1)

        return None
