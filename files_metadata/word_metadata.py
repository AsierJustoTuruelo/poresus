from bs4 import BeautifulSoup
from docx import Document
import io
import socks
import socket
import requests
from urllib.parse import urljoin


class OnionWordScanner:
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

        # Buscar todos los enlaces a archivos Word
        enlaces_word = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.docx')]

        for enlace in enlaces_word:
            # Convertir enlace relativo a absoluto si es necesario
            enlace_absoluto = urljoin(self.url, enlace)

            # Obtener el contenido del archivo Word
            respuesta = self.make_tor_request(enlace_absoluto)
            if respuesta is None:
                print(f"No se pudo descargar el archivo Word de {enlace_absoluto}")
                continue

            archivo_word = io.BytesIO(respuesta.content)

            # Leer el archivo Word y extraer los metadatos
            documento = Document(archivo_word)
            metadatos = documento.core_properties

            print(f'Metadatos para {enlace_absoluto}:')
            for key in metadatos.__dir__():
                if not key.startswith('_'):
                    value = getattr(metadatos, key)
                    print(f'  {key}: {value}')

if __name__ == "__main__":
    # Prueba la función con la URL de tu elección
    scanner = OnionWordScanner('http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html')
    scanner.obtener_metadatos()