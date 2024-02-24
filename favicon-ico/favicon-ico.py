import requests
import socks
import socket
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
import hashlib
from urllib.parse import urljoin
from bs4 import BeautifulSoup

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
                    # Calcular el hash MD5 de la imagen del favicon
                    favicon_hash = hashlib.md5(favicon_content).hexdigest()
                    print(f"Hash del favicon.ico (MD5): {favicon_hash}")
                    return favicon_content
        print(f"No se pudo descargar el favicon de {self.url}")
        return None

    def compare_favicons(self, surface_favicons):
        onion_favicon = self.download_favicon()
        if onion_favicon:
            onion_favicon_hash = hashlib.md5(onion_favicon).hexdigest()
            for surface_url, surface_favicon in surface_favicons.items():
                surface_favicon_hash = hashlib.md5(surface_favicon).hexdigest()
                if onion_favicon_hash == surface_favicon_hash:
                    print(f"El favicon de {self.url} coincide con el de {surface_url}")
                else:
                    print(f"El favicon de {self.url} no coincide con el de {surface_url}")

if __name__ == "__main__":
    onion_url = input("Ingrese la URL del sitio .onion del que desea descargar el favicon: ")
    # Aquí debes proporcionar un diccionario con los favicons de los sitios web de la web superficial que quieres comparar
    surface_favicons = {} 
    downloader = OnionFaviconDownloader(onion_url)
    downloader.compare_favicons(surface_favicons)
