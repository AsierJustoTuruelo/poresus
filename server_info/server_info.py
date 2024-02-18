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
    
    def analyze_error_messages_redirection(self):
        error_arrays = {
            "Apache": [
                "Not Found",
                "HTTP Error 404"
            ],
            "Nginx": [
                "404 Not Found",
                "404 Not Found\n\nnginx/1.14.0 (Ubuntu)",
                "No se puede encontrar la página\n\nnginx",
                "Error 404\n\nNot Found\n\nnginx"
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

        print("\nError messages:")
        for url in self.urls:
            try:
                # Añade una ruta inexistente a la URL
                nonexistent_url = url + '/nonexistentpage'
                response = requests.get(nonexistent_url, proxies=self.proxies)
                print(response.text)
                # Si el servidor devuelve un error 404, extrae el contenido del elemento <h1> y <address>
                if response.status_code == 404:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.h1.text.strip()
                    print(f"Title: {title}")
                    address = soup.address.text.strip() if soup.address else ""
                    print(f"Address: {address}")

                    # Busca si existe un elemento <hr>
                    hr_element = soup.find('hr')
                    if hr_element:
                        center_element = hr_element.find_next('center')
                        if center_element:
                            center_content = center_element.text.strip()
                            print(f"Center content: {center_content}")

                            # Verifica si el texto contiene la cadena 'nginx'
                            if 'nginx' in center_content:
                                print(f"Nginx server detected at {url}")
                                self.check_server_type(title, address, "Nginx", error_arrays)
                        else:
                            # Si no existe un center element, puede ser un Apache o Lighttpd server
                            print("No center element found in the HTML.")
                            self.check_server_type(title, address, "Apache", error_arrays)
                              
                    else:
                        print("No hr element found in the HTML.")
                        self.check_server_type(title, address, "Lighttpd", error_arrays)  
            except Exception as e:
                print(f"Error accessing URL: {url}. {e}")

    def check_server_type(self, title, address, server_type, error_arrays):
        for error_message in error_arrays.get(server_type, []):
            if error_message in title or (address and error_message in address):
                print(f"The server at  seems to be of type {server_type}")
                break


if __name__ == "__main__":
    urls = ['http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/']
    server_info = ServerInfo(urls)
    #server_info.analyze_server_header()
    server_info.analyze_error_messages_redirection()
