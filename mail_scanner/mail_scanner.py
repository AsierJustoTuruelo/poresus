import requests
import re
import socks
import socket
import json

class HtmlEmailExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def fetch_html_and_extract_emails(self):
        results = {}
        for url in self.urls:
            try:
                # Configuración del proxy para las solicitudes
                socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
                socket.socket = socks.socksocket

                response = requests.get(url, proxies=self.proxies)
                if response.status_code == 200:
                    html_content = response.text
                    emails_found = self._extract_emails(html_content)
                    results = {"emails": emails_found}
                else:
                    print(f"Error al hacer la solicitud para {url}. Código de estado: {response.status_code}")
                    results[url] = {"error": f"Código de estado: {response.status_code}"}
            except requests.RequestException as e:
                print(f"Error al hacer la solicitud para {url}: {e}")
                results[url] = {"error": str(e)}
        return results

    def _extract_emails(self, html_content):
        # Expresión regular para buscar direcciones de correo electrónico y enlaces mailto:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        mailto_pattern = r'mailto:([^\s]+)'
        
        # Buscar direcciones de correo electrónico normales
        emails_found = re.findall(email_pattern, html_content)
        
        # Buscar direcciones de correo electrónico en enlaces mailto:
        mailtos_found = re.findall(mailto_pattern, html_content)
        
        # Añadir las direcciones de correo electrónico de los enlaces mailto: encontrados
        for mailto in mailtos_found:
            # Asegurar que hay al menos dos partes después de la división
            parts = mailto.split(':')
            if len(parts) > 1:
                email = parts[1]
                emails_found.append(email)
        
        return emails_found

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/mailweb/mailweb.html"
    ]
    extractor = HtmlEmailExtractor(urls)
    emails = extractor.fetch_html_and_extract_emails()
    print(json.dumps(emails, indent=2))
