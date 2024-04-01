from urllib.parse import urljoin
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
from bs4 import BeautifulSoup
import io
import socks
import socket
import requests
from mutagen.id3 import ID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp4 import MP4, MP4StreamInfoError
import os
import json


class OnionMediaScanner:
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

    def scan_media_files(self):
        results = {"media_metadata": [], "errors": []}

        for url in self.urls:
            # Obtener el contenido de la página web
            respuesta = self.make_tor_request(url)
            if respuesta is None:
                error_msg = f"No se pudo descargar la página web: {url}"
                print(error_msg)
                results["errors"].append(error_msg)
                continue
            
            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Buscar todos los enlaces a archivos MP3 y MP4
            enlaces_media = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith(('.mp3', '.mp4'))]

            for enlace in enlaces_media:
                # Convertir enlace relativo a absoluto si es necesario
                enlace_absoluto = urljoin(url, enlace)

                # Obtener el contenido del archivo de medios
                respuesta = self.make_tor_request(enlace_absoluto)
                if respuesta is None:
                    error_msg = f"No se pudo descargar el archivo de medios de {enlace_absoluto}"
                    print(error_msg)
                    results["errors"].append(error_msg)
                    continue

                archivo_media = io.BytesIO(respuesta.content)
                metadata = {}

                if enlace.endswith('.mp3'):
                    try:
                        metadatos = EasyID3(archivo_media)
                        metadata['format'] = 'MP3'
                    except ID3NoHeaderError:
                        error_msg = f"El archivo MP3 en {enlace_absoluto} no tiene una etiqueta ID3"
                        print(error_msg)
                        results["errors"].append(error_msg)
                        continue
                    
                    for key, value in metadatos.items():
                        metadata[key] = value
                    file_name = os.path.basename(enlace)
                
                elif enlace.endswith('.mp4'):
                    try:
                        metadatos = MP4(archivo_media)
                        metadata['format'] = 'MP4'
                    except MP4StreamInfoError:
                        error_msg = f"El archivo en {enlace_absoluto} no es un archivo MP4 válido"
                        results["errors"].append(error_msg)
                        continue
                    
                    for tag in metadatos.tags:
                        metadata[tag] = metadatos.tags[tag]
                    file_name = os.path.basename(enlace)
                
                results["media_metadata"].append({file_name: metadata})

        # Convertir los resultados a JSON y devolverlos
        return json.dumps(results)


if __name__ == "__main__":
    # Prueba la función con la lista de URLs de tu elección
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html'
    ]
    scanner = OnionMediaScanner(urls)
    results_json = scanner.scan_media_files()
    print(results_json)
