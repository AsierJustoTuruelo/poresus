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


class OnionMediaScanner:
    def __init__(self, url):
        self.url = url
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

    def obtener_metadatos(self):
        # Obtener el contenido de la página web
        respuesta = self.make_tor_request(self.url)
        soup = BeautifulSoup(respuesta.text, 'html.parser')

        # Buscar todos los enlaces a archivos MP3 y MP4
        enlaces_media = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith(('.mp3', '.mp4'))]

        for enlace in enlaces_media:
            # Convertir enlace relativo a absoluto si es necesario
            enlace_absoluto = urljoin(self.url, enlace)

            # Obtener el contenido del archivo de medios
            respuesta = self.make_tor_request(enlace_absoluto)
            if respuesta is None:
                print(f"No se pudo descargar el archivo de medios de {enlace_absoluto}")
                continue

            archivo_media = io.BytesIO(respuesta.content)

            if enlace.endswith('.mp3'):
                try:
                    metadatos = EasyID3(archivo_media)
                except ID3NoHeaderError:
                    print(f"El archivo MP3 en {enlace_absoluto} no tiene una etiqueta ID3")
                    continue
                
                print(f"Metadatos del archivo MP3 en {enlace_absoluto}:")
                for key, value in metadatos.items():
                    print(f"{key}: {value}")
                print("\n")
                
            elif enlace.endswith('.mp4'):
                try:
                    metadatos = MP4(archivo_media)
                except MP4StreamInfoError:
                    print(f"El archivo en {enlace_absoluto} no es un archivo MP4 válido")
                    continue
                
                print(f"Metadatos del archivo MP4 en {enlace_absoluto}:")
                for tag in metadatos.tags:
                    print(tag)
                print("\n")

if __name__ == "__main__":
    # Prueba la función con la URL de tu elección
    scanner = OnionMediaScanner('http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html')
    scanner.obtener_metadatos()
