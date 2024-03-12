import requests
import time
from bs4 import BeautifulSoup

class InformacionServidor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
    
    def analizar_encabezado_servidor(self):
        for url in self.urls:
            try:
                tiempo_inicio = time.time()
                response = requests.get(url, proxies=self.proxies)
                tiempo_fin = time.time()
                print(response.text)
                
                servidor = response.headers.get('Server', 'Desconocido')
                print(f"\nInformación del servidor: {servidor}")

                tiempo_respuesta = tiempo_fin - tiempo_inicio
                print(f"Tiempo de respuesta: {tiempo_respuesta} segundos")

                headers_seguridad = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Content-Type-Options', 'X-Frame-Options', 'X-XSS-Protection']
                print("Encabezados de seguridad:")
                for header in headers_seguridad:
                    print(f"{header}: {response.headers.get(header, 'No establecido, posible vulnerabilidad.')}")

                robots_txt_url = url + '/robots.txt'
                robots_txt_response = requests.get(robots_txt_url, proxies=self.proxies)
                if robots_txt_response.status_code == 200:
                    print(f"robots.txt: {robots_txt_response.text}")
                else:
                    print("No se encontró robots.txt.")
            except requests.exceptions.RequestException as e:
                print(f"Se produjo un error: {e}")
    
    def analizar_mensajes_error_redireccion(self):
        mensajes_error = {
            "Apache": [
                "Not Found",
                "HTTP Error 404"
            ],
            "Nginx": [
                "404 Not Found",
                "404 Not Found\n\nnginx/1.14.0 (Ubuntu)",
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
            ]
        }

        for url in self.urls:
            try:
                url_no_existente = url + '/paginanoexistente'
                response = requests.get(url_no_existente, proxies=self.proxies)
                if response.status_code == 404:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    if soup.h1 is not None:
                        titulo = soup.h1.text.strip()
                        print(f"Título: {titulo}")
                    else:
                        print("No se encontró etiqueta <h1> en el HTML.")
                    
                    if soup.address is not None:
                        direccion = soup.address.text.strip()
                        print(f"Dirección: {direccion}")
                    else:
                        direccion = ""
                    
                    hr_element = soup.find('hr')
                    if hr_element:
                        center_element = hr_element.find_next('center')
                        if center_element:
                            contenido_central = center_element.text.strip()
                            print(f"Contenido central: {contenido_central}")

                            if 'nginx' in contenido_central:
                                print(f"Servidor Nginx detectado en {url}")
                                self.verificar_tipo_servidor(titulo, direccion, "Nginx", mensajes_error)
                        else:
                            print("No se encontró un elemento center en el HTML.")
                            self.verificar_tipo_servidor(titulo, direccion, "Apache", mensajes_error)                      
                    else:
                        print("No se encontró el elemento <hr> en el HTML.")
                        self.verificar_tipo_servidor(titulo, direccion, "Lighttpd", mensajes_error)
                        self.verificar_tipo_servidor(titulo, direccion, "Apache", mensajes_error)
                        self.verificar_tipo_servidor(titulo, direccion, "Nginx", mensajes_error)
  
                else:
                    if "nginx" in response.headers.get('Server', ''):
                        print(f"Servidor Nginx detectado en {url}")
            except Exception as e:
                print(f"Error al acceder a la URL: {url}. {e}")


    def verificar_tipo_servidor(self, titulo, direccion, tipo_servidor, mensajes_error):
        for mensaje_error in mensajes_error.get(tipo_servidor, []):
            if mensaje_error in titulo or (direccion and mensaje_error in direccion):
                print(f"El servidor puede ser del tipo {tipo_servidor}")
                break


if __name__ == "__main__":
    urls = ['http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/']
    informacion_servidor = InformacionServidor(urls)
    # informacion_servidor.analizar_encabezado_servidor()
    informacion_servidor.analizar_mensajes_error_redireccion()
