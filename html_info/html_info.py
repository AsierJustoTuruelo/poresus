from bs4 import BeautifulSoup, Comment
import requests
import time

class ServerInfo:
    def __init__(self, url):
        self.url = url
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def analyze_page_content(self):
        try:
            response = requests.get(self.url, proxies=self.proxies)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all comments
            print("-------------------------------------------------------------------------------------------")
            comments = soup.findAll(string=lambda text: isinstance(text, Comment))
            print(f"Comments for {self.url}:\n")
            for comment in comments:
                print("[+]" + comment)
            print("-------------------------------------------------------------------------------------------")

            # Find all script tags
            scripts = soup.find_all('script')
            print(f"\nScripts for {self.url}:\n")
            for script in scripts:
                print(script)
            
            # Find all meta tags
            print("-------------------------------------------------------------------------------------------")
            metas = soup.find_all('meta')
            print(f"\nMeta tags for {self.url}:\n")
            for meta in metas:
                print(meta)

            # Find hidden elements
            print("-------------------------------------------------------------------------------------------")
            hidden_elements = soup.find_all(style=lambda value: 'display:none' in value or 'visibility:hidden' in value if value is not None else False)
            print(f"\nHidden elements for {self.url}:\n")
            for hidden_element in hidden_elements:
                print(hidden_element)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    onion_url = input("Ingrese la URL del sitio .onion que desea analizar: ")
    server_info = ServerInfo(onion_url)
    server_info.analyze_page_content()
