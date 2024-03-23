import io
import socks
import socket
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json

class BinaryFileScanner:
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

    def scan_binary_files(self):
        result_data = {}
        for url in self.urls:
            # Obtener el contenido de la página web
            response = self.make_tor_request(url)
            if response is None:
                print(f"No se pudo acceder a la página {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Buscar todos los enlaces a archivos binarios
            binary_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.bin')]

            binary_data_per_url = {}
            for binary_link in binary_links:
                # Convertir enlace relativo a absoluto si es necesario
                absolute_link = urljoin(url, binary_link)

                # Obtener el contenido del archivo binario
                response = self.make_tor_request(absolute_link)
                if response is None:
                    print(f"No se pudo descargar el archivo binario de {absolute_link}")
                    continue

                binary_file = io.BytesIO(response.content)

                # Leer el archivo binario y convertirlo en una lista de cadenas binarias
                data = binary_file.read()
                binary_data = [format(byte, '08b') for byte in data]

                binary_data_per_url[binary_link] = binary_data

            result_data.update(binary_data_per_url)

        # Convertir los resultados a JSON y devolverlos
        return json.dumps(result_data)

if __name__ == "__main__":
    # Lista de URLs de prueba
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html'
        # Puedes agregar más URLs aquí si es necesario
    ]
    scanner = BinaryFileScanner(urls)
    results_json = scanner.scan_binary_files()
    print(results_json)
