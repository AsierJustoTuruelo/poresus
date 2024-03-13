import requests
from bs4 import BeautifulSoup
import json
from collections import Counter

class InformacionServidor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
    
    def analizar_servidor(self):
        resultados = []
        for url in self.urls:
            try:
                response = requests.get(url, proxies=self.proxies)
                response2 = requests.get(url+"/nonexistent", proxies=self.proxies)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    soup2 = BeautifulSoup(response2.text, 'html.parser')
                    servidor_html = self.detectar_servidor_html(soup)
                    servidor_html2 = self.detectar_servidor_html(soup2)
                    servidor_header = self.detectar_servidor_header(response)
                    servidor_error = self.detectar_servidor_error(response2)
                    servidor_mas_comun = self.detectar_servidor_mas_comun([servidor_html, servidor_html2, servidor_header, servidor_error])
                    resultado = {
                        "url": url,
                        "servidor": servidor_mas_comun
                    }
                    resultados.append(resultado)
                else:
                    resultados.append({"url": url, "error": f"Error al acceder a {url}: {response.status_code}"})
            except Exception as e:
                resultados.append({"url": url, "error": f"Error al acceder a {url}: {e}"})
        return resultados

    def detectar_servidor_html(self, soup):
        text = soup.get_text()
        servidores = {
            "Nginx": "nginx",
            "Apache": "apache",
            "IIS": "iis",
            "Lighttpd": "lighttpd",
            "Caddy": "caddy"
        }
        contador_servidores = Counter()
        for servidor, palabra_clave in servidores.items():
            if palabra_clave in text:
                contador_servidores[servidor] += 1
        return contador_servidores.most_common(1)[0][0] if contador_servidores else None

    def detectar_servidor_header(self, response):
        server_header = response.headers.get('Server', '')
        servidores_conocidos = {
            "Nginx": "nginx",
            "Apache": "apache",
            "IIS": "Microsoft-IIS",
            "Lighttpd": "lighttpd",
            "Caddy": "Caddy"
        }
        for servidor, identificador in servidores_conocidos.items():
            if identificador in server_header:
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
        return contador_servidores.most_common(1)[0][0] if contador_servidores else None

if __name__ == "__main__":
    urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/php_info/php_info.html']
    informacion_servidor = InformacionServidor(urls)
    resultados = informacion_servidor.analizar_servidor()
    print(json.dumps(resultados, indent=4))
