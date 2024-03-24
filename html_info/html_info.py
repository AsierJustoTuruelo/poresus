from bs4 import BeautifulSoup, Comment
import requests
import json
import os

class ServerInfo:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def analyze_page_content(self):
        try:
            last_url = self.urls[-1]
            response = requests.get(last_url, proxies=self.proxies)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all comments
            comments = soup.findAll(string=lambda text: isinstance(text, Comment))
            comments_list = [comment for comment in comments]

            # Find all script tags
            scripts = soup.find_all('script')
            script_names = [os.path.basename(script['src']) for script in scripts if script.get('src')]

            # Find all meta tags
            metas = soup.find_all('meta')
            metas_list = [str(meta) for meta in metas]

            # Find hidden elements
            hidden_elements = soup.find_all(style=lambda value: 'display:none' in value or 'visibility:hidden' in value if value is not None else False)
            hidden_elements_list = [str(hidden_element) for hidden_element in hidden_elements]

            result = {
                'comments': comments_list,
                'scripts': script_names,
                'metas': metas_list,
                'hidden_elements': hidden_elements_list
            }

            # Devuelve el resultado como JSON
            return json.dumps(result)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Lista de URLs .onion de ejemplo
    onion_urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/google_ap/google_ap.html'
    ]
    
    server_info = ServerInfo(onion_urls)
    result = server_info.analyze_page_content()
    print(result)
