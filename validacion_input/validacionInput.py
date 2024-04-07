import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
import json
from tqdm import tqdm

class ValidacionInput:
    def __init__(self, onion_urls, tor_proxy="socks5h://127.0.0.1:9050"):
        self.onion_urls = onion_urls
        self.tor_proxy = tor_proxy
        self.session = requests.Session()
        self.session.proxies = {
            'http': self.tor_proxy,
            'https': self.tor_proxy
        }
        self.results = {}

    def is_accessible(self, url):
        try:
            response = self.session.head(url)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def get_form_inputs(self, onion_url):
        try:
            response = self.session.get(onion_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
           
            if not forms:
                return None

            for form in forms:
                inputs = form.find_all('input')
                for input in inputs:
                    yield input.get('name')
        except requests.exceptions.RequestException as e:
            return str(e)

    def test_input(self, onion_url):
        try:
            if not self.is_accessible(onion_url):
                self.results[onion_url] = {"error": "URL no accesible"}
                return
            
            inputs = list(self.get_form_inputs(onion_url))
            if inputs == []:
                self.results[onion_url] = {"Error": "No se encontraron formularios"}
                return

            results_for_url = {}
            for input_name in inputs:
                try:
                    response = self.session.get(onion_url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    form = soup.find('form')
                    if not form:
                        results_for_url[input_name] = {"error": "No se encontró ningún formulario"}
                        continue

                    action = form.get('action')
                    if not action:
                        results_for_url[input_name] = {"error": "No se encontró ninguna acción en el formulario"}
                        continue

                    res = self.session.post(urljoin(onion_url, action), data={input_name: "A" * 10000},
                                            proxies=self.session.proxies, allow_redirects=True)

                    results_for_url[input_name] = {
                        "status_code": res.status_code,
                        "response_text": res.text
                    }
                except requests.exceptions.RequestException as e:
                    results_for_url[input_name] = {"error": str(e)}
            self.results[onion_url] = results_for_url
        except requests.exceptions.RequestException as e:
            self.results[onion_url] = {"error": str(e)}

if __name__ == "__main__":
    onion_urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_validacion_entrada/prueba_validacion_entrada.html",
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/",
        "http://example.invalid"  # URL no válida para generar un error
    ]
    pentester = ValidacionInput(onion_urls, tor_proxy="socks5h://127.0.0.1:9050")
    threads = []
    for onion_url in onion_urls:
        thread = threading.Thread(target=pentester.test_input, args=(onion_url,))
        threads.append(thread)
        thread.start()

    for thread in tqdm(threads, desc="Progress"):
        thread.join()

    print(json.dumps(pentester.results))
