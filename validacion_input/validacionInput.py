import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
import json

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

    def get_form_inputs(self, onion_url):
        try:
            response = self.session.get(onion_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')

            for form in forms:
                inputs = form.find_all('input')
                for input in inputs:
                    yield input.get('name')
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {onion_url}: {e}")

    def test_input(self, onion_url, input_name, test_value):
        try:
            response = self.session.get(onion_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')
            if not form:
                print(f"No se encontró ningún formulario en {onion_url}")
                return

            action = form.get('action')
            if not action:
                print(f"No se encontró ninguna acción en el formulario de {onion_url}")
                return

            res = self.session.post(urljoin(onion_url, action), data={input_name: test_value},
                                    proxies=self.session.proxies, allow_redirects=True)

            self.results[input_name] = {
                "status_code": res.status_code,
                "response_text": res.text
            }

        except requests.exceptions.RequestException as e:
            print(f"Error durante la prueba para el input {input_name} en {onion_url}: {e}")

    def run_tests(self):
        threads = []
        for onion_url in self.onion_urls:
            for input_name in self.get_form_inputs(onion_url):
                # Prueba con entradas muy largas
                thread = threading.Thread(target=self.test_input, args=(onion_url, input_name, "A" * 10000))
                threads.append(thread)
                thread.start()

                # Prueba con números fuera de rango
                thread = threading.Thread(target=self.test_input, args=(onion_url, input_name, 1000000000))
                threads.append(thread)
                thread.start()

                # Prueba con fechas/horas incorrectas
                thread = threading.Thread(target=self.test_input, args=(onion_url, input_name, "30-02-2023"))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    onion_urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_validacion_entrada/prueba_validacion_entrada.html"
    ]
    pentester = ValidacionInput(onion_urls, tor_proxy="socks5h://127.0.0.1:9050")
    pentester.run_tests()
    print(json.dumps(pentester.results))
