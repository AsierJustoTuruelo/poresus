from bs4 import BeautifulSoup
from docx import Document
import io
import socks
import socket
import requests
from urllib.parse import urljoin
import json
from datetime import datetime

class OnionWordScanner:
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
            print(f"Error al hacer la solicitud a través de Tor: {e}")
            return None

    def scan_word_files(self):
        results = {"word_metadata": []}

        for url in self.urls:
            # Obtener el contenido de la página web
            respuesta = self.make_tor_request(url)
            if respuesta is None:
                print(f"No se pudo descargar la página web: {url}")
                results['error'] = f"No se pudo descargar la página web: {url}"
                continue
            
            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Buscar todos los enlaces a archivos Word
            enlaces_word = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.docx')]

            for enlace in enlaces_word:
                # Convertir enlace relativo a absoluto si es necesario
                enlace_absoluto = urljoin(url, enlace)

                # Obtener el contenido del archivo Word
                respuesta = self.make_tor_request(enlace_absoluto)
                if respuesta is None:
                    print(f"No se pudo descargar el archivo Word de {enlace_absoluto}")
                    results['error'] = f"No se pudo descargar el archivo Word de {enlace_absoluto}"
                    continue

                archivo_word = io.BytesIO(respuesta.content)

                # Leer el archivo Word y extraer los metadatos
                documento = Document(archivo_word)
                metadatos = documento.core_properties

                metadata_dict = {}
                for key in metadatos.__dir__():
                    if not key.startswith('_'):
                        value = getattr(metadatos, key)
                        # Convertir objetos datetime a strings
                        if isinstance(value, datetime):
                            value = value.isoformat()
                        metadata_dict[key] = value

                results["word_metadata"].append({enlace: metadata_dict})

        # Convertir los resultados a JSON y devolverlos
        return json.dumps(results, default=str)  # Convertir objetos datetime a strings


if __name__ == "__main__":
    # Prueba la función con la lista de URLs de tu elección
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html'
    ]
    scanner = OnionWordScanner(urls)
    results_json = scanner.scan_word_files()
    print(results_json)
