import requests
import re
import socks
import socket
import json
from stem import Signal
from stem.control import Controller
from tqdm import tqdm

class GoogleIDsExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def scan_google_services(self):
        results = {}
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            for url in tqdm(self.urls, desc="Scanning URLs for Google Services"):
                try:
                    response = requests.get(url, proxies=self.proxies)
                    if response.status_code == 200:
                        html_content = response.text
                        analytics_ids, publisher_ids = self._extract_google_ids(html_content)
                        if not analytics_ids and not publisher_ids:
                            results[url] = {"analytics_ids": "No Google Analytics or Publisher IDs found"}
                        else:
                            results[url] = {"analytics_ids": analytics_ids, "publisher_ids": publisher_ids}
                    else:
                        results[url] = {"error": f"Error making request. Status code: {response.status_code}"}
                except requests.RequestException as e:
                    results[url] = {"error": f"Error making request: {e}"}
                    continue

            return results
        except Exception as e:
            return {"error": str(e)}

    def _extract_google_ids(self, html_content):
        analytics_id_pattern = r'UA-\d{8}-\d{1,2}'
        publisher_id_pattern = r'pub-\d{16}'

        analytics_ids = re.findall(analytics_id_pattern, html_content)
        publisher_ids = re.findall(publisher_id_pattern, html_content)

        return analytics_ids, publisher_ids

if __name__ == "__main__":
    urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/google_ap/google_ap.html',
        'a', 
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/google_ap/'
    ]
    extractor = GoogleIDsExtractor(urls)
    results = extractor.scan_google_services()
    results_json = json.dumps(results, indent=4)
    print(results_json)
