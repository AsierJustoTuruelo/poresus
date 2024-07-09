import re
import requests
import json
from tqdm import tqdm

class PHPServerInfoScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def make_tor_request(self, url):
        try:
            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            return None

    def find_php_files(self, html_content):
        pattern = r'([^"]+\.php(?:\?[^"]*)?)'
        php_files = re.findall(pattern, html_content)
        return php_files

    def extract_filename(self, url):
        return url.split('/')[-1]

    def scan_php_server_info(self):
        results = {}
        for url in tqdm(self.urls, desc="Scanning URLs for PHP Server Info"):
            try:
                base_page_response = self.make_tor_request(url)
                if base_page_response is None:
                    results[url] = {
                        "Error": "Unable to access URL"
                    }
                    continue

                html_content = base_page_response.text
                php_files = self.find_php_files(html_content)

                if not php_files:
                    results[url] = {
                        "Error": "No PHP files found on the page"
                    }
                    continue

                for php_file in php_files:
                    if php_file.endswith('.php'):
                        # Replace the last segment of the URL with the found PHP file
                        url_parts = url.rsplit('/', 1)
                        php_url = url_parts[0] + '/' + php_file
                        response = self.make_tor_request(php_url)
                        php_content = response.text
                        
                        sensitive_info = []
                        if 'IP' in php_content:
                            sensitive_info.append('IP addresses')
                        if 'PHP' in php_content:
                            sensitive_info.append('PHP version')
                        if '.com' in php_content:
                            sensitive_info.append('Domain names')
                        if 'Server' in php_content or 'Servidor' in php_content:
                            sensitive_info.append('Server information')
                        if 'Debian' in php_content:
                            sensitive_info.append('Debian OS information')
                        if 'onion' in php_content:
                            sensitive_info.append('Onion URLs')
                        if 'password' in php_content:
                            sensitive_info.append('Passwords')
                        if 'login' in php_content:
                            sensitive_info.append('Login credentials')
                        if 'username' in php_content:
                            sensitive_info.append('Usernames')
                        
                        if sensitive_info:
                            results[url] = {
                                "Exposes sensitive information": True,
                                "Sensitive information": sensitive_info
                            }
                        else:
                            results[url] = {
                                "Exposes sensitive information": False,
                                "Sensitive information": []
                            }
                            
            except Exception as e:
                results[url] = {
                    "Error": "Unable to access URL"
                }
        
        return results

    def to_json(self, results):
        return json.dumps(results)

if __name__ == "__main__":
    # Lista de URLs donde se alojan los archivos PHP
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/php_info/php_info.html',"a",
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/"
        # Add more URLs here
    ]

    # Crear instancia del escáner
    scanner = PHPServerInfoScanner(urls)

    # Probar la exposición de phpinfo() en los archivos PHP encontrados
    results = scanner.scan_php_server_info()

    # Convertir los resultados a formato JSON
    json_results = scanner.to_json(results)

    # Imprimir los resultados JSON
    print(json_results)
