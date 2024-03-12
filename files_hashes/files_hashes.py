import os
import hashlib
import requests
import socks
import socket
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class OnionFileAnalyzer:
    def __init__(self, onion_url):
        self.onion_url = onion_url
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

    def analyze_files_on_page(self):
        response = self.make_tor_request(self.onion_url)
        if response:
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                files = []
                for link in soup.find_all('a', href=True):
                    file_url = urljoin(self.onion_url, link['href'])
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
            print(f"No se pudo acceder a la página .onion: {self.onion_url}")
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

if __name__ == "__main__":
    onion_url = input("Ingrese la URL de la página .onion que desea escanear: ")
    analyzer = OnionFileAnalyzer(onion_url)
    files = analyzer.analyze_files_on_page()
    if files:
        print("Archivos encontrados en la página .onion:")
        for file_data in files:
            print(f"Nombre: {file_data['name']}")
            print(f"URL: {file_data['url']}")
            print("Huellas digitales:")
            for algo, hash_value in file_data['hashes'].items():
                print(f"{algo}: {hash_value}")
            print()
    else:
        print("No se encontraron archivos en la página .onion o se produjo un error durante el análisis.")
