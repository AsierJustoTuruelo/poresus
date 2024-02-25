import requests
import socks
import socket
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
import hashlib
import mmh3
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import base64

SHODAN_API_KEY = 'QfGPuZYj6CwENQ9xlenqQC8bbsjy2yDs'

class OnionFaviconDownloader:
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

    def download_favicon(self):
        response = self.make_tor_request(self.url)
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            link_tag = soup.find('link', rel='icon')
            if link_tag:
                favicon_url = urljoin(self.url, link_tag.get('href'))
                favicon_response = self.make_tor_request(favicon_url)
                if favicon_response and favicon_response.status_code == 200:
                    favicon_content = favicon_response.content
                    # Calcular el hash MMH3 de la imagen del favicon
                    mmh3_hash = mmh3.hash(favicon_content)
                    print(f"Hash del favicon.ico (MMH3): {mmh3_hash}")

                    # Calcular el hash SHA-256
                    sha256_hash = hashlib.sha256(favicon_content).hexdigest()
                    print(f"Hash del favicon.ico (SHA-256): {sha256_hash}")

                    # Calcular el hash MD5
                    md5_hash = hashlib.md5(favicon_content).hexdigest()
                    print(f"Hash del favicon.ico (MD5): {md5_hash}")

                    # Búsqueda en Shodan
                    shodan_results = self.search_shodan(mmh3_hash)
                    if shodan_results is not None:
                        print(shodan_results)
                    else:
                        print("No se encontraron resultados en Shodan")

                    return favicon_content
        print(f"No se pudo descargar el favicon de {self.url}")
        return None

    def search_shodan(self, favicon_hash):
        try:
            shodan_url = f'https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query=http.favicon.hash:{favicon_hash}'
            response = requests.get(shodan_url)
            if response.status_code == 200:
                data = response.json()
                return data['matches']
            else:
                print(f"Error al realizar la solicitud a Shodan. Código de estado: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error al procesar la respuesta de Shodan: {e}")
            return None

if __name__ == "__main__":
    onion_url = input("Ingrese la URL del sitio .onion del que desea descargar el favicon: ")
    downloader = OnionFaviconDownloader(onion_url)
    downloader.download_favicon()
