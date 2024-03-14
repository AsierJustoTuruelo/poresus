import re
import json
import socks
import socket
import requests
from bs4 import BeautifulSoup

class ServerStatusChecker:
    def __init__(self, url):
        self.url = url
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            print(f"Error al hacer la solicitud a través de Tor: {e}")
            return None

    def extract_ip_from_html(self, html):
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', html)
        if ips:
            return list(set(ips))
        return None

    def extract_server_from_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        server_tags = soup.find_all('address')
        servers = [tag.text.strip() for tag in server_tags]
        return servers

    def check_server_status(self):
        try:
            # Realizar la solicitud a la URL dada
            response = self.make_tor_request(self.url + "/server-status")
            if response is None:
                print("No se pudo obtener la respuesta de la página.")
                return

            # Verificar si la URL /server-status está disponible
            if response.status_code == 200:
                print("La URL /server-status está disponible.")
                ip_addresses = self.extract_ip_from_html(response.text)
                servers = self.extract_server_from_html(response.text)
                
                result = {
                    "IP_addresses": ip_addresses,
                    "Servers": servers
                }

                print(json.dumps(result, indent=4))
            else:
                print("La URL /server-status no está disponible.")
            
        except Exception as e:
            print(f"Error al verificar la URL /server-status: {e}")

if __name__ == "__main__":
    # Prueba la función con la URL de tu elección
    checker = ServerStatusChecker('http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/')
    checker.check_server_status()
