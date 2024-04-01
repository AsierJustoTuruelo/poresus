from bs4 import BeautifulSoup
import PyPDF2
import io
import socks
import socket
import requests
from urllib.parse import urljoin
import json

class OnionPdfScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {"pdf_metadata": {}}  # Diccionario para almacenar los resultados

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            print(f"Error al hacer la solicitud a través de Tor: {e}")
            return None

    def scan_pdf_files(self):
        for url in self.urls:
            # Obtener el contenido de la página web
            response = self.make_tor_request(url)
            if response is None:
                print(f"No se pudo acceder a la página {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Buscar todos los enlaces a archivos PDF
            pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

            for pdf_link in pdf_links:
                # Convertir enlace relativo a absoluto si es necesario
                absolute_link = urljoin(url, pdf_link)

                # Obtener el contenido del archivo PDF
                response = self.make_tor_request(absolute_link)
                if response is None:
                    print(f"No se pudo descargar el archivo PDF de {absolute_link}")
                    continue

                pdf_file = io.BytesIO(response.content)

                # Leer el archivo PDF y extraer los metadatos
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                metadata = pdf_reader.getDocumentInfo()

                # Convertir los metadatos a un formato serializable
                serializable_metadata = {}
                for key, value in metadata.items():
                    serializable_metadata[key] = str(value)

                self.results["pdf_metadata"][pdf_link] = serializable_metadata

        # Convertir loss resultados a JSON y devolverlos
        return json.dumps(self.results)

if __name__ == "__main__":
    # Lista de URLs de prueba
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html'
        # Puedes agregar más URLs aquí si es necesario
    ]
    scanner = OnionPdfScanner(urls)
    results_json = scanner.scan_pdf_files()
    print(results_json)
