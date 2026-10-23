
import csv
import json
import os
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.parse import urlencode

# Coordenades de Barcelona
parametres = {
    "latitude": 41.3874,
    "longitude": 2.1686,
    "current": (
        "temperature_2m,"
        "relative_humidity_2m,"
        "precipitation,"
        "wind_speed_10m"
    ),
    "timezone": "Europe/Madrid",
}

url = (
    "https://api.open-meteo.com/v1/forecast?"
    + urlencode(parametres)
)

# Consultar les dades meteorològiques
with urlopen(url, timeout=30) as resposta:
    dades = json.loads(resposta.read().decode("utf-8"))

actual = dades["current"]

# Preparar el registre
registre = {
    "consulta_utc": datetime.now(timezone.utc).isoformat(),
    "hora_local": actual["time"],
    "localitat": "Barcelona",
    "temperatura_C": actual["temperature_2m"],
    "humitat_percent": actual["relative_humidity_2m"],
    "precipitacio_mm": actual["precipitation"],
    "vent_kmh": actual["wind_speed_10m"],
}

# Guardar les dades en un fitxer CSV
os.makedirs("dades", exist_ok=True)
fitxer = "dades/historial.csv"
camps = list(registre.keys())

existeix = os.path.exists(fitxer)

with open(fitxer, "a", newline="", encoding="utf-8") as arxiu:
    escriptor = csv.DictWriter(arxiu, fieldnames=camps)

    if not existeix:
        escriptor.writeheader()

    escriptor.writerow(registre)

print("Dades meteorològiques desades correctament:")
print(registre)
