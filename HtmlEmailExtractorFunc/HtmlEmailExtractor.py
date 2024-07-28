import requests
import re
import socks
import socket
import json
from tqdm import tqdm

class HtmlEmailExtractorClass:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def extract_emails(self):
        results = {}
        for url in tqdm(self.urls, desc="Scanning URLs for Mails"):
            try:
                # Proxy configuration for requests
                socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
                socket.socket = socks.socksocket

                response = requests.get(url, proxies=self.proxies)
                if response.status_code == 200:
                    html_content = response.text
                    emails_found = self.find_mails(html_content)
                    if emails_found:
                        results[url] = {"Emails": emails_found}
                    else:
                        results[url] = {"Error": "No emails found."}
                else:
                    results[url] = {"Error": f"Status Code: {response.status_code}"}
            except requests.RequestException as e:
                results[url] = {"Error": str(e)}
        return results

    def find_mails(self, html_content):
        # Regular expression to find email addresses and mailto: links
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        mailto_pattern = r'mailto:([^\s]+)'
        
        # Find normal email addresses
        emails_found = re.findall(email_pattern, html_content)
        
        # Find email addresses in mailto: links
        mailtos_found = re.findall(mailto_pattern, html_content)
        
        # Add email addresses from found mailto: links
        for mailto in mailtos_found:
            # Ensure there are at least two parts after splitting
            parts = mailto.split(':')
            if len(parts) > 1:
                email = parts[1]
                emails_found.append(email)
        
        return emails_found

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/mailweb/mailweb.html",
        "a",
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/"
    ]
    extractor = HtmlEmailExtractorClass(urls)
    emails = extractor.extract_emails()
    print(json.dumps(emails, indent=2))
