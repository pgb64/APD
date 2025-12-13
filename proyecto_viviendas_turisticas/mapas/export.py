# export.py

import os
import webbrowser

def guardar_y_abrir(mapa, output_html, abrir, total, tipo):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_dir = os.path.join(base_dir, "html")

    os.makedirs(html_dir, exist_ok=True)

    output_path = os.path.join(html_dir, output_html)

    mapa.save(output_path)
    print(f"✅ {tipo} generado: {output_path}")
    print(f"📍 Total de puntos: {total}")

    if abrir:
        webbrowser.open(f"file://{output_path}")
