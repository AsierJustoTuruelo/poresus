import requests
import re
import socks
import socket
import json

class HtmlPhoneExtractor:
    def __init__(self, url):
        self.url = url
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def fetch_html_and_extract_phones(self):
        try:
            # Configuración del proxy para las solicitudes
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(self.url, proxies=self.proxies)
            if response.status_code == 200:
                html_content = response.text
                phones_found = self._extract_phones(html_content)
                return phones_found
            else:
                print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return []

    def _extract_phones(self, html_content):
        # Expresión regular para buscar números de teléfono en cualquier formato internacional
        phone_pattern = r'(?<!\d)(?<!\d-)(?<!\d\s)(?:\+\d{1,3}\s?)?(?:\(\d{1,4}\)\s*|\d{1,4}[-. ]?)?\d{1,4}[-. ]?\d{1,4}[-. ]?\d{1,4}(?!\d)'
        
        # Buscar números de teléfono
        phones_found = re.findall(phone_pattern, html_content)
        
        # Convertir los números de teléfono encontrados a JSON
        phones_json = json.dumps({"Phone_numbers": phones_found})
        
        return phones_json

if __name__ == "__main__":
    url = input("Ingrese la URL: ")
    extractor = HtmlPhoneExtractor(url)
    phones_json = extractor.fetch_html_and_extract_phones()
    print("Números de teléfono encontrados:")
    print(phones_json)
