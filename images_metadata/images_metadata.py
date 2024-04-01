import requests
import socks
import socket
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
from urllib.parse import urljoin
import json
import os 

class OnionImageScanner:
    def __init__(self, urls):
        self.urls = urls
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

    def scan_images(self):
        results = {}
        for onion_url in self.urls:
            response = self.make_tor_request(onion_url)
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                image_tags = soup.find_all('img')
                for img_tag in image_tags:
                    img_url = img_tag.get('src')
                    if img_url:
                        full_img_url = urljoin(onion_url, img_url)
                        img_response = self.make_tor_request(full_img_url)
                        if img_response and self.is_image_response(img_response):
                            image_data = img_response.content
                            image_info = self.analyze_image(image_data)
                            # Obtener solo el nombre de la imagen
                            img_name = os.path.basename(full_img_url)
                            results[img_name] = image_info  # Usar solo el nombre de la imagen como clave
        return results

    def is_image_response(self, response):
        return response.headers['Content-Type'].startswith('image')

    def analyze_image(self, image_data):
        try:
            image = Image.open(BytesIO(image_data))
            image_info = {
                'size': image.size,
                'mode': image.mode,
                'metadata': image.info
            }
            return image_info
        except Exception as e:
            print(f"Error al analizar la imagen: {e}")
            return None

if __name__ == "__main__":
    onion_urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html'
        
    ]
    scanner = OnionImageScanner(onion_urls)
    results = scanner.scan_images()
    print(json.dumps(results, indent=2))
