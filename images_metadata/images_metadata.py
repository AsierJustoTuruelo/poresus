import requests
import socks
import socket
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re

class OnionImageScanner:
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

    def scan_and_download_images(self):
        response = self.make_tor_request(self.url)
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            image_tags = soup.find_all('img')
            for img_tag in image_tags:
                img_url = img_tag.get('src')
                if img_url and self.is_absolute_url(img_url):
                    img_response = self.make_tor_request(img_url)
                    if img_response:
                        self.analyze_image(img_response.content)
                elif img_url and not self.is_absolute_url(img_url):
                    full_img_url = self.url + img_url
                    img_response = self.make_tor_request(full_img_url)
                    if img_response:
                        self.analyze_image(img_response.content)

    def analyze_image(self, image_data):
        try:
            image = Image.open(BytesIO(image_data))
            metadata = image.info
            print("Metadatos de la imagen:")
            for key, value in metadata.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error al analizar la imagen: {e}")

    def is_absolute_url(self, url):
        return bool(re.match(r'https?://', url))

if __name__ == "__main__":
    onion_url = input("Ingrese la URL del sitio .onion que desea escanear: ")
    scanner = OnionImageScanner(onion_url)
    scanner.scan_and_download_images()
