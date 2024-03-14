import socks
import socket
import json

class PortScanner:
    def __init__(self, url):
        self.url = url
        self.open_ports = []
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def scan_ports(self, ports, timeout=1):
        # Configuración del proxy Tor
        socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket

        # Quita el prefijo 'http://' si está presente en la URL
        if self.url.startswith('http://'):
            self.url = self.url[len('http://'):]

        # Quitar el sufijo '/' si está presente en la URL
        if self.url.endswith('/'):
            self.url = self.url[:-1]

        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(timeout)  # Establece el tiempo de espera para esta conexión de socket
                    result = s.connect_ex((self.url, port))
                    if result == 0:
                        self.open_ports.append(port)
            except Exception as e:
                pass
                #print(f"Error scanning port {port}: {e}")

    def get_open_ports_as_json(self):
        return json.dumps({"open_ports": self.open_ports}, indent=4)

if __name__ == "__main__":
    url = input("Enter URL: ")
    ports_to_scan = [21, 22, 80, 443, 9050]  # Example list of ports to scan
    scanner = PortScanner(url)
    scanner.scan_ports(ports_to_scan, timeout=2)  # Cambia el tiempo de espera a 2 segundos
    print(scanner.get_open_ports_as_json())
