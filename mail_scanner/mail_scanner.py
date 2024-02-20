import requests
import re
import socks
import socket

class HtmlEmailExtractor:
    def __init__(self, url):
        self.url = url
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def fetch_html_and_extract_emails(self):
        try:
            # Configuración del proxy para las solicitudes
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(self.url, proxies=self.proxies)
            if response.status_code == 200:
                html_content = response.text
                emails_found = self._extract_emails(html_content)
                return emails_found
            else:
                print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return []

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
    url = input("Enter URL: ")
    extractor = HtmlEmailExtractor(url)
    emails = extractor.fetch_html_and_extract_emails()
    print("Emails found:", emails)