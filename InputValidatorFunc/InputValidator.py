import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
import json
from tqdm import tqdm

class InputValidatorClass:
    def __init__(self, onion_urls):
        self.onion_urls = onion_urls
        self.tor_proxy = "socks5h://127.0.0.1:9050"
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
                self.results[onion_url] = {"Error": "URL not accessible."}
                return
            
            inputs = list(self.get_form_inputs(onion_url))
            if inputs == []:
                self.results[onion_url] = {"Error": "Could not find any form inputs."}
                return

            results_for_url = {}
            for input_name in inputs:
                try:
                    response = self.session.get(onion_url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    form = soup.find('form')
                    if not form:
                        results_for_url[input_name] = {"Error": "Could not find any form in the page."}
                        continue

                    action = form.get('action')
                    if not action:
                        results_for_url[input_name] = {"Error": "Could not find any action in the form."}
                        continue

                    res = self.session.post(urljoin(onion_url, action), data={input_name: "A" * 10000},
                                            proxies=self.session.proxies, allow_redirects=True)

                    results_for_url[input_name] = {
                        "Status Code": res.status_code,
                        "Response Text": res.text
                    }
                except requests.exceptions.RequestException as e:
                    results_for_url[input_name] = {"Error": "Error sending POST request."}
            self.results[onion_url] = results_for_url
        except requests.exceptions.RequestException as e:
            self.results[onion_url] = {"Error": "Error sending request."}

    def run_tests(self):
        threads = []
        for onion_url in self.onion_urls:
            thread = threading.Thread(target=self.test_input, args=(onion_url,))
            threads.append(thread)
            thread.start()

        for thread in tqdm(threads, desc="Scanning URLs for input validation"):
            thread.join()

        return self.results


if __name__ == "__main__":
    onion_urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_validacion_entrada/prueba_validacion_entrada.html",
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/",
        "http://example.invalid"  # URL no válida para generar un error
    ]
    pentester = InputValidatorClass(onion_urls)
    results = pentester.run_tests()

    print(json.dumps(results))
