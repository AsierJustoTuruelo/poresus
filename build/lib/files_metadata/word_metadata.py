from bs4 import BeautifulSoup
from docx import Document
import io
import socks
import socket
import requests
from urllib.parse import urljoin
import json
from datetime import datetime
from tqdm import tqdm

class OnionWordScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {"word_metadata": {}}  # Diccionario para almacenar los resultados

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return None

    def scan_word_files(self):
        for url in tqdm(self.urls, desc="Scanning URLs for Word files"):
            # Obtener el contenido de la página web
            response = self.make_tor_request(url)
            if response is None:
                self.results[url] = "No accesible"
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')

            # Buscar todos los enlaces a archivos Word
            word_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.docx')]

            if not word_links:
                self.results[url] = "No Word files found on this URL"
                continue

            for word_link in word_links:
                # Convertir enlace relativo a absoluto si es necesario
                absolute_link = urljoin(url, word_link)
                
                # Obtener el contenido del archivo Word
                response = self.make_tor_request(absolute_link)
                if response is None:
                    self.results[absolute_link] = "No accesible"
                    continue

                word_file = io.BytesIO(response.content)

                # Leer el archivo Word y extraer los metadatos
                document = Document(word_file)
                metadata = document.core_properties

                metadata_dict = {}
                for key in metadata.__dir__():
                    if not key.startswith('_'):
                        value = getattr(metadata, key)
                        # Convertir objetos datetime a strings
                        if isinstance(value, datetime):
                            value = value.isoformat()
                        metadata_dict[key] = value

                # Agregar el nombre del archivo al diccionario de metadatos
                file_name = word_link.split('/')[-1]
                self.results["word_metadata"][absolute_link] = metadata_dict

        # Convertir los resultados a JSON y devolverlos
        return self.results


if __name__ == "__main__":
    # Prueba la función con la lista de URLs de tu elección
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html', 'a', 'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion'
    ]
    scanner = OnionWordScanner(urls)
    results_json = scanner.scan_word_files()
    print(json.dumps(scanner.results, indent=4))
