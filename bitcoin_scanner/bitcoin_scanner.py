import requests
import re
import socks
import socket

class BitcoinAddressExtractor:
    def __init__(self, url):
        self.url = url
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def fetch_html_and_extract_addresses(self):
        try:
            # Configuración del proxy para las solicitudes
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(self.url, proxies=self.proxies)
            if response.status_code == 200:
                html_content = response.text
                addresses_found = self._extract_addresses(html_content)
                return addresses_found
            else:
                print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return []

    def _extract_addresses(self, html_content):
        # Expresiones regulares para buscar direcciones Bitcoin
        bitcoin_address_legacy_pattern = r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}'
        bitcoin_address_segwit_pattern = r'3[a-km-zA-HJ-NP-Z1-9]{25,34}'
        bitcoin_address_bech32_pattern = r'bc1[a-z0-9]{14,74}'  # El rango 14-74 es para cubrir todos los posibles casos de bech32

        # Buscar direcciones Bitcoin en el HTML
        addresses_found_legacy = re.findall(bitcoin_address_legacy_pattern, html_content)
        addresses_found_segwit = re.findall(bitcoin_address_segwit_pattern, html_content)
        addresses_found_bech32 = re.findall(bitcoin_address_bech32_pattern, html_content)

        # Utilizar un conjunto para evitar direcciones duplicadas
        addresses_found_set = set(addresses_found_legacy + addresses_found_segwit + addresses_found_bech32)

        return list(addresses_found_set)



if __name__ == "__main__":
    url = input("Ingrese la URL para buscar direcciones Bitcoin: ")
    extractor = BitcoinAddressExtractor(url)
    addresses = extractor.fetch_html_and_extract_addresses()
    
    if addresses:
        print("Direcciones Bitcoin encontradas:")
        for address in addresses:
            print(address)
    else:
        print("No se encontraron direcciones Bitcoin en la página.")