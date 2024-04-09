import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from tqdm import tqdm

class XSSScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.payload = '<script>alert("XSS")</script>'
        self.results = {}

    def is_accessible(self, url):
        try:
            response = requests.head(url, proxies=self.proxies)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def get_forms(self, url):
        try:
            response = requests.get(url, proxies=self.proxies)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            return forms
        except Exception as e:
            print(f"Error al obtener los formularios de {url}: {e}")
            self.results[url] = {"error": str(e)}
            return []

    def submit_forms(self, forms, url):
        if not forms:
            self.results[url] = {"error": "No se encontraron formularios"}
            return

        for form in forms:
            try:
                form_data = {}
                inputs = form.find_all('input')
                textareas = form.find_all('textarea')
                selects = form.find_all('select')

                for input_tag in inputs:
                    if input_tag.get('type') == 'text' or input_tag.get('type') == 'search':
                        form_data[input_tag.get('name')] = self.payload
                for textarea_tag in textareas:
                    form_data[textarea_tag.get('name')] = self.payload
                for select_tag in selects:
                    options = select_tag.find_all('option')
                    for option_tag in options:
                        form_data[select_tag.get('name')] = option_tag.get('value')

                action = form.get('action')
                full_url = urljoin(url, action)  # Construir la URL completa
                response = requests.post(full_url, data=form_data, proxies=self.proxies)
                if self.payload in response.text:
                    self.results[url] = {
                        "vulnerable_form": action,
                        "vulnerable": True
                    }
            
            except Exception as e:
                print(f"Error al enviar el formulario en {url}: {e}")
                if url in self.results:
                    self.results[url]["error"] = str(e)
                else:
                    self.results[url] = {"error": str(e)}

    def scan_xss(self):
        for url in tqdm(self.urls, desc="Scanning URLs for XSS vulnerabilities"):
            if not self.is_accessible(url):
                self.results[url] = {"error": "URL no accesible"}
                continue
            forms = self.get_forms(url)
            self.submit_forms(forms, url)

        return self.results

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_xss/prueba_xss.html",
        "a",
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_xss/"
    ]
    scanner = XSSScanner(urls)
    results = scanner.scan_xss()
    print(json.dumps(results, indent=4))
