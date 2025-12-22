import pandas as pd
import io

def transformar_provincias_a_castellano(input_file, output_file):
    """
    Carga un archivo CSV y reemplaza los nombres de las provincias
    en valenciano por sus nombres en castellano en las columnas
    'PROVINCIA' y 'EN_LOCALIDADES'.

    Args:
        input_file (str): Nombre del archivo CSV de entrada.
        output_file (str): Nombre del archivo CSV de salida.
    """
    try:
        # 1. Cargar el archivo CSV
        df = pd.read_csv(input_file, sep=';', encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: El archivo {input_file} no se encontró.")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    # Definir el mapeo de las provincias
    # Incluyo 'CASTELLÓ' y 'VALÈNCIA' por la columna EN_LOCALIDADES del ejemplo
    province_map = {
        'ALACANT': 'ALICANTE',
        'CASTELLÓ': 'CASTELLÓN',
        'CASTELLO': 'CASTELLÓN', # Por si aparece sin tilde
        'VALÈNCIA': 'VALENCIA',
        'VALENCIA': 'VALENCIA' # Por si ya aparece sin tilde
    }

    # 2. Aplicar la transformación a la columna PROVINCIA
    # El método .map() es ideal para reemplazar valores exactos
    df['PROVINCIA'] = df['PROVINCIA'].map(province_map).fillna(df['PROVINCIA'])

    # 3. Aplicar la transformación a la columna EN_LOCALIDADES
    # Esta columna requiere reemplazo de subcadenas ya que las provincias
    # están dentro de paréntesis, e.g., 'Agres (ALACANT)'
    def replace_provinces(text):
        if pd.isna(text):
            return text
        # Itera sobre el mapa y reemplaza cada nombre
        for valencian, spanish in province_map.items():
            # Reemplaza la provincia dentro de los paréntesis
            text = text.replace(f'({valencian})', f'({spanish})')
        return text

    df['EN_LOCALIDADES'] = df['EN_LOCALIDADES'].apply(replace_provinces)

    # 4. Guardar el DataFrame modificado en un nuevo archivo CSV
    df.to_csv(output_file, sep=';', index=False, encoding='utf-8')
    print(f"Transformación completada. El archivo modificado se ha guardado como: {output_file}")




transformar_provincias_a_castellano('database/turismoactivo.csv', 'database/output_turismoactivo_castellano.csv')

