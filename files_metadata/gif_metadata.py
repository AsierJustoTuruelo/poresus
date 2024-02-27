import io
import socks
import socket
import requests
from urllib.parse import urljoin
from PIL import Image
from bs4 import BeautifulSoup   
from PIL import ImageSequence

class GifScanner:
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

    def scan_gifs(self):
        # Obtener el contenido de la página web
        respuesta = self.make_tor_request(self.url)
        soup = BeautifulSoup(respuesta.text, 'html.parser')

        # Buscar todos los enlaces a archivos GIF
        enlaces_gifs = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.gif')]

        for enlace in enlaces_gifs:
            # Convertir enlace relativo a absoluto si es necesario
            enlace_absoluto = urljoin(self.url, enlace)

            # Obtener el contenido del archivo GIF
            respuesta = self.make_tor_request(enlace_absoluto)
            if respuesta is None:
                print(f"No se pudo descargar el archivo GIF de {enlace_absoluto}")
                continue

            archivo_gif = io.BytesIO(respuesta.content)

            # Leer el nombre del archivo para intentar extraer información sobre el autor
            nombre_archivo = enlace.split("/")[-1]  # Obtenemos el nombre del archivo de la URL
            partes_nombre = nombre_archivo.split("_")  # Dividimos el nombre del archivo por guiones bajos
            
            posible_autor = " ".join(partes_nombre[:-1])  # Unimos todas las partes del nombre excepto la última
            if posible_autor != "":
                print(f'Posible autor del GIF en {enlace_absoluto}: {posible_autor}')

if __name__ == "__main__":
    # Prueba la función con la URL de tu elección
    scanner = GifScanner('http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html')
    scanner.scan_gifs()
