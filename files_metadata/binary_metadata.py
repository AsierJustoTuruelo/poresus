import io
import socks
import socket
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

class BinaryFileMetadataExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {"Binary Data": {}}

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return None

    def scan_binary_files(self):
        for url in tqdm(self.urls, desc="Scanning URLs for Binary files"):
            # Obtener el contenido de la página web
            response = self.make_tor_request(url)
            if response is None:
                self.results[url] = "URL not accessible through Tor"
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Buscar todos los enlaces a archivos binarios
            binary_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.bin')]

            if not binary_links:
                self.results[url] = "No binary files found on this URL"

            binary_data_per_url = {}
            for binary_link in binary_links:
                # Convertir enlace relativo a absoluto si es necesario
                absolute_link = urljoin(url, binary_link)

                # Obtener el contenido del archivo binario
                response = self.make_tor_request(absolute_link)
                if response is None:
                    continue

                binary_file = io.BytesIO(response.content)

                # Leer el archivo binario y convertirlo en una lista de cadenas binarias
                data = binary_file.read()
                binary_data = [format(byte, '08b') for byte in data]

                binary_data_per_url[binary_link] = {"File's URL": absolute_link, "Binary Data": binary_data}

            self.results["Binary Data"].update(binary_data_per_url)

        # Convertir los resultados a JSON y devolverlos
        return self.results

if __name__ == "__main__":
    # Lista de URLs de prueba
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html', 'a', 'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/'
        # Puedes agregar más URLs aquí si es necesario
    ]
    scanner = BinaryFileMetadataExtractor(urls)
    results_json = scanner.scan_binary_files()
    print(json.dumps(scanner.results, indent=4))
