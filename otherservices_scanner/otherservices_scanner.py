import requests
import re
import socks
import socket
import json

class OnionServiceAnalyzer:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def analyze_services(self):
        results = {}
        for url in self.urls:
            try:
                # Configuración del proxy para las solicitudes
                socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
                socket.socket = socks.socksocket

                response = requests.get(url, proxies=self.proxies)
                if response.status_code == 200:
                    html_content = response.text
                    # Realizar análisis de otros servicios
                    ssh_found = self._analyze_ssh(html_content)
                    ftp_found = self._analyze_ftp(html_content)
                    smtp_found = self._analyze_smtp(html_content)
                    http_traces_found = self._analyze_http_traces(html_content)

                    result = {
                        "ssh_found": ssh_found,
                        "ftp_found": ftp_found,
                        "smtp_found": smtp_found,
                        "http_traces_found": http_traces_found
                    }
                    results = result
                else:
                    print(f"Error al hacer la solicitud para {url}. Código de estado: {response.status_code}")
                    results[url] = {
                        "error": f"Error al hacer la solicitud. Código de estado: {response.status_code}"
                    }
            except requests.RequestException as e:
                print(f"Error al hacer la solicitud para {url}: {e}")
                results[url] = {
                    "error": f"Error al hacer la solicitud: {e}"
                }
        return json.dumps(results, indent=2)

    def _analyze_ssh(self, html_content):
        # Lógica para analizar presencia de SSH
        ssh_found = "ssh://" in html_content
        return ssh_found
    
    def _analyze_ftp(self, html_content):
        # Lógica para analizar presencia de FTP
        ftp_found = "ftp://" in html_content
        return ftp_found
    
    def _analyze_smtp(self, html_content):
        # Lógica para analizar presencia de SMTP
        smtp_found = "smtp://" in html_content
        return smtp_found
    
    def _analyze_http_traces(self, html_content):
        # Lógica para analizar rastreos HTTP
        http_traces_found = "http://" in html_content or "https://" in html_content
        return http_traces_found

if __name__ == "__main__":
    urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/otherservices/otherservices.html"
    ]
    analyzer = OnionServiceAnalyzer(urls)
    result = analyzer.analyze_services()
    print(result)
