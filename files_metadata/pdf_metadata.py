from bs4 import BeautifulSoup
import PyPDF2
import io
import socks
import socket
import requests
from urllib.parse import urljoin
import json
from tqdm import tqdm

class OnionPdfScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {"PDF Metadata": {}}

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return None

    def scan_pdf_files(self):
        for url in tqdm(self.urls, desc="Scanning URLs for PDF files"):
            response = self.make_tor_request(url)
            if response is None:
                self.results[url] = "URL not accessible"
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

            if not pdf_links:
                self.results[url] = "No PDF files found on this URL"

            for pdf_link in pdf_links:
                absolute_link = urljoin(url, pdf_link)
                response = self.make_tor_request(absolute_link)
                if response is None:
                    continue

                pdf_file = io.BytesIO(response.content)

                try:
                    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                    metadata = pdf_reader.getDocumentInfo()

                    file_name = pdf_link.split('/')[-1]
                    serializable_metadata = {
                        "file_name": file_name
                    }
                    for key, value in metadata.items():
                        serializable_metadata[key] = str(value)

                    self.results["PDF Metadata"][url] = serializable_metadata
                except Exception as e:
                    self.results["PDF Metadata"][url] = "Error reading PDF file"
                    pass

        return json.dumps(self.results)



if __name__ == "__main__":
    # Lista de URLs de prueba
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html', 'a', 'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata'
        # Puedes agregar más URLs aquí si es necesario
    ]
    scanner = OnionPdfScanner(urls)
    results_json = scanner.scan_pdf_files()
    print(results_json)
