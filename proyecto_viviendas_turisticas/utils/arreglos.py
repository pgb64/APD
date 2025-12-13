import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "..", "database")

INPUT = os.path.join(DATABASE_DIR, "viviendas_depuradas.csv")
OUTPUT = os.path.join(DATABASE_DIR, "viviendas_limpias.csv")

# ============================
#  DICCIONARIO COMPLETO
#  CORRECCIÓN MUNICIPIOS
# ============================

correcciones_por_codigo = {
    # ALICANTE
    "03001": "L'ATZÚBIA",
    "03011": "L'ALFÀS DEL PI",
    "03014": "ALACANT / ALICANTE",
    "03021": "BANYERES DE MARIOLA",
    "03042": "EL POBLE NOU DE BENITATXELL",
    "03048": "CALLOSA D'EN SARRIÀ",
    "03049": "CALLOSA DE SEGURA",
    "03050": "EL CAMPELLO",
    "03054": "CASTELL DE CASTELLS",
    "03060": "QUATRETONDETA",
    "03070": "FORMENTERA DEL SEGURA",
    "03071": "GATA DE GORGOS",
    "03075": "EL CASTELL DE GUADALEST",
    "03076": "GUARDAMAR DEL SEGURA",
    "03077": "EL FONDÓ DE LES NEUS / HONDÓN DE LAS NIEVES",
    "03078": "HONDÓN DE LOS FRAILES",
    "03083": "XIXONA / JIJONA",
    "03084": "L'ORXA / LORCHA",
    "03088": "MONFORTE DEL CID",
    "03092": "MURO DE ALCOY",
    "03094": "LA NUCIA",
    "03105": "EL PINÓS / PINOSO",
    "03110": "EL RÀFOL D'ALMÚNIA",
    "03114": "LA ROMANA",
    "03115": "SAGRA",
    "03118": "SAN FULGENCIO",
    "03119": "SANT JOAN D'ALACANT",
    "03120": "SAN MIGUEL DE SALINAS",
    "03122": "SANT VICENT DEL RASPEIG",
    "03132": "LA TORRE DE LES MAÇANES / TORREMANZANAS",
    "03134": "LA VALL D'ALCALÀ",
    "03135": "LA VALL D'EBO",
    "03136": "LA VALL DE GALLINERA",
    "03137": "LA VALL DE LAGUAR",
    "03139": "LA VILA JOIOSA / VILLAJOYOSA",
    "03901": "ELS POBLETS",
    "03902": "PILAR DE LA HORADADA",
    "03903": "LOS MONTESINOS",

    # CASTELLÓN
    "12004": "ALCALÀ DE XIVERT",
    "12006": "L'ALCÚDIA DE VEO",
    "12007": "ALFONDEGUILLA",
    "12014": "ARES DEL MAESTRAT",
    "12028": "BENICÀSSIM / BENICASIM",
    "12032": "BORRIANA / BURRIANA",
    "12036": "CANET LO ROIG",
    "12037": "CASTELL DE CABRES",
    "12040": "CASTELLÓ DE LA PLANA",
    "12041": "CASTILLO DE VILLAMALEFA",
    "12044": "CERVERA DEL MAESTRE",
    "12048": "CORTES DE ARENOSO",
    "12050": "LES COVES DE VINROMÀ",
    "12063": "FUENTE LA REINA",
    "12064": "FUENTES DE AYÓDAR",
    "12075": "LA MATA DE MORELLA",
    "12083": "OLOCAU DEL REY",
    "12085": "ORPESA / OROPESA DEL MAR",
    "12089": "PENÍSCOLA / PEÑÍSCOLA",
    "12090": "PINA DE MONTORNÈS",
    "12091": "PORTELL DE MORELLA",
    "12092": "PUEBLA DE ARENOSO",
    "12093": "LA POBLA DE BENIFASSÀ",
    "12094": "LA POBLA TORNESA",
    "12098": "LA SALZADELLA",
    "12099": "SANT JORDI",
    "12102": "SANTA MAGDALENA DE PULPIS",
    "12103": "LA SERRATELLA",
    "12105": "SIERRA ENGARCERÁN",
    "12107": "SOT DE FERRER",
    "12108": "SUERA",
    "12116": "TORRALBA DEL PINAR",
    "12120": "TORRE D'EN BESORA",
    "12125": "LA VALL D'ALMONACID",
    "12129": "VILAFRANCA DEL CID",
    "12130": "VILLAHERMOSA DEL RÍO",
    "12133": "VILLANUEVA DE VIVER",
    "12134": "VILAR DE CANES",
    "12139": "VISTABELLA DEL MAESTRAT",
    "12141": "ZORITA DEL MAESTRAZGO",
    "12901": "LES ALQUERIES",
    "12902": "SANT JOAN DE MORÓ",

    # VALENCIA
    "46008": "ALBALAT DE LA RIBERA",
    "46009": "ALBALAT DELS SORELLS",
    "46010": "ALBALAT DELS TARONGERS",
    "46013": "ALBORAIA / ALBORAYA",
    "46020": "L'ALCÚDIA DE CRESPINS",
    "46028": "ALGAR DE PALANCIA",
    "46041": "ARAS DE LOS OLMOS",
    "46042": "AIELO DE MALFERIT",
    "46043": "AIELO DE RUGAT",
    "46048": "BELLREGUARD",
    "46053": "BENEIXIDA",
    "46058": "BENIFAIRÓ DE LES VALLS",
    "46059": "BENIFAIRÓ DE LA VALLDIGNA",
    "46074": "BONREPÒS I MIRAMBELL",
    "46079": "CALLES",
    "46080": "CAMPORROBLES",
    "46082": "CANET D'EN BERENGUER",
    "46090": "CASTELLÓ DE LA RIBERA",
    "46091": "CASTELLONET DE LA CONQUESTA",
    "46092": "CASTIELFABIB",
    "46095": "CAUDETE DE LAS FUENTES",
    "46099": "CORTES DE PALLÁS",
    "46101": "QUART DE LES VALLS",
    "46102": "QUART DE POBLET",
    "46124": "FONTANARS DELS ALFORINS",
    "46127": "LA FONT D'EN CARRÒS",
    "46128": "LA FONT DE LA FIGUERA",
    "46129": "FUENTERROBLES",
    "46140": "GUARDAMAR DE LA SAFOR",
    "46149": "LOSA DEL OBISPO",
    "46154": "LLANERA DE RANES",
    "46157": "LLOSA DE RANES",
    "46170": "MOIXENT / MOGENT",
    "46171": "MONTCADA",
    "46176": "MONTROI",
    "46178": "NÀQUERA / NÁQUERA",
    "46187": "PALMA DE GANDÍA",
    "46197": "POLINYÀ DE XÚQUER",
    "46199": "LA POBLA DE FARNALS",
    "46202": "LA POBLA DE VALLBONA",
    "46203": "LA POBLA LLARGA",
    "46204": "PUIG DE SANTA MARIA",
    "46210": "EL RÀFOL DE SALEM",
    "46211": "REAL DE GANDÍA",
    "46214": "RIBA-ROJA DE TÚRIA",
    "46217": "ROTGLÀ I CORBERA",
    "46220": "SAGUNT / SAGUNTO",
    "46231": "SIMAT DE LA VALLDIGNA",
    "46234": "SOT DE CHERA",
    "46237": "TAVERNES BLANQUES",
    "46238": "TAVERNES DE LA VALLDIGNA",
    "46245": "TORRES TORRES",
    "46254": "VENTA DEL MORO",
    "46255": "VILALLONGA / VILLALONGA",
    "46258": "VILLAR DEL ARZOBISPO",
    "46259": "VILLARGORDO DEL CABRIEL",
    "46903": "SAN ANTONIO DE BENAGÉBER",
    "46904": "BENICULL DE XÚQUER"
}

# Mapa de prefijo de código de municipio -> provincia
provincia_por_prefijo = {
    "03": "ALICANTE",
    "12": "CASTELLÓN",
    "46": "VALENCIA"
}

# ===================================
#     APLICAR CORRECCIONES
# ===================================

df = pd.read_csv(INPUT, sep=";", dtype=str, keep_default_na=False)

# Normalizamos espacios
df["municipio"] = df["municipio"].str.strip()
df["num_municipio"] = df["num_municipio"].str.strip()

# Reemplazo basado en el código oficial
df["municipio"] = df["num_municipio"].map(correcciones_por_codigo).fillna(df["municipio"])

# Asignar provincia según el prefijo del código de municipio
df["provincia"] = df["num_municipio"].str[:2].map(provincia_por_prefijo).fillna(df["provincia"])

# Guardar
df.to_csv(OUTPUT, sep=";", index=False, encoding="utf-8")

print("✔ Municipios corregidos mediante num_municipio y guardados en:", OUTPUT)