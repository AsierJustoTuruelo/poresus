import requests
import socks
import socket
import json

class HostnameHackingScanner:
    def __init__(self, onion_domains):
        self.onion_domains = onion_domains
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

    def scan_hostnames(self):
        try:
            results = []
            for onion_domain in self.onion_domains:
                # Realizar la solicitud al dominio .onion original
                response_normal = self.make_tor_request(onion_domain)

                # Modificar el encabezado 'Host' para la técnica de Hostname Hacking
                headers = {'Host': 'localhost'}
                response_hacked = requests.get(onion_domain, headers=headers, proxies=self.proxies)

                # Compara las respuestas para detectar diferencias
                if response_hacked.text != response_normal.text:
                    result = {
                        'resultado': f'El servicio en {onion_domain} es vulnerable a Hostname Hacking',
                        'is_hostname_vulnerable': True
                    }
                else:
                    result = {
                        'resultado': f'El servicio en {onion_domain} no es vulnerable a Hostname Hacking',
                        'is_hostname_vulnerable': False
                    }
                results.append(result)

            # Devuelve el resultado como JSON
            return json.dumps(results)

        except Exception as e:
            print(f"Error al escanear la página: {e}")
            return None

if __name__ == "__main__":
    # Lista de URLs .onion de ejemplo
    onion_domains = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/'
    ]

    # Prueba la función con la lista de URLs
    scanner = HostnameHackingScanner(onion_domains)
    result = scanner.scan_hostnames()
    print(result)
