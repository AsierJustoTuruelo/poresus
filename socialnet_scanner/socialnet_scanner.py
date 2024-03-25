import re
import json
import socks
import socket
import requests

class RedesSocialesScanner:
    def __init__(self, urls):
        self.urls = urls
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def make_tor_request(self, url):
        try:
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            response = requests.get(url, proxies=self.proxies)
            return response
        except Exception as e:
            print(f"Error al hacer la solicitud a través de Tor: {e}")
            return None

    def extract_social_media(self, text):
        patrones_redes_sociales = {
            'twitter': r'(https?://(?:www\.)?twitter\.com/[\w-]+)|\btwitter\b',
            'facebook': r'(https?://(?:www\.)?facebook\.com/[\w-]+)|\bfacebook\b',
            'instagram': r'(https?://(?:www\.)?instagram\.com/[\w-]+)|\binstagram\b',
            'reddit': r'(https?://(?:www\.)?reddit\.com/r/[\w-]+)|\breddit\b',
            'youtube': r'(https?://(?:www\.)?youtube\.com/[\w-]+)|\byoutube\b',
            'whatsapp': r'(https?://(?:www\.)?wa\.me/[\w-]+)|\bwhatsapp\b',
            'wechat': r'(https?://(?:www\.)?weixin\.qq\.com/[\w-]+)|\bwechat\b',
            'tiktok': r'(https?://(?:www\.)?tiktok\.com/@[\w-]+)|\btiktok\b',
            'linkedin': r'(https?://(?:www\.)?linkedin\.com/in/[\w-]+)|\blinkedin\b',
            'telegram': r'(https?://(?:www\.)?t\.me/[\w-]+)|\btelegram\b',
            'snapchat': r'(https?://(?:www\.)?snapchat\.com/add/[\w-]+)|\bsnapchat\b',
            'pinterest': r'(https?://(?:www\.)?pinterest\.com/[\w-]+)|\bpinterest\b',
            'quora': r'(https?://(?:www\.)?quora\.com/profile/[\w-]+)|\bquora\b',
            'twitch': r'(https?://(?:www\.)?twitch\.tv/[\w-]+)|\btwitch\b',
            'discord': r'(https?://(?:www\.)?discord\.gg/[\w-]+)|\bdiscord\b',
        }

        redes_sociales_encontradas = {}
        for nombre_red_social, patron in patrones_redes_sociales.items():
            matches = re.finditer(patron, text, flags=re.IGNORECASE)
            for match in matches:
                if nombre_red_social not in redes_sociales_encontradas:
                    redes_sociales_encontradas[nombre_red_social] = []
                redes_sociales_encontradas[nombre_red_social].append(match.group(0))

        return redes_sociales_encontradas

    def scan_social_media(self, url):
        try:
            response = self.make_tor_request(url)
            if response is None:
                print(f"No se pudo obtener la respuesta de la página: {url}")
                return None

            if response.status_code == 200:
                social_media_found = self.extract_social_media(response.text)
                return social_media_found
            else:
                print(f"No se pudo acceder a la página: {url}")
                return None
        except Exception as e:
            print(f"Error al escanear redes sociales en {url}: {e}")
            return None

    def scan_social_media_for_all_urls(self):
        results = {}
        for url in self.urls:
            social_media_found = self.scan_social_media(url)
            if social_media_found:
                results = social_media_found
        return results

if __name__ == "__main__":
    onion_urls = [
        'http://kz62gxxle6gswe5t6iv6wjmt4dxi2l57zys73igvltcenhq7k3sa2mad.onion/deanonymize/redes_sociales/redes_sociales.html'
    ]

    scanner = RedesSocialesScanner(onion_urls)
    results = scanner.scan_social_media_for_all_urls()
    if results:
        print(json.dumps(results, indent=4))
