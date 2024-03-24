import requests
import re
import socks
import socket
import json
from stem import Signal
from stem.control import Controller

class GoogleIDsExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def fetch_html_and_extract_google_ids(self):
        results = []
        try:
            # Configuración del proxy para las solicitudes
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            for url in self.urls:
                response = requests.get(url, proxies=self.proxies)
                if response.status_code == 200:
                    html_content = response.text
                    analytics_ids, publisher_ids = self._extract_google_ids(html_content)
                    results.append({"analytics_ids": analytics_ids, "publisher_ids": publisher_ids})
                else:
                    print(f"Error al hacer la solicitud para {url}. Código de estado: {response.status_code}")

            return json.dumps(results)
        except requests.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return json.dumps(results)

    def _extract_google_ids(self, html_content):
        # Expresiones regulares para buscar IDs de Google Analytics y Google Publisher
        analytics_id_pattern = r'UA-\d{8}-\d{1,2}'
        publisher_id_pattern = r'pub-\d{16}'

        # Buscar IDs de Google Analytics y Google Publisher en el HTML
        analytics_ids = re.findall(analytics_id_pattern, html_content)
        publisher_ids = re.findall(publisher_id_pattern, html_content)

        return analytics_ids, publisher_ids

if __name__ == "__main__":
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/google_ap/google_ap.html'
    ]
    extractor = GoogleIDsExtractor(urls)
    results_json = extractor.fetch_html_and_extract_google_ids()
    print(results_json)
