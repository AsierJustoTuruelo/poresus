import socks
import socket
import requests
import json
from tqdm import tqdm

class ETagScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {}  # Diccionario para almacenar los resultados de ETag

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            self.results[url] = f"Error al hacer la solicitud a través de Tor: {e}"
            return None

    def extract_etag(self, response):
        # Extraer la etiqueta ETag de la respuesta
        headers = response.headers
        if 'ETag' in headers:
            return headers['ETag']
        else:
            return None

    def scan_etag(self, url):
        try:
            # Realizar la solicitud a la URL dada
            response = self.make_tor_request(url)
            if response is None:
                self.results[url] = "No se pudo obtener la respuesta"
                return

            # Extraer la etiqueta ETag de la respuesta
            etag = self.extract_etag(response)

            if etag:
                self.results[url] = etag
            else:
                self.results[url] = "No encontrado ETag"
            
        except Exception as e:
            self.results[url] = f"Error al escanear la página {url}"

    def scan_etags(self):
        for url in tqdm(self.urls, desc="Scanning ETags"):  # Barra de progreso para cada URL
            self.scan_etag(url)

        # Devolver los resultados de ETag como un JSON
        return json.dumps(self.results)

if __name__ == "__main__":
    # Lista de URLs de prueba
    urls = [
        'http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/',"a", "http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/tests/"
        # Agrega más URLs aquí si es necesario
    ]
    scanner = ETagScanner(urls)
    results_json = scanner.scan_etags()
    print(results_json)
