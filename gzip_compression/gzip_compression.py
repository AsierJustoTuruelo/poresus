import io
import socks
import socket
import requests
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
from tqdm import tqdm  # Importa tqdm

class GzipHeaderScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return None

    def extract_sensitive_data(self, headers):
        # Extraer información sensible de los encabezados HTTP
        sensitive_headers = ["Date", "Otro encabezado sensible", "Otra información sensible"]
        extracted_data = {}
        for header in sensitive_headers:
            if header in headers:
                extracted_data[header] = headers[header]
        return extracted_data

    def estimate_location(self):
        # Estimar la ubicación aproximada en función de la hora actual
        hora_actual = datetime.now().hour
        if 0 <= hora_actual < 6:
            return "Oceanía"
        elif 6 <= hora_actual < 12:
            return "Asia"
        elif 12 <= hora_actual < 18:
            return "Europa"
        else:
            return "América"

    def scan_gzip_headers(self):
        results = {}
        try:
            for url in tqdm(self.urls, desc="Scanning URLs for GZIP header"):  # Barra de progreso para cada URL
                # Realizar la solicitud a la URL dada
                response = self.make_tor_request(url)
                print(response.headers)
                if response is None:
                    results[url] = {f"No se pudo obtener la respuesta de la página"}
                    continue

                # Analizar los encabezados HTTP
                headers = response.headers

                # Verificar si la compresión GZIP está presente en los encabezados
                gzip_enabled = 'Content-Encoding' in headers and headers['Content-Encoding'] == 'gzip'

                # Extraer datos sensibles de los encabezados HTTP
                extracted_data = self.extract_sensitive_data(headers)

                # Estimar la ubicación basada en la hora actual
                estimated_location = self.estimate_location()

                # Agregar resultados al diccionario de resultados
                results[url] = {
                    "gzip_enabled": gzip_enabled,
                    "sensitive_data": extracted_data,
                    "estimated_location": estimated_location
                }

            # Devolver los resultados
            return results
            
        except Exception as e:
            print(f"Error al escanear la página: {e}")


if __name__ == "__main__":
    # Prueba la función con la lista de URLs de tu elección
    urls = [
        "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/"
    ]
    scanner = GzipHeaderScanner(urls)
    results_json = scanner.scan_gzip_headers()
    print(results_json)
