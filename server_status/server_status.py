import re
import socks
import socket
import requests

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

    def check_server_status(self):
        try:
            # Realizar la solicitud a la URL dada
            response = self.make_tor_request(self.url +  "/server-status")
            if response is None:
                print("No se pudo obtener la respuesta de la página.")
                return

            # Verificar si la URL /server-status está disponible
            if response.status_code == 200:
                print("La URL /server-status está disponible.")
                print(response.text)    
                ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', response.text)
                if ips:
                    unique_ips = set(ips)
                    print("Direcciones IP encontradas en /server-status:")
                    for ip in unique_ips:
                        print(f"{ip}")
                else:
                    print("No se encontraron direcciones IP en la respuesta.")
            else:
                print(response.text)
                print("La URL /server-status no está disponible.")
            
        except Exception as e:
            print(f"Error al verificar la URL /server-status: {e}")

if __name__ == "__main__":
    # Prueba la función con la URL de tu elección
    checker = ServerStatusChecker('http://archiveiya74codqgiixo33q62qlrqtkgmcitqx5u2oeqnmn5bpcbiyd.onion')
    checker.check_server_status()
