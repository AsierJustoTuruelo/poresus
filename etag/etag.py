import socks
import socket
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class ETagScanner:
    def __init__(self, url):
        self.url = url
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
            print(f"Error al hacer la solicitud a través de Tor: {e}")
            return None

    def extract_etag(self, response):
        # Extraer la etiqueta ETag de la respuesta
        print(response.headers)
        headers = response.headers
        if 'ETag' in headers:
            return headers['ETag']
        else:
            return None

    def scan_etag(self):
        try:
            # Realizar la solicitud a la URL dada
            response = self.make_tor_request(self.url)
            if response is None:
                print("No se pudo obtener la respuesta de la página.")
                return

            # Extraer la etiqueta ETag de la respuesta
            etag = self.extract_etag(response)

            if etag:
                print(f"La etiqueta ETag de la página es: {etag}")
            else:
                print("No se encontró la etiqueta ETag en la página.")
            
        except Exception as e:
            print(f"Error al escanear la página: {e}")

if __name__ == "__main__":
    # Prueba la función con la URL de tu elección
    scanner = ETagScanner('http://torlinksge6enmcyyuxjpjkoouw4oorgdgeo7ftnq3zodj7g2zxi3kyd.onion/')
    scanner.scan_etag()
