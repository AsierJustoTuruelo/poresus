import os
import hashlib
import requests
import socks
import socket
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

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
            return None

    def download_file(self, file_url):
        response = self.make_tor_request(file_url)
        if response and response.status_code == 200:
            return response.content
        else:
            return None

    def analyze_files_on_page(self, onion_url):
        response = self.make_tor_request(onion_url)
        if response:
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                files = []
                common_file_extensions = ['.txt', '.pdf', '.docx', '.xlsx', '.pptx', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.zip', '.rar', '.tar.gz', '.bin', '.mp3', '.mp4']
                file_links = [urljoin(onion_url, link['href']) for link in soup.find_all('a', href=True)]
                
                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = []
                    for file_link in file_links:
                        if any(file_link.endswith(extension) for extension in common_file_extensions):
                            futures.append(executor.submit(self.process_file, file_link))
                    
                    for future in tqdm(futures, desc="Calculating files hashes", unit="file"):
                        result = future.result()
                        if result:
                            files.append(result)

                return files
            except Exception as e:
                return {"Error": str(e)}
        else:
            return {"Error": f"Could not access .onion page: {onion_url}"}

    def process_file(self, file_link):
        file_content = self.download_file(file_link)
        if file_content:
            file_name = os.path.basename(file_link)
            file_hashes = self.calculate_hashes(file_content)
            return {"name": file_name, "url": file_link, "hashes": file_hashes}
        else:
            return {"name": os.path.basename(file_link), "url": file_link, "hashes": "Not accessible"}

    def calculate_hashes(self, file_content):
        try:
            sha256_hash = hashlib.sha256(file_content).hexdigest()
            md5_hash = hashlib.md5(file_content).hexdigest()
            return {"SHA-256": sha256_hash, "MD5": md5_hash}
        except Exception as e:
            return None

    def analyze_files(self):
        all_files = {}
        for onion_url in self.onion_urls:
            files = self.analyze_files_on_page(onion_url)
            if files is not None and len(files) != 0:
                all_files[onion_url] = files
            else:
                all_files[onion_url] = "No files found to analyze."

        return all_files


if __name__ == "__main__":
    onion_urls = [
        'http://kz62gxxle6gwe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html',
        # Add more URLs here if necessary
    ]
    analyzer = OnionFileAnalyzer(onion_urls)
    files_json = analyzer.analyze_files()
    print(json.dumps(files_json, indent=4))
