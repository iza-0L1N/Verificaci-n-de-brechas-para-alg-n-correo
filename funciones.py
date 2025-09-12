import os
import getpass
import requests
import csv
import logging
import argparse


 # Crear función para lectura de API key
def leer_apikey(path="apikey.txt"):
    if not os.path.exists(path):
        clave = getpass.getpass("Ingresa tu API key: ")
        with open(path, "w") as archivo:
            archivo.write(clave.strip())
    with open(path, "r") as archivo:
        return archivo.read().strip()


 # Crear función para obtener argumentos con argparse
def obtener_argumentos():
    parser = argparse.ArgumentParser(
        description="Verifica si un correo ha sido comprometido usando la API de " \
        "Have I Been Pwned.")
    parser.add_argument("correo", help="Correo electrónico a verificar")
    parser.add_argument("-o", "--output", default="reporte.csv", \
                        help="Nombre del archivo CSV de salida")
    return parser.parse_args()


 # Crear función para consultas brechas por correo
def consultar_brechas(correo, api_key):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{correo}"
    headers = {"hibp-api-key": api_key, "user-agent": "PythonScript"}
    return requests.get(url, headers=headers)


 # Crear función para consultar detalles por brecha
def consultar_detalle(nombre, api_key):
    url = f"https://haveibeenpwned.com/api/v3/breach/{nombre}"
    headers = {"hibp-api-key": api_key, "user-agent": "PythonScript"}
    return requests.get(url, headers=headers)


 # Crear función para generar archivo CSV
def generar_csv(nombre_archivo, lista_detalles):
    with open(nombre_archivo, "w", newline='', encoding="utf-8") as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["Título", "Dominio", "Fecha de Brecha", "Datos Comprometidos", "Verificada", "Sensible"])
        for detalle in lista_detalles:
            writer.writerow([
                detalle.get("Title"),
                detalle.get("Domain"),
                detalle.get("BreachDate"),
                ", ".join(detalle.get("DataClasses", [])),
                "Sí" if detalle.get("IsVerified") else "No",
                "Sí" if detalle.get("IsSensitive") else "No"
            ])


 # Configurar logging
logging.basicConfig(
    filename="registro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
