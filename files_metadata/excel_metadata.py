from bs4 import BeautifulSoup
import pandas as pd
import io
import socks
import socket
import requests
from urllib.parse import urljoin

class OnionExcelScanner:
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

    def obtener_datos(self):
        # Obtener el contenido de la página web
        respuesta = self.make_tor_request(self.url)
        soup = BeautifulSoup(respuesta.text, 'html.parser')

        # Buscar todos los enlaces a archivos Excel
        enlaces_excel = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.xlsx')]

        for enlace in enlaces_excel:
            # Convertir enlace relativo a absoluto si es necesario
            enlace_absoluto = urljoin(self.url, enlace)

            # Obtener el contenido del archivo Excel
            respuesta = self.make_tor_request(enlace_absoluto)
            if respuesta is None:
                print(f"No se pudo descargar el archivo Excel de {enlace_absoluto}")
                continue

            archivo_excel = io.BytesIO(respuesta.content)

            # Leer el archivo Excel y extraer los datos
            df = pd.read_excel(archivo_excel)

            print(f'Datos para {enlace_absoluto}:')
            print(df)

if __name__ == "__main__":
    # Prueba la función con la URL de tu elección
    scanner = OnionExcelScanner('http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html')
    scanner.obtener_datos()
