import socks
import socket
import requests
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

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
            print(f"Error haciendo la solicitud a {url}: {e}")
            return None

    def extract_sensitive_data(self, headers):
        # Definir los encabezados sensibles que queremos extraer
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
            for url in tqdm(self.urls, desc="Scanning URLs for GZIP header"):
                response = self.make_tor_request(url)
                if response is None:
                    results[url] = {"Error": "No se pudo obtener la respuesta de la página"}
                    continue

                headers = response.headers

                gzip_enabled = 'Content-Encoding' in headers and headers['Content-Encoding'] == 'gzip'

                extracted_data = self.extract_sensitive_data(headers)

                estimated_location = self.estimate_location()

                results[url] = {
                    "gzip_enabled": gzip_enabled,
                    "sensitive_data": extracted_data,
                    "estimated_location": estimated_location
                }

            return results

        except Exception as e:
            print(f"Error al escanear las páginas: {e}")
