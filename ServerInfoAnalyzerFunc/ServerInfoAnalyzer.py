import requests
from bs4 import BeautifulSoup
import json
from collections import Counter
from tqdm import tqdm

class ServerInfoAnalyzer:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
    
    def get_server_info(self):
        resultados = {}
        for url in tqdm(self.urls, desc="Scanning URLs for Server Info"):
            try:
                response = requests.get(url, proxies=self.proxies)
                response2 = requests.get(url+"/nonexistent", proxies=self.proxies)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    soup2 = BeautifulSoup(response2.text, 'html.parser')
                    servidores_detectados = []

                    servidor_html = self.detectar_servidor_html(soup)
                    if servidor_html:
                        servidores_detectados.append(servidor_html)

                    servidor_html2 = self.detectar_servidor_html(soup2)
                    if servidor_html2:
                        servidores_detectados.append(servidor_html2)

                    servidor_header = self.detectar_servidor_header(response)
                    if servidor_header:
                        resultados[url] = {
                            "Server Type": servidor_header
                        }
                        continue

                    servidor_error = self.detectar_servidor_error(response2)
                    if servidor_error:
                        servidores_detectados.append(servidor_error)

                    servidor_mas_comun = self.detectar_servidor_mas_comun(servidores_detectados)
                    resultados[url] = {
                        "Server Type": servidor_mas_comun
                    }
                else:
                    resultados[url] = {"Error": f"Error accessing URL. Status Code: {response.status_code}"}
            except Exception as e:
                resultados[url] = {"Error": f"Error accessing URL: {str(e)}"}
        return resultados

    def detectar_servidor_html(self, soup):
        text = soup.get_text().lower()  # Convertir el texto a minúsculas para hacer coincidencias de forma insensible a mayúsculas
        servidores = {
            "Nginx": "nginx",
            "Apache": "apache",
            "IIS": "iis",
            "Lighttpd": "lighttpd",
            "Caddy": "caddy",
            "Tomcat": "apache tomcat",
            "Express": "express"
        }
        contador_servidores = Counter()
        for servidor, palabra_clave in servidores.items():
            if text.find(palabra_clave) != -1:
                contador_servidores[servidor] += 1
        return contador_servidores.most_common(1)[0][0] if contador_servidores else None

    def detectar_servidor_header(self, response):
        server_header = response.headers.get('Server', '')
        servidores_conocidos = {
            "Nginx": "nginx",
            "Apache": "apache",
            "IIS": "Microsoft-IIS",
            "Lighttpd": "lighttpd",
            "Caddy": "Caddy",
            "Tomcat": "Apache-Coyote",
            "Express": "Express"
        }
        for servidor, identificador in servidores_conocidos.items():
            if identificador.lower() in server_header.lower():
                return servidor
        return None

    def detectar_servidor_error(self, response):
        errores_conocidos = {
            "Apache": [
                "Not Found",
                "HTTP Error 404"
            ],
            "Nginx": [
                "404 Not Found",
                "404 Not Found\n\nnginx/1.14.0 (Ubuntu)",
                "404 Not Found\n\nnginx/1.24.0",
                "No se puede encontrar la página\n\nnginx",
                "Error 404\n\nNot Found\n\nnginx",
                "Not Found"
            ],
            "IIS": [
                "HTTP Error 404.0 - Not Found",
                "The resource you are looking for has been removed, had its name changed, or is temporarily unavailable.",
                "404 - File or directory not found."
            ],
            "Lighttpd": [
                "404 Not Found",
                "404 Not Found\n",
                "404 Not Found</h1>",
                "404 Not Found</html>"
            ],
            "Caddy": [
                "Caddy error"
            ],
            "Tomcat": [
                "Apache Tomcat Error Report",
                "HTTP Status 404",
                "Apache Tomcat/8.5.69",
                "Apache Tomcat/9.0.0"
            ],
            "Express": [
                "Cannot GET /nonexistent"
            ]
        }
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        contador_servidores = Counter()
        for servidor, errores in errores_conocidos.items():
            for error in errores:
                if error in text:
                    contador_servidores[servidor] += 1
        return contador_servidores.most_common(1)[0][0] if contador_servidores else None

    def detectar_servidor_mas_comun(self, servidores):
        contador_servidores = Counter(servidores)
        return contador_servidores.most_common(1)[0][0] if contador_servidores else ""

if __name__ == "__main__":
    urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/php_info/php_info.html',"a"]
    informacion_servidor = ServerInfoAnalyzer(urls)
    resultados = informacion_servidor.get_server_info()
    print(json.dumps(resultados, indent=4))
