import os
import json
import io
import socks
import socket
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

class TxtMetadataExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.results = {"TXT Metadata": {}}  # Diccionario para almacenar los resultados

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return None

    def scan_text_files(self):
        for url in tqdm(self.urls, desc="Scanning URLs for Txt files"):
            # Obtener el contenido de la página web
            response = self.make_tor_request(url)
            if response is None:
                self.results[url] = "URL not accessible though TOR."
                continue
            
            # Obtener los enlaces a archivos de texto
            text_links = self.extract_text_links(response.text)

            if not text_links:
                self.results[url] = "No text files found on this URL"
                continue

            for text_link in text_links:
                # Convertir enlace relativo a absoluto si es necesario
                absolute_link = self.make_absolute_link(url, text_link)
                
                # Obtener el contenido del archivo de texto
                response = self.make_tor_request(absolute_link)
                if response is None:
                    self.results[absolute_link] = "URL not accessible"
                    continue

                text_content = response.text

                # Leer los primeros 100 caracteres del archivo de texto para obtener metadatos
                metadata = self.extract_text_metadata(text_content)

                # Agregar el nombre del archivo al diccionario de metadatos
                file_name = text_link.split('/')[-1]
                self.results["TXT Metadata"][absolute_link] = metadata

        # Convertir los resultados a JSON y devolverlos
        return self.results

    def extract_text_links(self, html_content):
        """
        Extrae los enlaces a archivos de texto de un contenido HTML.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        text_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.txt')]
        return text_links

    def make_absolute_link(self, base_url, relative_link):
        """
        Convierte un enlace relativo a un enlace absoluto.
        """
        absolute_link = relative_link if relative_link.startswith('http') else os.path.join(base_url, relative_link)
        return absolute_link

    def extract_text_metadata(self, text_content):
        """
        Extrae los metadatos del contenido de un archivo de texto.
        """
        metadata = {
            "Content Length": len(text_content),
            "Word Count": len(text_content.split()),
            "Character Count": sum(len(word) for word in text_content.split()),
        }
        return metadata

if __name__ == "__main__":
    # Prueba la función con la lista de URLs de tu elección
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html', 'a', 'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion'
    ]
    scanner = TxtMetadataExtractor(urls)
    results_json = scanner.scan_text_files()
    print(json.dumps(scanner.results, indent=4))
