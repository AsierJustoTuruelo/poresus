import requests
import re
import socks
import socket
import json
from tqdm import tqdm

class HtmlPhoneExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def fetch_html_and_extract_phones(self):
        results = {}
        for url in tqdm(self.urls, desc="Extracting Phone Numbers"):
            try:
                # Proxy configuration for requests
                socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
                socket.socket = socks.socksocket

                response = requests.get(url, proxies=self.proxies, timeout=10)  # Add timeout to handle unreachable URLs
                if response.status_code == 200:
                    html_content = response.text
                    phones_found = self._extract_phones(html_content)
                    if phones_found:
                        results[url] = phones_found
                    else:
                        results[url] = "No phones found"
                else:
                    results[url] = {"error": f"Status Code: {response.status_code}"}
            except requests.RequestException as e:
                results[url] = {"error": str(e)}
        return json.dumps({"Phone_numbers": results}, indent=2)

    def _extract_phones(self, html_content):
        # Regular expression to search for phone numbers in any international format
        phone_pattern = r'(?<!\d)(?<!\d-)(?<!\d\s)(?:\+\d{1,3}\s?)?(?:\(\d{1,4}\)\s*|\d{1,4}[-. ]?)?\d{1,4}[-. ]?\d{1,4}[-. ]?\d{1,4}(?!\d)'
        
        # Regular expression to identify date-like patterns (for exclusion)
        date_pattern = r'\b\d{1,4}[./-]\d{1,2}[./-]\d{2,4}\b'
        
        # Search for phone numbers
        phones_found = re.findall(phone_pattern, html_content)
        
        # Filter out any patterns resembling dates
        phones_found = [phone for phone in phones_found if not re.match(date_pattern, phone)]
        
        return phones_found if phones_found else None

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/phone_numbers/phone_numbers.html","a",
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/"
    ]
    extractor = HtmlPhoneExtractor(urls)
    phones_json = extractor.fetch_html_and_extract_phones()
    print(phones_json)
