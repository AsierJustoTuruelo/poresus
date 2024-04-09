from urllib.parse import urljoin
from pptx import Presentation
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import io
import socks
import socket
import requests
import json
from tqdm import tqdm

class OnionPptScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {"ppt_metadata": {}}  # Diccionario para almacenar los resultados

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return None

    def scan_ppt_files(self):
        for url in tqdm(self.urls, desc="Scanning URLs for PowerPoint files"):
            # Obtener el contenido de la página web
            response = self.make_tor_request(url)
            if response is None:
                self.results[url] = "Url not accessible"
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Buscar todos los enlaces a archivos PowerPoint
            enlaces_ppt = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pptx')]

            if not enlaces_ppt:
                self.results[url] = "No PowerPoint files found on this URL"

            for enlace in enlaces_ppt:
                # Convertir enlace relativo a absoluto si es necesario
                enlace_absoluto = urljoin(url, enlace)

                # Obtener el contenido del archivo PowerPoint
                response = self.make_tor_request(enlace_absoluto)
                if response is None:
                    continue

                archivo_ppt = io.BytesIO(response.content)

                # Leer el archivo PowerPoint y extraer los metadatos
                presentacion = Presentation(archivo_ppt)
                metadatos = presentacion.core_properties

                # Convertir los metadatos a un formato serializable
                serializable_metadatos = {
                    "Título": metadatos.title,
                    "Autor": metadatos.author,
                    "Fecha de creación": str(metadatos.created),
                    "Última fecha de modificación": str(metadatos.modified),
                    "Nombre de archivo": enlace  # Agregar el nombre del archivo entre los metadatos
                }

                # Usar la URL como clave en el diccionario de resultados y agregar los metadatos al diccionario ppt_metadata
                if "ppt_metadata" not in self.results:
                    self.results["ppt_metadata"] = {}
                self.results["ppt_metadata"][url] = serializable_metadatos

        # Convertir los resultados a JSON y devolverlos
        return self.results

if __name__ == "__main__":
    # Lista de URLs de prueba
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html', 'a', 'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize'
        # Puedes agregar más URLs aquí si es necesario
    ]
    scanner = OnionPptScanner(urls)
    results_json = scanner.scan_ppt_files()
    print(json.dumps(scanner.results, indent=4))