from bs4 import BeautifulSoup, Comment
import requests
import json
import os
from tqdm import tqdm

class HtmlInfoExtractor:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def analyze_html(self):
        all_results = {}
        for url in tqdm(self.urls, desc="Scanning URLs for HTML information"):  
            try:
                response = requests.get(url, proxies=self.proxies)
                response.raise_for_status()
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
                    'Comments': comments_list,
                    'Scrips': script_names,
                    'Metas': metas_list,
                    'Hidden Elements': hidden_elements_list
                }

                all_results[url] = result
            except requests.exceptions.RequestException as e:
                all_results[url] = {"Error": str(e)}  # Manejo de errores: agregar el error al resultado

        # Devuelve el resultado completo como JSON
        return all_results

if __name__ == "__main__":
    # Lista de URLs .onion de ejemplo
    onion_urls = [
        "http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/image_metadata/metadata.html","a","http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/"
    ]
    
    server_info = HtmlInfoExtractor(onion_urls)
    result = server_info.analyze_html()
    print(json.dumps(result, indent=4))
