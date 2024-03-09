import requests
import socks
import socket
import json

class HostnameHackingScanner:
    def __init__(self, onion_domain):
        self.onion_domain = onion_domain
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

    def test_hostname_hacking(self):
        try:
            # Realizar la solicitud al dominio .onion original
            response_normal = self.make_tor_request(self.onion_domain)

            # Modificar el encabezado 'Host' para la técnica de Hostname Hacking
            headers = {'Host': 'localhost'}
            response_hacked = requests.get(self.onion_domain, headers=headers, proxies=self.proxies)

            # Compara las respuestas para detectar diferencias
            if response_hacked.text != response_normal.text:
                result = {
                    'message': f'El servicio en {self.onion_domain} es vulnerable a Hostname Hacking',
                    'hostname_vuln': True
                }
            else:
                result = {
                    'message': f'El servicio en {self.onion_domain} no es vulnerable a Hostname Hacking',
                    'hostname_vuln': False
                }
            
            # Devuelve el resultado como JSON
            return json.dumps(result)

        except Exception as e:
            print(f"Error al escanear la página: {e}")
            return None

if __name__ == "__main__":
    # Prueba la función con el dominio .onion de tu elección
    scanner = HostnameHackingScanner('http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/')
    result = scanner.test_hostname_hacking()
    print(result)
