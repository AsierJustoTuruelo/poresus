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
from tqdm import tqdm

class OnionMediaScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {"Media Metadata": {}}  # Diccionario para almacenar los resultados

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return None

    def scan_media_files(self):
        for url in tqdm(self.urls, desc="Scanning URLs for Media files"):
            # Obtener el contenido de la página web
            respuesta = self.make_tor_request(url)
            if respuesta is None:
                self.results[url] = "URL not accessible through TOR."
                continue
            
            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Buscar todos los enlaces a archivos MP3 y MP4
            enlaces_media = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith(('.mp3', '.mp4'))]

            if not enlaces_media:
                self.results[url] = "No media files found on this URL"
                continue

            for enlace in enlaces_media:
                # Convertir enlace relativo a absoluto si es necesario
                enlace_absoluto = urljoin(url, enlace)
                # Obtener el contenido del archivo de medios
                respuesta = self.make_tor_request(enlace_absoluto)
                if respuesta is None:
                    self.results[enlace_absoluto] = "URL not accessible through TOR."
                    continue

                archivo_media = io.BytesIO(respuesta.content)
                metadata = {}

                if enlace.endswith('.mp3'):
                    try:
                        metadatos = EasyID3(archivo_media)
                        metadata['format'] = 'MP3'
                    except ID3NoHeaderError:
                        self.results[enlace_absoluto] = "No ID3 tags found"
                        continue
                    
                    for key, value in metadatos.items():
                        metadata[key] = value
                    file_name = os.path.basename(enlace)
                
                elif enlace.endswith('.mp4'):
                    try:
                        metadatos = MP4(archivo_media)
                        metadata['format'] = 'MP4'
                    except MP4StreamInfoError:
                        self.results[enlace_absoluto] = "Invalid MP4 file"
                        continue
                    
                    for tag in metadatos.tags:
                        metadata[tag] = metadatos.tags[tag]
                    file_name = os.path.basename(enlace)
               
                
                # Agregar el nombre del archivo al diccionario de metadatos
                metadata["File Name"] = file_name

                self.results["Media Metadata"][enlace_absoluto] = metadata

        # Convertir los resultados a JSON y devolverlos
        return self.results


if __name__ == "__main__":
    # Prueba la función con la lista de URLs de tu elección
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html', 'a', 'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/'
    ]
    scanner = OnionMediaScanner(urls)
    results_json = scanner.scan_media_files()
    print(json.dumps(scanner.results, indent=4))
