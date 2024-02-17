import os
import requests
import time
from bs4 import BeautifulSoup

class ServerInfo:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
    
    def analyze_server_header(self):
        for url in self.urls:
            try:
                start_time = time.time()
                response = requests.get(url, proxies=self.proxies)
                end_time = time.time()
                print(response.text)
                # Server type and version
                server = response.headers.get('Server', 'Unknown')
                print(f"\nServer info: {server}")

                # Response time
                response_time = end_time - start_time
                print(f"Response time: {response_time} seconds")

                # Security headers
                security_headers = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Content-Type-Options', 'X-Frame-Options', 'X-XSS-Protection']
                print("Security headers:")
                for header in security_headers:
                    print(f"{header}: {response.headers.get(header, 'No establecido, posible vulnerabilidad.')}")

                # robots.txt
                robots_txt_url = url + '/robots.txt'
                robots_txt_response = requests.get(robots_txt_url, proxies=self.proxies)
                if robots_txt_response.status_code == 200:
                    print(f"robots.txt: {robots_txt_response.text}")
                else:
                    print("No robots.txt encontrado.")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
    
    def analyze_error_messages(self):
        """ funcion que analiza por si tiene las cabeceras desactivadas y no dan el tipo de servidor """
        apache_errors = [
            "404 Not Found",
            "Not Found\n\nThe requested URL was not found on this server.",
            "Object not found!\n\nThe requested URL was not found on this server.",
            "404 Not Found\n\nThe requested URL was not found on this server."
        ]

        nginx_errors = [
            "404 Not Found",
            "404 Not Found\n\nnginx/1.14.0 (Ubuntu)",
            "No se puede encontrar la página\n\nnginx",
            "Error 404\n\nNot Found\n\nnginx"
        ]

        iis_errors = [
            "HTTP Error 404.0 - Not Found",
            "The resource you are looking for has been removed, had its name changed, or is temporarily unavailable.",
            "404 - File or directory not found."
        ]

        tomcat_errors = [
            "HTTP Status 404 – Not Found\n\nType Status Report\n\nMessage /{requested-url} not found\n\nDescription The origin server did not find a current representation for the target resource or is not willing to disclose that one exists.",
            "HTTP Status 404 - Not Found\n\nThe requested resource is not available.",
            "Error 404\n\n/{requested-url} Not Found."
        ]

        error_arrays = {
            "Apache": apache_errors,
            "Nginx": nginx_errors,
            "IIS": iis_errors,
            "Tomcat": tomcat_errors
        }

        print("\nError messages:")
        for url in self.urls:
            try:
                # Añade una ruta inexistente a la URL
                nonexistent_url = url + '/nonexistentpage'
                response = requests.get(nonexistent_url, proxies=self.proxies)
                print(response.text)
                # Si el servidor devuelve un error 404, extrae el contenido del elemento <title> y <address>
                if response.status_code == 404:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.text.strip()

                    address = ""
                    if soup.address:
                        address = soup.address.text.strip()
                        print(f"Address: {address}")
                    else:
                        print("No address found in the HTML.")

                    # Busca si existe un elemento <hr>
                    hr_element = soup.find('hr')
                    if hr_element:
                        center_content = hr_element.find_next('center').text.strip()
                        print(f"Center content: {center_content}")

                        # Busca si el texto contiene la cadena 'nginx'
                        if 'nginx' in center_content:
                            print(f"Nginx server detected at {url}")

                    # Compara el título y la dirección con los mensajes de error definidos en los arrays
                    for server, error_list in error_arrays.items():
                        for error_message in error_list:
                            if error_message in title or (address and error_message in address):
                                print(f"El servidor en {url} parece ser del tipo {server}")
                                break

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/']
    server_info = ServerInfo(urls)
    #server_info.analyze_server_header()
    server_info.analyze_error_messages()
