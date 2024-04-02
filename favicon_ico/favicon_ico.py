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
from tqdm import tqdm  # Importa tqdm

class OnionFaviconDownloader:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {}  # Diccionario para almacenar los resultados de hashes

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
        for url in tqdm(self.urls, desc="Downloading Favicons"):  # Barra de progreso para cada URL
            response = self.make_tor_request(url)
            if response:
                try:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    link_tag = soup.find('link', rel='icon')
                    if link_tag:
                        favicon_url = urljoin(url, link_tag.get('href'))
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

                            # Almacenar los hashes en el diccionario de resultados
                            self.results[url] = {
                                "MMH3": mmh3_hash,
                                "SHA-256": sha256_hash,
                                "MD5": md5_hash
                            }
                        else:
                            self.results[url] = "No se pudo descargar el favicon"
                    else:
                            self.results[url] = "No se pudo descargar el favicon"
                except Exception as e:
                    print(f"Error al procesar la URL {url}: {e}")
        if not self.results:
            print("No se pudo descargar el favicon de ninguna de las URLs proporcionadas.")
        return self.results

if __name__ == "__main__":
    urls = ["http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/favicon-ico/favicon-ico.html"]
    downloader = OnionFaviconDownloader(urls)
    hashes = downloader.download_favicon()
    if hashes:
        print(json.dumps(hashes, indent=4))
