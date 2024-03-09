import re
import requests
import json

class PHPServerInfoScanner:
    def __init__(self, url):
        self.url = url
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def make_tor_request(self, url):
        try:
            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            print(f"Error al hacer la solicitud a través de Tor: {e}")
            return None

    def find_php_files(self, html_content):
        pattern = r'([^"]+\.php(?:\?[^"]*)?)'
        php_files = re.findall(pattern, html_content)
        return php_files

    def test_phpinfo_exposure(self):
        results = {}
        try:
            base_page_response = self.make_tor_request(self.url)
            html_content = base_page_response.text
            php_files = self.find_php_files(html_content)

            for php_file in php_files:
                if php_file.endswith('.php'):
                    # Reemplazar el último segmento de la URL con el archivo PHP encontrado
                    url_parts = self.url.rsplit('/', 1)
                    php_url = url_parts[0] + '/' + php_file
                    print(f"Probando {php_url}")
                    response = self.make_tor_request(php_url)
                    php_content = response.text
                    print(php_content)
                    if 'IP' in php_content or 'PHP' in php_content or '.com' in php_content or 'Server' in php_content or 'Debian' in php_content or 'onion' in php_content:
                        results[php_url] = "Exposes sensitive information"
                    else:
                        results[php_url] = "Does not expose sensitive information"

        except Exception as e:
            results['error'] = str(e)
        
        return results

    def to_json(self, results):
        return json.dumps(results)

if __name__ == "__main__":
    # URL base donde se alojan los archivos PHP
    base_url = 'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/php_info/php_info.html'

    # Crear instancia del escáner
    scanner = PHPServerInfoScanner(base_url)

    # Probar la exposición de phpinfo() en los archivos PHP encontrados
    results = scanner.test_phpinfo_exposure()

    # Convertir los resultados a formato JSON
    json_results = scanner.to_json(results)

    # Imprimir los resultados JSON
    print(json_results)
