import requests
import socks
import socket
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urljoin
import json
from tqdm import tqdm
from io import BytesIO
import base64

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
            return None

    def scan_images(self):
        results = {}
        for onion_url in tqdm(self.urls, desc="Scanning URLs for Images Files"):
            response = self.make_tor_request(onion_url)
            if response:
                if response.status_code == 404:
                    results[onion_url] = "not found"
                    continue
                soup = BeautifulSoup(response.content, 'html.parser')
                image_tags = soup.find_all('img')
                if not image_tags:
                    results[onion_url] = "No images found"
                    continue
                for img_tag in image_tags:
                    img_url = img_tag.get('src')
                    if img_url:
                        full_img_url = urljoin(onion_url, img_url)
                        img_response = self.make_tor_request(full_img_url)
                        if img_response and self.is_image_response(img_response):
                            image_info = self.analyze_image(img_response.content)
                            if image_info:
                                results[onion_url] = results.get(onion_url, [])
                                results[onion_url].append({
                                    'image_url': full_img_url,
                                    'image_info': image_info
                                })
            else:
                results[onion_url] = "Url not reachable"
        return results

    def is_image_response(self, response):
        return response.headers['Content-Type'].startswith('image')

    def analyze_image(self, image_data):
        try:
            image = Image.open(BytesIO(image_data))
            image_info = {
                'size': image.size,
                'mode': image.mode,
                'metadata': str(image.info)
                
            }
            return image_info
        except Exception as e:
            return None

if __name__ == "__main__":
    onion_urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html', 
        "A", 
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/bitcoin_address/bitcoin_adress.html"
    ]
    scanner = OnionImageScanner(onion_urls)
    results = scanner.scan_images()
    print(json.dumps(results, indent=2))
