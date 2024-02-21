import requests
import re
import socks
import socket

class RedesSocialesScanner:
    def __init__(self, url):
        self.url = url
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def escanear_redes_sociales(self):
        try:
            # Configurar el proxy para las solicitudes
            socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            # Realizar la solicitud HTTP para obtener el contenido de la página
            response = requests.get(self.url, proxies=self.proxies)
            if response.status_code == 200:
                # Utilizar expresiones regulares para buscar enlaces a redes sociales
                patrones_redes_sociales = {
                    'twitter': r'https?://(?:www\.)?twitter\.com/\w+',
                    'facebook': r'https?://(?:www\.)?facebook\.com/\w+',
                    'instagram': r'https?://(?:www\.)?instagram\.com/\w+',
                    'reddit': r'https?://(?:www\.)?reddit\.com/r/\w+',
                    'youtube': r'https?://(?:www\.)?youtube\.com/\w+',
                    'whatsapp': r'https?://(?:www\.)?wa\.me/\w+',
                    'wechat': r'https?://(?:www\.)?weixin\.qq\.com/\w+',
                    'tiktok': r'https?://(?:www\.)?tiktok\.com/@\w+',
                    'linkedin': r'https?://(?:www\.)?linkedin\.com/in/\w+',
                    'telegram': r'https?://(?:www\.)?t\.me/\w+',
                    'snapchat': r'https?://(?:www\.)?snapchat\.com/add/\w+',
                    'pinterest': r'https?://(?:www\.)?pinterest\.com/\w+',
                    'quora': r'https?://(?:www\.)?quora\.com/profile/\w+',
                    'twitch': r'https?://(?:www\.)?twitch\.tv/\w+',
                    'discord': r'https?://(?:www\.)?discord\.gg/\w+',
                }

                redes_sociales_encontradas = {}
                for nombre_red_social, patron in patrones_redes_sociales.items():
                    redes_sociales_encontradas[nombre_red_social] = re.findall(patron, response.text)

                return redes_sociales_encontradas
            else:
                print(f'Error al obtener la página. Código de estado: {response.status_code}')
                return None
        except Exception as e:
            print(f'Error al escanear las redes sociales: {e}')
            return None

if __name__ == "__main__":
    url_pagina = input("Ingrese la URL de la página que desea escanear en busca de redes sociales: ")
    scanner = RedesSocialesScanner(url_pagina)
    redes_sociales_encontradas = scanner.escanear_redes_sociales()
    
    if redes_sociales_encontradas:
        print("Redes sociales encontradas:")
        for red_social, enlaces in redes_sociales_encontradas.items():
            if enlaces:
                print(f"{red_social.capitalize()}:")
                for enlace in enlaces:
                    print(enlace)
            else:
                pass
                #print(f"No se encontraron enlaces a {red_social.capitalize()}.")
    else:
        pass
        print("No se encontraron redes sociales en la página.")
