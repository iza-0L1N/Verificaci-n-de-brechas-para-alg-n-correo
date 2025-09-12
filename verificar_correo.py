import sys
import os
import getpass
import requests
import time
import csv
import logging
logging.basicConfig(
    filename="registro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if len(sys.argv) != 2:
    print("Uso: python verificar_correo.py correo@example.com")
    logging.error("Número incorrecto de argumentos. Se espera 1 (correo).")
    sys.exit(1)
correo = sys.argv[1]
api_key_path = "apikey.txt"
if not os.path.exists(api_key_path):
    print("No se encontró el archivo apikey.txt.")
    clave = getpass.getpass("Ingresa tu API key: ")
    try:
        with open(api_key_path, "w") as archivo:
            archivo.write(clave.strip())
    except Exception as e:
        logging.error(f"No se pudo guardar la API key: {e}")
        sys.exit(1)

try:
    with open(api_key_path, "r") as archivo:
        api_key = archivo.read().strip()
except Exception as e:
    print("Error al leer la API key.")
    logging.error(f"No se pudo guardar la API key: {e}")
    sys.exit(1)
url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{correo}"
headers = {
    "hibp-api-key": api_key,
    "user-agent": "PythonScript"
}
try:
    response = requests.get(url, headers=headers)
except Exception as e:
    print("Error al conectar con la API.")
    logging.error(f"Error de conexión: {e}")
    sys.exit(1)
if response.status_code == 200:
    brechas = response.json()
    print(len(brechas))
    logging.info(f"Consulta exitosa para {correo}. \
               Brechas encontradas: {len(brechas)}")
    try:
        with open(
            "reporte.csv", "w", newline='', encoding="utf-8"
        ) as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow([
                "Título", "Dominio", "Fecha de Brecha",
                "Datos Comprometidos", "Verificada", "Sensible"
            ])
            for i, brecha in enumerate(brechas[:3]):
                nombre = brecha['Name']
                detalle_url = f"https://haveibeenpwned.com/api/v3/breach/{nombre}"
                try:
                    detalle_resp = requests.get(detalle_url, headers=headers)
                    if detalle_resp.status_code == 200:
                        detalle = detalle_resp.json()
                        writer.writerow([
                            detalle.get("Title"),
                            detalle.get("Domain"),
                            detalle.get("BreachDate"),
                            ", ".join(detalle.get("DataClasses", [])),
                            "Sí" if detalle.get("IsVerified") else "No",
                            "Sí" if detalle.get("IsSensitive") else "No"
                        ])
                    else:
                        msj = f"No se pudo obtener detalles de la brecha: {nombre}. "
                        msj += f"Código: {detalle_resp.status_code}"
                        logging.error(msj)
                except Exception as e:
                    logging.error(f"Error al consultar detalles \
                                    de la brecha {nombre}: {e}")
                if i < 2:
                    time.sleep(10)   # Delay entre consultas
    except Exception as e:
        print("Error al generar el archivo CSV.")
        logging.error(f"Error al escribir reporte.csv: {e}")
        sys.exit(1)
    print("Consulta completada. \
        Revisa el archivo reporte.csv para ver los resultados.")
elif response.status_code == 404:
    print(f"La cuenta {correo} no aparece en ninguna brecha conocida.")
    logging.info(f"Consulta exitosa para {correo}. No se encontraron brechas.")
elif response.status_code == 401:
    print("Error de autenticación: revisa tu API key.")
    logging.error("Error 401: API key inválida.")
else:
    print(f"Error inesperado. Código de estado: {response.status_code}")
    logging.error(f"Error inesperado. Código de estado: \
    {response.status_code}")
