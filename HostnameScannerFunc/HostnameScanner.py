import requests
import socks
import socket
from tqdm import tqdm

class HostnameScannerClass:
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
            return None

    def scan_hostnames(self):
        results = {}
        try:
            for onion_domain in tqdm(self.onion_domains, desc="Scanning URLs for Hostname Vulnerability"):
                try:
                    # Make request to the original .onion domain
                    response_normal = self.make_tor_request(onion_domain)

                    # Modify the 'Host' header for Hostname Hacking technique
                    headers = {'Host': 'localhost'}
                    response_hacked = requests.get(onion_domain, headers=headers, proxies=self.proxies)

                    # Compare responses to detect differences
                    if response_normal is None:
                        results[onion_domain] = {
                            'Result': f'The service at {onion_domain} is not accessible',
                            'Vulnerable to Hostname': False
                        }
                    elif response_hacked.text != response_normal.text:
                        results[onion_domain] = {
                            'Result': f'The service at {onion_domain} is vulnerable to Hostname Hacking',
                            'Vulnerable to Hostname': True
                        }
                    else:
                        results[onion_domain] = {
                            'Result': f'The service at {onion_domain} is not vulnerable to Hostname Hacking',
                            'Vulnerable to Hostname': False
                        }
                except Exception as e:
                    results[onion_domain] = {
                        'Result': f'Error occurred: {e}',
                        'Vulnerable to Hostname': False
                    }

            # Return the result as a dictionary
            return results

        except Exception as e:
            results["Error"] = "Error occurred while scanning the pages"
            return results


if __name__ == "__main__":
    # Sample list of .onion URLs
    onion_domains = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html',
        'a',
        'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/'
    ]

    # Test the function with the list of URLs
    scanner = HostnameScannerClass(onion_domains)
    result = scanner.scan_hostnames()
    print(result)
