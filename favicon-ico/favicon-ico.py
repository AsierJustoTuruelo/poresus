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
import re
import json

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
                    # Pasos 1 a 3: Convertir a base64 y añadir saltos de línea cada 76 caracteres
                    b64 = base64.b64encode(favicon_content)
                    utf8_b64 = b64.decode('utf-8')
                    with_newlines = re.sub("(.{76}|$)", "\\1\n", utf8_b64, 0, re.DOTALL)
                    # Calcular el hash MMH3
                    mmh3_hash = mmh3.hash(with_newlines.encode())

                    # Calcular el hash SHA-256
                    sha256_hash = hashlib.sha256(favicon_content).hexdigest()

                    # Calcular el hash MD5
                    md5_hash = hashlib.md5(favicon_content).hexdigest()

                    # Retornar los hashes en formato JSON
                    hashes_json = {
                        "MMH3": mmh3_hash,
                        "SHA-256": sha256_hash,
                        "MD5": md5_hash
                    }

                    return hashes_json
        print(f"No se pudo descargar el favicon de {self.url}")
        return None

if __name__ == "__main__":
    onion_url = input("Ingrese la URL del sitio .onion del que desea descargar el favicon: ")
    downloader = OnionFaviconDownloader(onion_url)
    hashes = downloader.download_favicon()
    if hashes:
        print(json.dumps(hashes, indent=4))
