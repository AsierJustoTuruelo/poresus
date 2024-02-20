import requests
import re
import socks
import socket
from stem import Signal
from stem.control import Controller

class GoogleIDsExtractor:
    def __init__(self, url):
        self.url = url
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def fetch_html_and_extract_google_ids(self):
        try:
            # Configuración del proxy para las solicitudes
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(self.url, proxies=self.proxies)
            if response.status_code == 200:
                html_content = response.text
                emails_found = self._extract_google_ids(html_content)
                return emails_found
            else:
                print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return []

    def _extract_google_ids(self, html_content):
        # Expresiones regulares para buscar IDs de Google Analytics y Google Publisher
        analytics_id_pattern = r'UA-\d{8}-\d{1,2}'
        publisher_id_pattern = r'pub-\d{16}'

        # Buscar IDs de Google Analytics y Google Publisher en el HTML
        analytics_ids = re.findall(analytics_id_pattern, html_content)
        publisher_ids = re.findall(publisher_id_pattern, html_content)

        return analytics_ids, publisher_ids

if __name__ == "__main__":
    url = input("Enter URL: ")
    extractor = GoogleIDsExtractor(url)
    analytics_ids, publisher_ids = extractor.fetch_html_and_extract_google_ids()
    print("Google Analytics IDs found:", analytics_ids)
    print("Google Publisher IDs found:", publisher_ids)