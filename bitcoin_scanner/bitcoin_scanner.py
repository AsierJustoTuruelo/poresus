import requests
import re
import socks
import socket
import json
from tqdm import tqdm

class BitcoinAddressExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def extract_bitcoin_addresses(self):
        addresses_found = {}
        try:
            # Proxy configuration for requests
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            for url in tqdm(self.urls, desc="Scanning URLs for Bitcoin Addresses"):
                try:
                    response = requests.get(url, proxies=self.proxies, timeout=10)
                    if response.status_code == 200:
                        html_content = response.text
                        addresses = self.find_addresses(html_content)
                        addresses_found[url] = addresses
                    else:
                        print(f"Error making request to {url}. Status code: {response.status_code}")
                except requests.RequestException as e:
                    addresses_found[url] = "The URL is not accessible through Tor"
        except Exception as e:
            addresses_found[url] = "Unknown error"

        if not addresses_found:
            addresses_found = {"Not found"}

        return addresses_found

    def find_addresses(self, html_content):
        # Regular expressions to search for Bitcoin addresses
        bitcoin_address_legacy_pattern = r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}'
        bitcoin_address_segwit_pattern = r'3[a-km-zA-HJ-NP-Z1-9]{25,34}'
        bitcoin_address_bech32_pattern = r'bc1[a-z0-9]{14,74}'

        # Search for Bitcoin addresses in the HTML
        addresses_found_legacy = re.findall(bitcoin_address_legacy_pattern, html_content)
        addresses_found_segwit = re.findall(bitcoin_address_segwit_pattern, html_content)
        addresses_found_bech32 = re.findall(bitcoin_address_bech32_pattern, html_content)

        # Use a set to avoid duplicate addresses
        addresses_found_set = set(addresses_found_legacy + addresses_found_segwit + addresses_found_bech32)

        if not addresses_found_set:
            addresses_found_set.add("No bitcoins found at this URL")

        return list(addresses_found_set)

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/bitcoin_address/bitcoin_adress.html",
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/",
        "aaa"
    ]
    extractor = BitcoinAddressExtractor(urls)
    addresses = extractor.extract_bitcoin_addresses()
    
    result = {
        "Bitcoin Addresses": addresses
    }
    result_json = json.dumps(result, indent=4)
    print(result_json)
