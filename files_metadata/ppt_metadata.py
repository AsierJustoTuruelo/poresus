from urllib.parse import urljoin
from pptx import Presentation
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import io
import socks
import socket
import requests

class OnionPptScanner:
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

        # Buscar todos los enlaces a archivos PowerPoint
        enlaces_ppt = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pptx')]

        for enlace in enlaces_ppt:
            # Convertir enlace relativo a absoluto si es necesario
            enlace_absoluto = urljoin(self.url, enlace)

            # Obtener el contenido del archivo PowerPoint
            respuesta = self.make_tor_request(enlace_absoluto)
            if respuesta is None:
                print(f"No se pudo descargar el archivo PowerPoint de {enlace_absoluto}")
                continue

            archivo_ppt = io.BytesIO(respuesta.content)

            # Leer el archivo PowerPoint y extraer los metadatos
            presentacion = Presentation(archivo_ppt)
            metadatos = presentacion.core_properties

            print(f'Metadatos para {enlace_absoluto}:')
            print(f'  Título: {metadatos.title}')
            print(f'  Autor: {metadatos.author}')
            print(f'  Fecha de creación: {metadatos.created}')
            print(f'  Última fecha de modificación: {metadatos.modified}')

if __name__ == "__main__":
    # Prueba la función con la URL de tu elección
    scanner = OnionPptScanner('http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html')
    scanner.obtener_metadatos()
