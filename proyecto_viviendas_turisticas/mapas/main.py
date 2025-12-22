from mapa import Mapa
import os

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "..", "database", "coords_cv.csv")

    mapa = Mapa()

    mapa.generar_mapa_calor(
        csv_path=csv_path,
        output_html="mapa_viviendas_turisticas.html",
        zoom_inicial=12,
        columna_tooltip="id_vivienda",
        radio_calor=20,
        blur_calor=15,
        mostrar_marcadores=True
    )

if __name__ == "__main__":
    main()


