import requests
import re
import socks
import socket
import json

class HtmlPhoneExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def fetch_html_and_extract_phones(self):
        results = []
        for url in self.urls:
            try:
                # Configuración del proxy para las solicitudes
                socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
                socket.socket = socks.socksocket

                response = requests.get(url, proxies=self.proxies)
                if response.status_code == 200:
                    html_content = response.text
                    phones_found = self._extract_phones(html_content)
                    results.extend(phones_found)
                else:
                    print(f"Error al hacer la solicitud para {url}. Código de estado: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error al hacer la solicitud para {url}: {e}")
        return json.dumps({"Phone_numbers": results}, indent=2)

    def _extract_phones(self, html_content):
        # Expresión regular para buscar números de teléfono en cualquier formato internacional
        phone_pattern = r'(?<!\d)(?<!\d-)(?<!\d\s)(?:\+\d{1,3}\s?)?(?:\(\d{1,4}\)\s*|\d{1,4}[-. ]?)?\d{1,4}[-. ]?\d{1,4}[-. ]?\d{1,4}(?!\d)'
        
        # Buscar números de teléfono
        phones_found = re.findall(phone_pattern, html_content)
        
        return phones_found

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/phone_numbers/phone_numbers.html"
    ]
    extractor = HtmlPhoneExtractor(urls)
    phones_json = extractor.fetch_html_and_extract_phones()
    print(phones_json)
