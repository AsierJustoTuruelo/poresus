from bs4 import BeautifulSoup
from PIL import Image
import io
import socks
import socket
import requests
from urllib.parse import urljoin
import json

class OnionGifScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {"gif_metadata": {}}  # Diccionario para almacenar los resultados

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            print(f"Error al hacer la solicitud a través de Tor: {e}")
            return None

    def scan_gif_files(self):
        for url in self.urls:
            # Obtener el contenido de la página web
            respuesta = self.make_tor_request(url)
            if respuesta is None:
                print(f"No se pudo acceder a la página {url}")
                continue

            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Buscar todos los enlaces a archivos GIF
            enlaces_gif = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.gif')]

            for enlace in enlaces_gif:
                # Convertir enlace relativo a absoluto si es necesario
                enlace_absoluto = urljoin(url, enlace)

                # Obtener el contenido del archivo GIF
                respuesta = self.make_tor_request(enlace_absoluto)
                if respuesta is None:
                    print(f"No se pudo descargar el archivo GIF de {enlace_absoluto}")
                    continue

                archivo_gif = io.BytesIO(respuesta.content)

                # Leer el archivo GIF y extraer los metadatos
                imagen_gif = Image.open(archivo_gif)
                metadatos = imagen_gif.info

                # Convertir los metadatos a un formato serializable
                serializable_metadatos = {}
                for key, value in metadatos.items():
                    serializable_metadatos[key] = str(value)

                self.results["gif_metadata"][enlace] = serializable_metadatos

        # Convertir los resultados a JSON y devolverlos
        return json.dumps(self.results)

if __name__ == "__main__":
    # Lista de URLs de prueba
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html'
        # Puedes agregar más URLs aquí si es necesario
    ]
    scanner = OnionGifScanner(urls)
    results_json = scanner.scan_gif_files()
    print(results_json)
