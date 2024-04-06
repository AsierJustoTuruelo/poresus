import re
import json
import socks
import socket
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

class ServerStatusChecker:
    def __init__(self, urls):
        self.urls = urls
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

    def check_server_status(self, url):
        try:
            # Realizar la solicitud a la URL dada
            response = self.make_tor_request(url + "/server-status")
            if response is None:
                print("No se pudo obtener la respuesta de la página.")
                return {"error": "No se pudo obtener la respuesta de la página."}

            # Verificar si la URL /server-status está disponible
            disponible = response.status_code == 200

            if disponible:
                ip_addresses = self.extract_ip_from_html(response.text)
                servers = self.extract_server_from_html(response.text)
            else:
                ip_addresses = None
                servers = None

            result = {
                "Disponible": disponible,
                "Direcciones IP Encontradas": ip_addresses,
                "Servidores": servers
            }

            return result
            
        except Exception as e:
            print(f"Error al verificar la URL {url}/server-status: {e}")
            return {"error": f"Error al verificar la URL {url}/server-status: {e}"}

    def check_servers_status(self):
        results = {}
        for url in tqdm(self.urls, desc="Checking Servers"):
            result = self.check_server_status(url)
            if result:
                results[url] = result
        return results

if __name__ == "__main__":
    # Prueba la función con una lista de URLs de tu elección
    onion_urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/', 'a'
    ]
    
    checker = ServerStatusChecker(onion_urls)
    results = checker.check_servers_status()
    if results:
        print(json.dumps(results, indent=4))
