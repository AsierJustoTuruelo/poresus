import os
import hashlib
import requests
import socks
import socket
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json

class OnionFileAnalyzer:
    def __init__(self, onion_urls):
        self.onion_urls = onion_urls
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

    def analyze_files_on_page(self, onion_url):
        response = self.make_tor_request(onion_url)
        if response:
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                files = []
                for link in soup.find_all('a', href=True):
                    file_url = urljoin(onion_url, link['href'])
                    file_response = self.make_tor_request(file_url)
                    if file_response and file_response.status_code == 200:
                        file_content = file_response.content
                        file_name = os.path.basename(file_url)
                        file_hashes = self.calculate_hashes(file_content)
                        files.append({"name": file_name, "url": file_url, "hashes": file_hashes})
                return files
            except Exception as e:
                print(f"Error al analizar la página .onion: {e}")
                return None
        else:
            print(f"No se pudo acceder a la página .onion: {onion_url}")
            return None

    def calculate_hashes(self, file_content):
        try:
            # Calcular el hash SHA-256
            sha256_hash = hashlib.sha256(file_content).hexdigest()

            # Calcular el hash MD5
            md5_hash = hashlib.md5(file_content).hexdigest()

            return {"SHA-256": sha256_hash, "MD5": md5_hash}
        except Exception as e:
            print(f"Error al calcular los hashes del archivo: {e}")
            return None

    def analyze_files(self):
        all_files = {}
        for onion_url in self.onion_urls:
            files = self.analyze_files_on_page(onion_url)
            if files:
                all_files[onion_url] = files
        return all_files

if __name__ == "__main__":
    # Lista de URLs de prueba
    onion_urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/metadata/metadata.html',
        # Agrega más URLs aquí si es necesario
    ]
    analyzer = OnionFileAnalyzer(onion_urls)
    files_json = analyzer.analyze_files()
    print(json.dumps(files_json, indent=4))
