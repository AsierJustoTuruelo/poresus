import requests
import re
import socks
import socket
import json
from tqdm import tqdm

class OtherServicesAnalyzerClass:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def analyze_services(self):
        results = {}
        for url in tqdm(self.urls, desc="Scanning URLs for Other Services"):
            try:
                # Proxy configuration for requests
                socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
                socket.socket = socks.socksocket

                response = requests.get(url, proxies=self.proxies, timeout=10)  # Add timeout to handle unreachable URLs
                if response.status_code == 200:
                    html_content = response.text
                    # Perform analysis of other services
                    ssh_found = self._analyze_ssh(html_content)
                    ftp_found = self._analyze_ftp(html_content)
                    smtp_found = self._analyze_smtp(html_content)
                    http_traces_found = self._analyze_http_traces(html_content)

                    result = {
                        "SSH Traces Found": ssh_found,
                        "FTP Traces Found": ftp_found,
                        "SMTP Traces Found": smtp_found,
                        "HTTP Traces Found": http_traces_found
                    }
                    results[url] = result
                else:
                    results[url] = {"Error": f"Error accessing URL. Status Code: {response.status_code}"}
            except requests.RequestException as e:
                results[url] = {"Error": str(e)}
        return results

    def _analyze_ssh(self, html_content):
        # Logic to analyze presence of SSH
        ssh_found = "ssh://" in html_content
        return ssh_found
    
    def _analyze_ftp(self, html_content):
        # Logic to analyze presence of FTP
        ftp_found = "ftp://" in html_content
        return ftp_found
    
    def _analyze_smtp(self, html_content):
        # Logic to analyze presence of SMTP
        smtp_found = "smtp://" in html_content
        return smtp_found
    
    def _analyze_http_traces(self, html_content):
        # Logic to analyze HTTP traces
        http_traces_found = "http://" in html_content or "https://" in html_content
        return http_traces_found

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/otherservices/otherservices.html",
        "a",
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/"
    ]
    analyzer = OtherServicesAnalyzerClass(urls)
    result = analyzer.analyze_services()
    print(json.dumps(result, indent=2))
