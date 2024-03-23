import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading

class ValidacionInput:
    def __init__(self, onion_url, tor_proxy="socks5h://127.0.0.1:9050"):
        self.onion_url = onion_url
        self.tor_proxy = tor_proxy
        self.session = requests.Session()
        self.session.proxies = {
            'http': self.tor_proxy,
            'https': self.tor_proxy
        }

    def get_form_inputs(self):
        response = self.session.get(self.onion_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')

        for form in forms:
            inputs = form.find_all('input')
            for input in inputs:
                yield input.get('name')

    def test_input(self, input_name, test_value):
        response = self.session.get(self.onion_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form', {'method': 'post'})
        action = form['action']
        method = form['method']

        if method == "post":
            res = self.session.post(urljoin(self.onion_url, action), data={input_name: test_value},
                                    proxies=self.session.proxies, allow_redirects=True)
        elif method == "get":
            res = self.session.get(urljoin(self.onion_url, action), params={input_name: test_value},
                                   proxies=self.session.proxies, allow_redirects=True)

        print(f"La prueba para el input {input_name} ha devuelto el código de estado HTTP {res.status_code}.")
        print("Respuesta del servidor:")
        print(response.text)

    def run_tests(self):
        threads = []
        for input_name in self.get_form_inputs():
            # Prueba con entradas muy largas
            thread = threading.Thread(target=self.test_input, args=(input_name, "A" * 10000))
            threads.append(thread)
            thread.start()

            # Prueba con números fuera de rango
            thread = threading.Thread(target=self.test_input, args=(input_name, 1000000000))
            threads.append(thread)
            thread.start()

            # Prueba con fechas/horas incorrectas
            thread = threading.Thread(target=self.test_input, args=(input_name, "30-02-2023"))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

# Cambios en el uso de la clase para conectarse a .onion
onion_url = input("Por favor, introduce la URL del sitio .onion: ")
pentester = ValidacionInput(onion_url, tor_proxy="socks5h://127.0.0.1:9050")
pentester.run_tests()
