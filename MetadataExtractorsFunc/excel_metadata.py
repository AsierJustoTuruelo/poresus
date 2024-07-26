from bs4 import BeautifulSoup
import pandas as pd
import io
import socks
import socket
import requests
from urllib.parse import urljoin
import json
from tqdm import tqdm

class ExcelMetadataExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {"Excel Metadata": {}}  # Diccionario para almacenar los resultados

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return None

    def scan_excel_files(self):
        for url in tqdm(self.urls, desc="Scanning URLs for Excel files"):
            # Obtener el contenido de la página web
            respuesta = self.make_tor_request(url)
            if respuesta is None:
                self.results[url] = "URL not accessible"
                continue

            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Buscar todos los enlaces a archivos Excel
            enlaces_excel = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.xlsx')]

            if not enlaces_excel:
                self.results[url] = "No Excel files found on this URL"

            for enlace in enlaces_excel:
                # Convertir enlace relativo a absoluto si es necesario
                enlace_absoluto = urljoin(url, enlace)

                # Obtener el contenido del archivo Excel
                respuesta = self.make_tor_request(enlace_absoluto)
                if respuesta is None:
                    continue

                try:
                    archivo_excel = io.BytesIO(respuesta.content)

                    # Leer el archivo Excel y extraer los datos
                    df = pd.read_excel(archivo_excel)
                    json_data = df.to_json(orient="records")

                    self.results["Excel Metadata"][enlace] = json_data
                except Exception as e:
                    self.results["Excel Metadata"][enlace] = "Error reading Excel file"
        # Convertir los resultados a JSON y devolverlos
        return self.results

if __name__ == "__main__":
    # Lista de URLs de prueba
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html', 'a', 'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/'
        # Agrega más URLs aquí si es necesario
    ]
    scanner = ExcelMetadataExtractor(urls)
    results_json = scanner.scan_excel_files()
    print(json.dumps(scanner.results, indent=4))
